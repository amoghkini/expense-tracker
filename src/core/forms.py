from flask_wtf import Form
from wtforms import fields

class ColumnForm(Form):
    col_id = fields.HiddenField()
    column_width = fields.IntegerField('col width',description='width of columms per bootstrap3 grid')
    push = fields.IntegerField('push',description='push column x col width to the right')
    pull = fields.IntegerField('pull',description='pull column x col width to the left')
    offset = fields.IntegerField('offset',description='place column offset x col width from normal placement')