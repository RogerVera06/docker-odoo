# -*- coding: utf-8 -*-
{
    'name': "Performance Reviews",

    'summary': "Module that adds performance reviews",

    'description': """
    Module that adds performance evaluations and performance history reports
    """,

    'author': "Roger Vera",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'employees',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        
        #Views
        'views/hr_employee_views.xml',
        'views/hr_performance_review_views.xml',
        'views/ir_menu_views.xml',
        
        #Reports
        'report/hr_performance_review_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

