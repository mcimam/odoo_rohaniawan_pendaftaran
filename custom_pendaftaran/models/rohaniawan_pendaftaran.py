# import qrcode
from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, models, fields, _


class Rohaniawan(models.Model):
    _name = 'rohaniawan.pendaftaran'
    _inherit = 'mail.thread'
    _description = 'Pendaftaran baru rohaniawan'

    name = fields.Char("Registration Number", default=lambda self: self.env['ir.sequence'].next_by_code('rohaniawan.pendaftaran'))
    card_number = fields.Char("Card Number")

    rname = fields.Char("Name", required=True)
    vname = fields.Char("Visudhi", required=True)
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female")
    ])

    nationality = fields.Many2one("res.country")

    nik = fields.Char("NIK/Pasport", required=True)
    pob = fields.Char("Place of Birth", required=True)
    dob = fields.Date("Date of Birth", required=True)
    institution = fields.Many2one("rohaniawan.institution")

    level = fields.Selection([
        ('bhikkhu', 'Bhikkhu/Bhikkhuni'),
        ('lama', 'Lama/Acariya/Renpoche'),
        ('padita', 'Padita'),
        ('rohaniawan', 'Rohaniawan'),
    ], 'Level')

    classification = fields.Selection([
        ('1', 'Anggota Sangha'),
        ('2', 'Pandita Lokapalasraya'),
        ('3', 'Pandita Dharmaduta'),
        ('4', 'Rohaniwan Asing')
    ], 'Classification')

    address = fields.Char("Address")
    city = fields.Char("Kota")
    province = fields.Char("Province")

    surat_pemohon = fields.Binary("Surat Pemohon", attachment=True)
    surat_bukti = fields.Binary("Bukti Rohaniawan", attachment=True)
    ktp = fields.Image("KTP / Paspor", attachment=True)
    pas_foto = fields.Image("Pas Foto", attachment=True)

    valid_till = fields.Date("Valid until")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('postponed', 'Postponed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', required=True)

    avatar = fields.Image("Avatar")
    qr_image = fields.Image("QR")

    submitter_id = fields.Many2one("res.users", "Submit by")
    partner_id = fields.Many2one("res.partner", "Related partner")
    verifier_id = fields.Many2one("res.partner", "Virified by", domain=[("is_dirjen", "=", True)])
    verifier_signature = fields.Binary(related='verifier_id.digitized_signature')

    card = fields.Binary("Card")

    def action_submit(self):
        for rec in self:
            rec.generate_card_number()
            rec.state = 'postponed'

    def action_approve(self):
        for rec in self:
            rec.generate_card_number()

            # Assign valid date
            rec.valid_till = fields.Datetime.today() + relativedelta(year=5)

            # Validate
            if not rec.verifier_id:
                raise exceptions.UserError(_("Please assign verifier"))

            if not rec.card:
                raise exceptions.UserError(_("Please input 'kartu rohaniawan'"))

            rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'

    def action_revert_to_draft(self):
        for rec in self:
            rec.verifier_id = False
            rec.state = 'draft'

    @api.model
    def register_new(self, values):
        pend = self.create(values)

        if not pend.partner_id:
            # Create new contact
            new_ct = self.env['res.partner'].create(
                {
                    'name': pend.name,
                }
            )
            pend.partner_id = new_ct

        pend.partner_id.is_rohaniawan = True

        pend.action_submit()
        return pend

    def generate_qr(self):
        """ Generate QR code containing certain value
        """

    def generate_card_number(self):
        self.ensure_one()
        kode_klasifikasi = "1"
        kode_lembaga = self.institution.code
        ttl = self.dob.strftime("%Y.%m.%d")
        nomor_urut = self.env['ir.sequence'].next_by_code('rohaniawan.card')
        gender = 1 if self.gender == 'male' else 2
        nomor = (f"{kode_klasifikasi}.{kode_lembaga}.{ttl}.{gender}.{nomor_urut}")

        self.card_number = nomor
    def get_portal_url(self):
        self.ensure_one()
        return (f"/my/regis/{self.id}")

    def get_card_url(self):
        self.ensure_one()
        return (f"/my/regis/{self.id}/card")

    def delete_registration(self):
        self.ensure_one()
        return ("/my/regis/delete",)
