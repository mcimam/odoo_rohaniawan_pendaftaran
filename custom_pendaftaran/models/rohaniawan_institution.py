from odoo import models, fields

class RohaniawanInstitution(models.Model):
    _name = 'rohaniawan.institution'
    _description = "Instutusi Budha"

    name = fields.Char("Name", required=True)
    initial = fields.Char("Initial", )
    code = fields.Char("Code")
