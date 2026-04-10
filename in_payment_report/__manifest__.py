# -*- coding: utf-8 -*-
{
    'name': 'Print Payment Receipt',
    'version': '19.0.1.0',
    'category': 'Accounting/Reports',
    'summary': """
        Custom-designed payment receipt with summary and description,
        supporting Arabic and English layouts.
    """,

    'description': """
Print Payment Receipt
=============================

This module customizes the default Odoo Payment Receipt report by:

• Replacing the default layout with a modern, professional design  
• Adding a clear summary section for payment details  
• Displaying partner, payment reference, and cheque information  
• Supporting bilingual output (Arabic / English) automatically  
• Hiding unnecessary totals and invoice tables  
• Enhancing readability for official printed receipts  

Suitable for:
--------------
• Real estate companies  
• Accounting departments  
• Official payment documentation  

Compatible with Odoo 19.
    """,

    'author': 'Intajya',
    'license': 'LGPL-3',

    'depends': [
        'account',
        'sale',
        'web',
    ],

    'data': [
        'views/report_payment_receipt.xml',
    ],
    'images': ['static/description/icon1.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
