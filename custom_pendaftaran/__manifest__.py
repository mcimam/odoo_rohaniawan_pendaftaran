{
    "name": "Custom Pendaftaran",
    "version": "17.0.1.0.0",
    "category": "Custom",
    "depends": ['portal', 'contacts'],
    "author": "Mcimam",
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/institution.xml",
        "views/pendaftaran.xml",
        "views/partner.xml",
        "views/menu.xml",

        "views/portal_template.xml",
    ],
    "external_dependencies": {
        "python": ["qrcode"]
    },
    "license": "LGPL-3",
    "description": """
        Pendaftaran Custom Module
        """,
    "installable": True,
}
