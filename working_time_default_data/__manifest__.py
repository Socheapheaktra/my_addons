{
    'name': 'Cambodia Default Working Time',
    'version': '14.0.0',
    'summary': 'Default Working Time Data',
    'description': '''
    - Version 14.0.0:
        - 8AM-5PM (8:00-12:00, 13:00-17:00)
        - 8AM-5PM (8:00-17:00)
        - 9AM-5PM (9:00-12:00, 12:00-17:00)
        - 9AM-5PM (9:00-17:00)
        - 1PM-10PM (13:00-17:00, 18:00-22:00)
        - 1PM-10PM (13:00-22:00)
        - 2PM-10PM (14:00-18:00, 18:00-22:00)
        - 2PM-10PM (14:00-22:00)
    ''',
    'category': 'Human Resource',
    'author': 'Socheapheaktra Doung',
    'depends': [
        'biz_resource_calendar_attendance'
    ],
    'data': [
        'data/working_time_data.xml',
        'data/attendance_data.xml'
    ],
    'installable': True,
    'auto_install': False,
}