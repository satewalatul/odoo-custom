{
    'name' : 'Excel Leads v2',
    'version' : '1.0.0',
    'summary': 'Excel Leads',
    'sequence': -100,
    'description': """Generate python leads""",
    'category': 'Spreadsheet',
    'data': [
        'data/cron.xml',
        'views/views.xml'
    ],

    'depends': ['base', 'crm'],

    'demo': [],

    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
