# -*- coding: utf-8 -*-
{
    'name': "employee_dashboard",

    'summary': """
        Employee Management""",

    'description': """
        Employee Management
    """,

    'author': "Damodar Aryal"
              "Utshab Bardewa"
              "Sharan Gyawali",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','web','mail','website','resource','hr','hr_attendance','biometric_attendance'],

    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        "data/email_template.xml",
        'views/server_action.xml',
        'data/ticket_sequence_code.xml',
        'static/src/xml/sidebar_template.xml',
        'static/src/xml/global_template.xml',
        'static/src/xml/dashboard_template.xml',
        'static/src/xml/dashboard_page.xml',
        'static/src/xml/departments_employee_leave.xml',
        'static/src/xml/calender_view_template.xml',
        'static/src/xml/view_profile_template.xml',
        'static/src/xml/kitchen_request_template.xml',
        'static/src/xml/overtime_view_template.xml',
        'static/src/xml/leave_request_template.xml',
        'static/src/xml/leave_history_template.xml',
        'static/src/xml/checkin_checkout_template.xml',
        'static/src/xml/overtime_history_template.xml',
        'static/src/xml/department_details.xml',
        'static/src/xml/attendance_history.xml',
        'views/views.xml',
        'views/kitchen_management.xml',
        'views/meal_request.xml',
        'views/employee_registration_view.xml',
        'views/employee_signup_template.xml',
        'views/employee_view_inherit.xml',
        'views/calender_view.xml',
        'views/views_inherit.xml',

        "data/website_menu.xml",
    ],
    'assets':{
        'web.assets_frontend':[
            '/employee_dashboard/static/src/css/style.scss',
            '/employee_dashboard/static/src/css/abcd.scss',
            "/employee_dashboard/static/src/css/leave_template.scss",
            # "/employee_dashboard/static/src/js/leave_request.js",
            "/employee_dashboard/static/src/js/sidebar_script.js",
            "/employee_dashboard/static/src/js/edit_profile.js",
            "/employee_dashboard/static/src/js/search.js",
            "/employee_dashboard/static/src/js/kitechen_request.js",
        ],
    },
    'demo': [
        'demo/demo.xml',
    ],
}
