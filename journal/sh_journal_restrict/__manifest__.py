# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Journal Restriction For Users",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "summary": "Journal access for user account journal users restriction journal entry restriction for users journal entry restriction invoice restriction for user bill restriction for user access control access management Team-Based Access Control for Accounting Account Journal Access Accounting Journal Access Invoice Access Group Restrict Journal Access Restrict Customer Invoices Access Restrict Vendor Bills Access accounting access control accounting access user wise journal entry restriction for users user journal restriction on Users restrict account journal to the specific users restrict journal to the specific users User Journal Restrictions User Journal entry Restrictions User accounting Restrictions Journal Security Journal Restricted Users Journal Restrictions Restrict Creation Of Journal Restriction for User access on Journal Restriction Access Allowed Journal Account Journal Restriction Journal Base User Access Journal Restriction For Users Journal Access Control User Restriction in Journals Journal Module User Journal Access Restriction System Journal Security Access Control for Journals User Permission Settings in Journal User Restriction Features in Journals Odoo Journal Restrict For Users Odoo restrict journal access restrict accounting journals per user assign allowed users per journal assign allowed journals per user restrict invoice journal restrict bill journal restrict cash journal restrict bank journal restrict sale journal restrict purchase journal allowed journals list display only allowed journals warning on unauthorized journal use admin full journal access security group based journal control accounting workflow journal visibility restriction Odoo accounting security fine grained journal access",
    "description": """This module restricts journals for specific users. You can add access users on journal configuration, only allowed users can access that journal. Users are allocated in specific journals like invoice, bill, cash, bank, sale & purchase, So users can not access a journal where the journal is not available for that user.""",
    "version": "0.0.1",
    "depends": [
        "account"
    ],
    "application": True,
    "data": [

        "security/journal_restrict_security.xml",
        "views/account_views.xml",
        "views/res_config_settings_views.xml",

    ],

    "images": ["static/description/background.gif", ],
    "auto_install": False,
    "installable": True,
    "price": 18,
    "currency": "EUR"
}
