# -*- coding: utf-8 -*-

{
    'name': "SMS Manager",
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'SMS Management Module for Quotations/Orders',
    'description': """
        Manages SMS in Unit Price in Quotations/Orders
    """,
    'author': "Ajay",
    'website': "https://www.youngman.co.in/",
    'sequence': -100,

    'depends': ['base'],

    'data': [
        'views/views.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}
