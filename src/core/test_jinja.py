import os
from jinja2 import Environment
from typing import Any

from core.layouts import LayoutManager


jinja2_env = Environment(
    block_start_string="{{%",
    block_end_string="%}}",
    variable_start_string="{{{",
    variable_end_string="}}}",
    trim_blocks=True,
)

DEFAULT_LAYOUT = 'TWO_COL_LEFTBAR'


class Row(object):
    _cols = None
    _height = None
    
    def __init__(
        self,
        height,
        cols: list[Any] = []
    ) -> None:
        self._cols = cols
        self._height = height
        
    @property
    def height(self):
        return self._height
    
    @property
    def cols(self):
        return self._cols
    

class Column(object):
    _count = 0
    _rows: list[Any] = []
    
    def __init__(
        self,
        **kwargs
    ) -> None:
        Column._count += 1
        self._id: int = Column._count
        self._args: dict = {}
        if 'rows' in kwargs:
            self._rows = kwargs.pop('rows')
        for arg in kwargs:
            self._args[arg] = kwargs[arg]
        self._args['debug_id'] = self._id
        if 'height' in kwargs:
            self.height = kwargs.pop('height')
            
    @property
    def args(self) -> dict:
        return self._args or {}
    
    @property
    def blockname(self) -> str:
        return f'column_{str(self._id)}'
    
col = lambda x,y=100,debug=False: Column(num=x,height=y,debug=debug)
row = lambda x, **y: Row(height=x,**y)


def make_grid(**kwargs):
    cols = kwargs.pop('cols')
    footer = (row('150',cols=(col(3,'150'),col(3,'150'),col(3,'150'),col(3,'150'))),)
    _cols = []
    
    for w,h in cols:
        _cols.append(col(w,h))
        
    content = (row('760',cols=_cols),)
    flocation = 'admin/templates/make_grid.html'        # take this from json or yaml config file. Write two methods two read json and yaml config files
    if not os.path.exists(flocation):
        flocation =  os.path.join(os.pardir,'admin/templates/make_grid.html')
    return jinja2_env.from_string(open(flocation,'r').read()).render(dict(rows=content+footer,fluid=True,wide=True,body_style=''))


def main(layout = DEFAULT_LAYOUT, page_type='body'):
    ''' layout = ONE_COL_EMPTY ....
        page_type = BODY, FOOTER
    '''
    _cols = LayoutManager.get_cols(layout)
    _height = LayoutManager.get_height(page_type)
    cols = [(x,_height) for x in _cols]
    return make_grid(cols=tuple(cols))