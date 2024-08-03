{
    'name': 'Sheet Music',
    'version': '1.0.0',
    'summary': 'Managing Sheet Music',
    'description': '''
    - Version 1.0.0:
        - Add Composer
        - Add Sheet Music
        - Add Music Category
        - View Sheet Music
    ''',
    'images': ['static/description/icon.png'],
    'category': 'Web',
    'author': 'Socheapheaktra Doung',
    'depends': [],
    'data': [
        'security/sheet_music_groups.xml',  # Added groups first because they're used in `access.csv`
        'security/ir.model.access.csv',
        'views/sheet_music_views.xml',
        'views/music_composer_views.xml',
        'views/music_category_views.xml',
        'views/sheet_music_actions.xml',
        'views/sheet_music_menus.xml',
        'data/music_composer_data.xml',
        'data/music_category_data.xml',
    ],
    "qweb": [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
