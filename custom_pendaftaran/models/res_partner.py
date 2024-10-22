from odoo import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    is_dirjen = fields.Boolean("Dirjen")
    is_rohaniawan = fields.Boolean("Rohaniawan")

    nip = fields.Char("NIP")
    digitized_signature = fields.Binary('Signature')
