# -*-  coding: utf -8 -*-
{
    'name': "Modulo de aprendizaje",
    'sumary': """Aprendiendo a utilizar Odoo""",
    'descripcion': """
""",

    'author': "Quadit",
    'website': "",

    # categories  can be use  to filter modules in modules listing

    'category': 'tutorial',
    'version': '1.0',

    'depends': ['base', 'sale'],

    'data': {
        'views/academy.xml',
        'security/ir.model.access.csv',
    },

    # only loaded in demostration mode
    'demo': {

    },
}
