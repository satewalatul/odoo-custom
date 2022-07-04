# -*- coding: utf-8 -*-
{
    'name': "Sale Order Custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Youngman",
    'website': "https://www.youngman.co.in/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'jobsites'],

    # always loaded
    'data': [
        'views/sale_order_form.xml',
        'report/sale_report_inherit.xml',
    ],
}
