# -*- coding: utf-8 -*-
from odoo import fields,models,api, _ 
from odoo.exceptions import ValidationError

class StockStoragTag(models.Model):
    _name = "stock.storage.tag"
    _description = "Smart storage tags"
    _rec_name = "name"
    
    name = fields.Char(
        string="Tag Name",
        required=True,
        help="Storage Tag Name"
    )
    
    color = fields.Char(
        string="Color",
        required=True,
        help="Tag Color"
    )
    
    description = fields.Text(
        string="Description",
        help="Tag Description"
    )
    
    _sql_constraints = [
        ('tag_name_unique','unique(name)',_('A tag with this name already exists.')),
        ]