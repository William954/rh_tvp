{
    'name': 'Ausencias TVP',
    'version': '1.0',
    'summary': 'Personalizacion de campos',
    'description': 'Adecuacion en el modulo de Ausencias o Leaves para el manejo de vacaciones en la empresa TVP',
    'category': 'Personalizacion',
    'author': 'Xmarts',
    'website': 'www.xmarts.com',
    'depends': ['base',
                'hr_attendance',
                'contacts',
                'hr',
                'fleet',
                'sale',
                'crm',
                'helpdesk',
                'hr_expense',
                'stock',
                'project',
                'hr_holidays',
                'sale_management',
                'timesheet_grid',
                'account'],

    'data': ['views/view.xml'],
    'installable': True,
    'aplication': True,
    'auto_install': False,
}



