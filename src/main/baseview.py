import os
import json
from flask.views import MethodView
from flask import flash, jsonify, make_response, redirect, render_template, url_for, current_app, request, Flask
from inflection import pluralize
from wtforms.form import FormMeta
from typing import Any, Optional, Type, Union


is_verbose = lambda: os.environ.get('VERBOSE') and True or False


# classproperty decorator
class classproperty(object):
    """
    This decorator is used to create read-only properties that are accessed directly on the class
    """
    def __init__(self, getter):
        self.getter = getter
        
    def __get__(self, instance, owner):
        return self.getter(owner)
    
    
class Flasher(object):
    DEFAULT_CATEGORY: str = 'info'
    DARK_CLASS: str = 'dark'
    DANGER_CLASS: str = 'danger'
    INFO_CLASS: str = 'info'
    LIGHT_CLASS: str = 'light'
    SUCCESS_CLASS: str = 'success'
    WARNING_CLASS: str = 'warning'

    def __init__(
        self, 
        default: Optional[str] = None, 
        class_map: Optional[dict[str, str]] = None
    ) -> None:
        if default:
            self.DEFAULT_CATEGORY = default
        if class_map:
            self._set_classes(class_map)

    def _set_classes(
        self, 
        class_map: dict[str, str]
    ) -> None:
        DEFAULT_MAP = {
            'dark': self.DARK_CLASS,
            'danger': self.DANGER_CLASS,
            'info': self.INFO_CLASS,
            'light': self.LIGHT_CLASS,
            'success':self.SUCCESS_CLASS,
            'warning':self.WARNING_CLASS
        }
        for k in class_map:
            tmp = class_map.get(k)
            if tmp is not None:
                DEFAULT_MAP[k] = tmp

    def flash(self, msg: str, cat: Optional[str] = None):
        cat = cat or self.DEFAULT_CATEGORY
        return flash(msg, cat)

    def add_dark(self, msg: str):
        return self.flash(msg, self.DARK_CLASS)
    
    def add_danger(self, msg: str):
        return self.flash(msg, self.DANGER_CLASS)
    
    def add_info(self, msg: str):
        return self.flash(msg, self.INFO_CLASS)
    
    def add_light(self, msg: str):
        return self.flash(msg, self.LIGHT_CLASS)
    
    def add_success(self, msg: str):
        return self.flash(msg, self.SUCCESS_CLASS)
    
    def add_warning(self, msg: str):
        return self.flash(msg, self.WARNING_CLASS)


class PostViewAddon(object):
    def _process_post(self):
        self.post_data = ((request.data and json.loads(request.data)) if not request.form else dict(request.form.items())) if not request.mimetype == 'application/json' else request.json


class BaseView(MethodView):
    _template: Optional[str] = None
    _form: Optional[Union[FormMeta, Any]] = None
    _context: dict[str, Any] = {}
    _form_obj: Optional[Any] = None
    _obj_id: Optional[int] = None
    _form_args: dict[str, Any] = {}
    _default_view_routes: dict[str, str] = {}
    _flasher_class_map: Optional[dict[str, str]] = None

    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self._flasher = Flasher(class_map=self._flasher_class_map) if self._flasher_class_map else Flasher()

    def flash(self, msg: str):
        return self._flasher.flash(msg)

    def dark(self, msg: str):
        return self._flasher.add_dark(msg)
    
    def danger(self, msg: str):
        return self._flasher.add_danger(msg)
    
    def info(self, msg: str):
        return self._flasher.add_info(msg)
    
    def light(self, msg: str):
        return self._flasher.add_light(msg)
    
    def success(self, msg: str):
        return self._flasher.add_success(msg)

    def warning(self, msg: str):
        return self._flasher.add_warning(msg)
    
    @classmethod
    def _add_default_routes(
        cls,
        app: Flask
    ) -> None:        
        for route,endpoint in cls._default_view_routes.items():
            if is_verbose():
                print('attaching',route,'to view func',endpoint)
            app.add_url_rule(route,endpoint,view_func=cls.as_view(endpoint))

    def render(self,**kwargs):
        if self._template is None:
            return NotImplemented
        if kwargs:
            self._context.update(kwargs)
        if "errors" not in self._context:
            self._context['errors'] = {}
            
        if self._form is not None:

            if type(self._form) == FormMeta:
                if self._form_obj is not None:
                    self._context['form'] = self._form(obj=self._form_obj,**self._form_args)
                else:
                    self._context['form'] = self._form(**self._form_args)
                if self._obj_id is not None:
                    self._context['obj_id'] = self._obj_id
            else:
                self._context['form'] = self._form
            choices = self._context.get('choices')
            if choices:
                for field in self._context['form']:
                    if hasattr(field,field.__name__) and hasattr(getattr(field,field.__name__),field.__name__):
                        inner_field = getattr(getattr(field,field.__name__),getattr(field.__name__))
                        if hasattr(inner_field,'choices'):
                            setattr(inner_field,'choices',choices)
            for f,v in self._form_args.items():
                self._form.__dict__[f].data = v
        return render_template(self._template,**self._context)

    def redirect(self, endpoint: str, **kwargs: Any):
        if not kwargs.pop('raw', False):
            return redirect(url_for(endpoint, **kwargs))
        return redirect(endpoint, **kwargs)
        
    def form_validated(self):
        if self._form:
            return self._form().validate()
        return False

    def get_form_data(self):
        result = {}
        for field in self._form():
            name = field.name
            if '_' in field.name:
                if not field.name.startswith('_'):
                    if not field.name.endswith('_'):
                        if field.name.split('_')[0] == field.name.split('_')[1]:
                            name = field.name.split('_')[0]
            result[name] = field.data
        return result
    
    def get_env(self) -> Any:
        return current_app.create_jinja_environment()
    
    @property
    def flasher(self) -> Flasher:
        return self._flasher


