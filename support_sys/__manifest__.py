# -*- coding: utf-8 -*-
{
    'name': "support_sys",
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,
    'sequence': 1,
    'author':"Utshab Bardewa"
             "Sharan Gyawali"
             "Damodar Aryal",
    'depends': ['base','web','hr','mail','employee_dashboard'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/expense_request_view.xml',
        'views/configuration_view.xml',
        'data/ticket_sequence_code.xml',
        'views/ticket_request_view.xml',
        'views/employee_task_assignment_view.xml',
        'views/employee_daily_work_report.xml',
        'views/client_ view.xml',
        'views/parent_menu.xml',
        'views/sidebar_template.xml',
        'views/advance_request.xml',
        'views/daily_tasks.xml',
        'views/expenditure_data.xml',
        'views/hr_employee_inherit.xml',
        'views/assigned_task_view.xml',
        'views/ticket_raise.xml',

    ],

    'assets': {
        'web.assets_frontend': [
            'support_sys/static/src/scss/expenditure_data.scss',
            # 'support_sys/static/src/scss/multiple_select.sccss',
            'support_sys/static/src/js/branches.js',
            'support_sys/static/src/js/task_completion.js',

        ]

    }
}