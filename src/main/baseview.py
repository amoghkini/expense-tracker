import os
import json
from flask.views import MethodView
from flask import flash, jsonify, make_response, redirect, render_template, url_for, current_app, request, Flask
from inflection import pluralize
from wtforms.form import FormMeta
from typing import Any, Optional, Type, Union


is_verbose = lambda: os.environ.get('VERBOSE') and True or False

    
class Flasher(object):
    DEFAULT_CATEGORY: str = 'info'
    PRIMARY_CLASS: str = 'primary'
    SECONDARY_CLASS: str = 'secondary'
    SUCCESS_CLASS: str = 'success'
    DANGER_CLASS: str = 'danger'
    WARNING_CLASS: str = 'warning'
    INFO_CLASS: str = 'info'
    LIGHT_CLASS: str = 'light'
    DARK_CLASS: str = 'dark'

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
            'primary': self.PRIMARY_CLASS,
            'secondary': self.SECONDARY_CLASS,
            'success':self.SUCCESS_CLASS,
            'danger': self.DANGER_CLASS,
            'warning':self.WARNING_CLASS,
            'info': self.INFO_CLASS,
            'light': self.LIGHT_CLASS,
            'dark': self.DARK_CLASS
        }
        for k in class_map:
            tmp = class_map.get(k)
            if tmp is not None:
                DEFAULT_MAP[k] = tmp

    def flash(self, msg: str, cat: Optional[str] = None):
        cat = cat or self.DEFAULT_CATEGORY
        return flash(msg, cat)

    def add_primary(self, msg: str):
        return self.flash(msg, self.PRIMARY_CLASS)
    
    def add_secondary(self, msg: str):
        return self.flash(msg, self.SECONDARY_CLASS)
    
    def add_success(self, msg: str):
        return self.flash(msg, self.SUCCESS_CLASS)
    
    def add_danger(self, msg: str):
        return self.flash(msg, self.DANGER_CLASS)
    
    def add_warning(self, msg: str):
        return self.flash(msg, self.WARNING_CLASS)
    
    def add_info(self, msg: str):
        return self.flash(msg, self.INFO_CLASS)
    
    def add_light(self, msg: str):
        return self.flash(msg, self.LIGHT_CLASS)
    
    def add_dark(self, msg: str):
        return self.flash(msg, self.DARK_CLASS)
    
    
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
            
        return render_template(self._template,**self._context)

    def redirect(self, endpoint: str, **kwargs: Any):
        if not kwargs.pop('raw', False):
            return redirect(url_for(endpoint, **kwargs))
        return redirect(endpoint, **kwargs)
        
    
    def get_env(self) -> Any:
        return current_app.create_jinja_environment()
    
    @property
    def flasher(self) -> Flasher:
        return self._flasher