class ModelView(BaseView):
    # ModelView is an abstract class
    # just an interface really
    # to use the ModelView create your own view class
    # and use this as the parent class, and 
    # set its _model class attr to the class to wrap ie:
    # 
    # class UserModelView(ModelView):
    #   _model = User
    _model = None

    def render(self,**kwargs):
        alt_model_id = '{0}_id'.format(self._model.__name__.lower())
        if self._model is not None:
            if 'model_id' in kwargs:
                model_id = kwargs.pop('model_id')
            elif alt_model_id in kwargs:
                model_id = kwargs.pop('alt_model_id')
            else:
                model_id = None
            if model_id is not None:
                self._context['object'] = self.get_by_id(model_id)
            else:
                self._context['object'] = self._model()
            self._context['model'] = self._model
        return super(ModelView,self).render(**kwargs)

    def add(self,**kwargs):
        tmp = self._model(**kwargs)
        tmp.save()
        return tmp

    def update(self,model_id,**kwargs):
        tmp = self._model.query.filter_by(self._model.id==model_id).first()
        if 'return' in kwargs:
            if kwargs.pop('return',None):
                rtn = True
            else:
                rtn = False
        for k in kwargs.keys():
            tmp.__dict__[k] = kwargs[k]
        tmp.save()
        if rtn: return tmp

    def get_all(self):
        return self._model.get_all()

    def get_by_id(self,model_id):
        return self._model.get_by_id(model_id)

class AddModelView(ModelView,PostViewAddon):
    _success_endpoint = None
    _success_message = 'You successfully added an item'
    
    def get(self):
        return self.render()

    def post(self):
        self._process_post()
        self._context['obj'] = self._model(**self.post_data).save()
        self.success(self._success_message)
        return self.redirect(self._success_endpoint or '.index')


def AddModelApiView(ModelView,PostViewAddon):
    def post(self):
        self._process_post()
        return jsonify(**self.add(**self.post_data).to_json())

class ListModelView(ModelView):
    def get(self):
        name = pluralize(self._model.__name__)
        return jsonify(name=[m.to_json() for m in self.get_all()])

class ViewModelView(ModelView):
    def get(self,item_id):
        m = self.get_by_id(item_id)
        return jsonify(**m.to_json())

class ModelAPIView(ModelView):
    __abstract__ = True

    @classproperty
    def _default_view_routes(cls):
        if cls is ModelAPIView:
            return {}
        name = cls.__name__.lower()
        _default_view_routes = {
                '/{}/list'.format(name):'{}-list'.format(name),
                '/{}/detail'.format(name):'{}-detail'.format(name),
                '/{}/edit'.format(name):'{}-edit'.format(name),
        }
        return _default_view_routes


    def render(self,**kwargs):
        old_rtn = super(ModelAPIView,self).render(**kwargs)
        rtn = make_response(json.dumps(self._context))
        rtn.headers['Content-Type'] = 'application/json'
        return rtn