{
    'name': 'Complementos TVP',
    'version': '1.0',
    'summary': 'Personalizacion de campos',
    'description': 'Adecuacion en el modulo de Ausencias, Empleados y Contratos para el manejo de informacion en la empresa TVP',
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
                'account',
                'hr_contract'],

    'data': ['views/view.xml'],
    'installable': True,
    'aplication': True,
    'auto_install': False,
}



