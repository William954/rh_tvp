{
    'name': 'Campos para RH, Contratos y Ausencias',
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
                'hr_holidays',
                'account',
                'hr_contract'],

    'data': ['views/view.xml'],
    'installable': True,
    'aplication': True,
    'auto_install': False,
}


