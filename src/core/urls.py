from core import core_blueprint
from core.views import (
   AboutView, 
   IndexView,
)


core_blueprint.json_decoder = None


routes = [
   (
       (core_blueprint),
            ('/', 'index_api', IndexView),
            ('/about', 'about_api', AboutView),
   ) 
]