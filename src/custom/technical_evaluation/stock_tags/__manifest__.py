# -*- coding: utf-8 -*-
{
    'name': "Stock Storage Tags",

    'summary': "Module for smart tags for products",

    'description': """
Module for the creation, assignment and visualization of smart tags for products
    """,

    'author': "Roger Vera",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #Data
        'data/stock_storage_tag_data.xml',
        
        #Views
        'views/product_template_views.xml',
        'views/stock_storage_tag_views.xml',
        'views/ir_menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

