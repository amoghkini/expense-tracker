import os
import sys
from flask import Flask
from typing import Any, Tuple
from werkzeug.utils import import_string, find_modules

from config.settings import get_config, BaseConfig, get_server_helper_config_from_yaml
from main.app_life_cycle import AppLifeCycle
from main.baseview import is_verbose
from main.error_handler import ErrorHandler
from main.exceptions import (
    NoContextProcessorException, 
    NoExtensionException, 
    NoInstalledBlueprintsSettingException,
    NoRouteModuleException, 
    NoTemplateFilterException
)
from utils.logger import Logger


class MyFlask(Flask):
    jinja_options = dict(Flask.jinja_options)
    jinja_options.setdefault('extensions',
            []).append('jinja2_highlight.HighlightExtension')
        
class AppFactory(object):
    """
    Main class for managing Flask application setup and configuration.
    """
    
    __routes_registered: bool = False
    
    def __init__(
        self,
    ) -> None:
        self.app_config: BaseConfig = get_config()
        
    def get_app(
        self,
        app_module_name: str,
        **kwargs: Any
    ) -> Flask:
        self.app: MyFlask = MyFlask(app_module_name, **kwargs)
        self.app.config.from_object(self.app_config)
        self.app.config['VERBOSE'] = is_verbose()

        self.__server_bootup_operations()
        
        self.__set_path()
        self.__bind_extensions()
        self.__register_routes()
        self.__load_models()
        self.__load_views()
        self.__register_context_processors()
        self.__register_templalte_filters()
        self.__register_template_extensions()
        self.__register_middlewares()
        
        # Instantiate AppLifecycle with the app instance
        lifecycle_manager = AppLifeCycle(self.app)
        lifecycle_manager.register_before_first_request()
        lifecycle_manager.register_before_request()
        lifecycle_manager.register_after_request()
        lifecycle_manager.register_teardown_appcontext()
        
        error_handler_manager = ErrorHandler(self.app)
        error_handler_manager.register_400_error()
        error_handler_manager.register_403_error()
        error_handler_manager.register_404_error()
        error_handler_manager.register_405_error()
        error_handler_manager.register_500_error()
        return self.app
    
    def __server_bootup_operations(self):
        # Setup the logger
        Logger.configure_logger('server')
        
        # Setup profile pic directory
        server_config: dict = get_server_helper_config_from_yaml()
        profile_pic_dir: str = server_config.get('paths','').get('profile_pics')
        if not os.path.exists(profile_pic_dir):
            os.makedirs(profile_pic_dir)
            print("New directory created==>", profile_pic_dir)
    
    def __set_path(self):
        sys.path.append(self.app.config.get("ROOT_PATH", ''))
    
    def __get_imported_stuff_by_path(
        self, 
        path: str
    ) -> Tuple[Any, str]:
        """
        Import module and get object by its path.
        
        Args:
            path (str): Path to the module and object.
        
        Returns:
            Tuple[Any, str]: A tuple containing the imported module and object name.
        
        Example:
            >>> main = Main(config)
            >>> module, object_name = main.__get_imported_stuff_by_path('my_module.my_object_path')
        """
        module_name: str
        object_name: str
        
        module_name, object_name = path.rsplit('.', 1)
        module: Any = import_string(module_name)
        return module, object_name
            
    def __bind_extensions(self) -> None:
        """
        Bind extensions to the Flask application.
        
        Raises:
            NoExtensionException: If an extension is not found.
        """
        if self.app.config.get('VERBOSE', False):
            print("Binding extensions...")
        
        extenstions: list[str] = self.app.config.get('EXTENSIONS', [])            
        for extension_path in extenstions:
            module, extension_name = self.__get_imported_stuff_by_path(extension_path)
            
            if not hasattr(module, extension_name):
                raise NoExtensionException(f"No {extension_name} extension found")
            
            extension: Any = getattr(module, extension_name)
            if getattr(extension, 'init_app', False):
                extension.init_app(self.app)
            else:
                extension(self.app)
                        
    def __register_routes(self) -> None:
        """
        Register routes with the Flask application.
        
        Raises:
            NoRouteModuleException: If no blueprints are found.
        """
        if not AppFactory.__routes_registered:
            AppFactory.__routes_registered = True
            
            if self.app.config.get('VERBOSE', False):
                print("Registering routes")
        
            url_modules: list[str] = self.app.config.get("URL_MODULES", [])
                         
            for url_module in url_modules:
                if self.app.config.get('VERBOSE', False):
                    print(f"Working on module {url_module}")
                    
                module, route_name = self.__get_imported_stuff_by_path(url_module)
                if self.app.config.get('VERBOSE',False):
                    print(f"Route: {route_name}")
                    print(f"Module: {module}")
                    
                if route_name == 'routes' and hasattr(module, route_name):
                    if self.app.config.get('VERBOSE',False):
                        print(f"Setting: {route_name}")
                        print('\tsetting up routing for {} with\n\troute module {}\n'.format(module.__package__,module.__name__))
                    self.__setup_routes(getattr(module, route_name))
                else:
                    raise NoRouteModuleException(f"No {route_name} url module found")
            if self.app.config.get('VERBOSE',False):
                print('Finished registering blueprints and url routes')
        else:
            print(f"All the routes are already registered")
            if self.app.config.get('VERBOSE',False):
                print(f"Skipping this processes...")
            
    def __setup_routes(
        self,
        routes
    ) -> None:

        for route in routes:
            blueprint, rules = route[0], route[1:]

            for item in rules:
                if len(item) == 3:
                    pattern, endpoint, view = item
                else:
                    pattern, view = item
                    endpoint = None
                
                if self.app.config.get('VERBOSE', False):
                    print('\t\tplugging url Pattern:',pattern)
                    print('\t\tinto View class/function:',hasattr(view,'func_name') and view.view_class.__name__ or view.__name__)
                    print('\t\tat endpoint:',endpoint or view.func_name)
                
                if isinstance(blueprint, tuple):
                    blueprint = blueprint[0]
                blueprint.add_url_rule(pattern,endpoint or view.func_name,view_func=hasattr(view,'func_name') and view or view.as_view(endpoint))
            if not self.__check_for_registered_blueprint(blueprint):
                if self.app.config.get('VERBOSE',False):
                    print('\n\t\t\tNow registering {} as blueprint\n\n'.format(str(blueprint.name)))
                self.app.register_blueprint(blueprint)
    
    
    def __check_for_registered_blueprint(
        self,
        blueprint
    ) -> bool:
        found: bool = False
        for name in [str(x) for x in self.app.blueprints]:
            if blueprint.__class__.__name__.split('.')[-1] in name:
                found = True
        return found
    
    def __register_context_processors(self) -> None:
        """
        Register context processors with the Flask application.
        
        Raises:
            NoContextProcessorException: If no blueprints are found.
        """
        if self.app.config.get('VERBOSE',False):
            print(f"Registering template context processors")
        
        context_processors: list[str] = self.app.config.get("CONTEXT_PROCESSORS", [])       
        for context_processor in context_processors:
            module, context_processor_name = self.__get_imported_stuff_by_path(context_processor)
            if hasattr(module, context_processor_name):
                self.app.context_processor(getattr(module, context_processor_name))
            else:
                raise NoContextProcessorException(f"No {context_processor_name} context processor found")
            
    def __register_templalte_filters(self) -> None:
        """
        Register template filters with the Flask application.
        
        Raises:
            NoTemplateFilterException: If no blueprints are found.
        """
        if self.app.config.get('VERBOSE',False):
            print(f"Registering template filters")

        template_filters: list[str] = self.app.config.get('TEMPLATE_FILTERS', [])
                    
        for filter_path in template_filters:
            module, filter_path_name = self.__get_imported_stuff_by_path(filter_path)
            if hasattr(module, filter_path_name):
                self.app.jinja_env.filters[filter_path_name] = getattr(module, filter_path_name)
            else:
                raise NoTemplateFilterException(f"No {filter_path_name} template filter found")
          
    def __register_template_extensions(self):
        self.app.jinja_options = dict(Flask.jinja_options)
        exts = self.app.config.get('TEMPLATE_EXTENSIONS') or ['jinja2_highlight.HighlightExtension']
        self.app.jinja_options.setdefault('extensions', []).extend(exts)
        
    def __register_middlewares(self) -> None:
        if self.app.config.get('VERBOSE',False):
            print(f"Registering middlewares")
            
        middlewares: list[str] = self.app.config.get('MIDDLEWARE', [])
        for middleware_path in middlewares:
            module_name, middleware_name = middleware_path.rsplit('.', 1)
            module_name, _ = self.__get_imported_stuff_by_path(middleware_path)
            middleware: Any = getattr(module_name, middleware_name, None)
            if not middleware:
                self.app.wsgi_app = middleware(self.app.wsgi_app)
                
    def __load_models(self):
        return self.__load_resource('models')
    
    def __load_views(self):
        return self.__load_resource('views')
    
    def __is_public_attr(
        self,
        name: str
    ):
        return not name.startswith('_')
    
    def __load_resource(
        self,
        type_name: str
    ):
        blueprint_settings_path = ((self.app.config.get('BLUEPRINTS',None) and 'BLUEPRINTS') or (self.app.config.get('INSTALLED_BLUEPRINTS',None) and 'INSTALLED_BLUEPRINTS') or False)
        if not blueprint_settings_path:
            raise NoInstalledBlueprintsSettingException(f"You must have a setting for either  INSTALLED_BLUEPRINTS or BLUEPRINTS")
        
        for blueprint_path in self.app.config.get(blueprint_settings_path, []):
            module_name, object_name = blueprint_path.rsplit('.',1)
            blueprint_module, blueprint_name = self.__get_imported_stuff_by_path(blueprint_path)
            
            blueprint = getattr(blueprint_module, blueprint_name)
            modules = find_modules(module_name)
            
            for module in modules:
                if type_name in module:
                    mod = import_string(module)
                    for item in dir(mod):
                        cls = getattr(mod, item)
                        if self.__is_public_attr(item) and item[0] == str(item[0]).upper() and 'class' in str(cls) and 'view' in str(item).lower():
                            if hasattr(cls,'_add_default_routes') and getattr(cls,'_default_view_routes'):
                                if is_verbose():
                                    print('getting default routes for ',cls.__name__)
                                getattr(cls,'_add_default_routes')(app=blueprint or self.app)
                                