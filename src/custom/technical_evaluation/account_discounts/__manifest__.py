# -*- coding: utf-8 -*-
{
    'name': "Discount Policies on Invoices",

    'summary': "Module that allows managing discounts according to customer types",

    'description': """
    Module that allows managing discounts according to customer types in the 'Invoicing' module
    """,

    'author': "Roger Vera",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #Data
        'data/account_discount.xml',

        #Views
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'views/account_discount_views.xml',
        'views/ir_menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

