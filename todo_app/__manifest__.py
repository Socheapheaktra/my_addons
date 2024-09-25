{
    'name': 'To-Do Application',
    'version': '14.0.0',
    'summary': 'Helps you Organize your Tasks',
    'description': '''
    This is my custom To-Do Application to keep myself Organize with all the tasks assigned by Product Owner to my team.
    
    - Version 14.0.0
        - Add Stakeholder (Client)
        - Add Task Responsible (Person in charge of each Task)
        - Add Task Menu
    ''',
    'images': ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/todo_list_views.xml',
        'views/stakeholder_views.xml',
        'views/person_in_charge_views.xml',
    ],
    'category': 'Web',
    'author': 'Socheapheaktra Doung',
    'depends': [],
    'installable': True,
}
