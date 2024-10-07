{
    'name': 'Biz Unit Test',
    'version': '0.1.0',
    'summary': 'Unit Testing Module',
    'description': '''
    - 0.1.0:
        - Base Unit Test
    ''',
    'category': 'Technical',
    'author': 'Socheapheaktra Doung',
    'depends': [
        'biz_hr_employee_info',
        'biz_payroll_cambodia',
        'biz_resource_calendar_attendance',
        'biz_hr_work_entry_holidays',
        'biz_hr_work_entry_duration_day',
        'biz_hr_employee_leaves_report',
    ],
    'data': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [
            'StrEnum',
            'marshmallow',
        ],
    }
}
