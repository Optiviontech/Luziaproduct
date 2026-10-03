# -*- coding: utf-8 -*-

{
    "name": 'Create Bill Button (Odoo 19)',
    "summary": "Add the classic Create Bill button back to the Purchase Order form view (Odoo 19).",
    "description": """
        In Odoo 19, the Create Bill action is no longer available directly in the 
        Purchase Order form view, as the billing workflow has shifted toward 
        Upload Bill and list-view actions.

        This module brings back the classic Create Bill button directly into the 
        Purchase Order form view, following the familiar Odoo 18 workflow, 
        so users can generate vendor bills instantly while reviewing a purchase order.

        The standard Upload Bill feature remains untouched, allowing businesses 
        to choose the workflow that best fits their process.

        Key Features:
        - Adds the Create Bill button back to the Purchase Order form view.  
        - Restores the familiar Odoo 18–style billing flow in Odoo 19.  
        - No impact on Odoo 19’s Upload Bill functionality.  
        - Faster vendor bill creation without switching to list views.  
        
    """,
    "author": "CodeSphere Tech",
    "website": "https://www.codespheretech.in/",
    "category": "Purchase",
    "version": "19.0.1.0.0",
    "sequence": 0,
    "currency": "USD",
    "price": "0.00",
    "depends": ["purchase",],
    'data': [
        "views/purchase_order_view.xml",
    ],
    "images": ["static/description/Banner.png"],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False
}

