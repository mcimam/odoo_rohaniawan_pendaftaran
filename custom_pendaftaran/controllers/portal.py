import base64
from odoo import _
from odoo.http import Controller, request, route, content_disposition

class CustomerPortal(Controller):

    def _prepare_portal_layout_values(self):
        return {}

    def _preprocess_pendaftaran_values(self, user, **kwargs):
        values = {
            'rname': kwargs.get('rname'),
            'vname': kwargs.get('vname'),
            'gender': kwargs.get('gender'),
            'nationality': kwargs.get('nationality'),
            'nik': kwargs.get('nik'),
            'pob': kwargs.get('pob', False),
            'dob': kwargs.get('dob'),
            'institution': kwargs.get('institution'),
            'level': kwargs.get('level'),
            'address': kwargs.get('address'),
            'city': kwargs.get('city'),
            'province': kwargs.get('province'),
            'submitter_id': user.id,
        }

        if kwargs.get('rname', '') == user.partner_id.name:
            values['partner_id'] = user.partner_id.id

        if kwargs.get('surat_pemohon'):
            values['surat_pemohon'] = base64.b64encode(kwargs['surat_pemohon'].read())

        if kwargs.get('surat_bukti'):
            values['surat_bukti'] = base64.b64encode(kwargs['surat_bukti'].read())

        if kwargs.get('ktp'):
            values['ktp'] = base64.b64encode(kwargs['ktp'].read())

        if kwargs.get('pas_foto'):
            values['pas_foto'] = base64.b64encode(kwargs['pas_foto'].read())

        return values

    @route('/my/regis', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def regis(self, **post):
        values = self._prepare_portal_layout_values()
        values['page_name'] = 'regis'
        if request.httprequest.method == 'POST':
            whitelisted_values = self._preprocess_pendaftaran_values(request.env.user, **post)
            pend = request.env['rohaniawan.pendaftaran'].sudo().register_new(whitelisted_values)
            if pend:
                values['success_msg'] = _('Form is submitted successfully')

        # prepare value
        user = request.env.user
        values['registrations'] = request.env['rohaniawan.pendaftaran'].search([('submitter_id', '=', user.id)])

        return request.render('custom_pendaftaran.portal_my_regis', values)

    @route('/my/regis/<int:regis_id>', type='http', auth='user', website=True, methods=['GET'])
    def edit_regis(self, regis_id, **post):
        values = self._prepare_portal_layout_values()
        pend = request.env['rohaniawan.pendaftaran'].browse(regis_id)
        if not pend:
            request.not_found()

        values['registration'] = pend
        return request.render("custom_pendaftaran.portal_my_regis_new", values)

    @route('/my/regis/<int:regis_id>/delete', type='http', auth='user', website=True, methods=['GET'])
    def delete_regis(self, regis_id, **post):
        values = self._prepare_portal_layout_values()

        pend = request.env['rohaniawan.pendaftaran'].browse(regis_id)
        pend.sudo().action_archive()

        values['success_msg'] = _('Form is archived successfully')
        return request.render("custom_pendaftaran.portal_my_regis", values)

    @route('/my/regis/<int:regis_id>/card', type="http", auth='user', website=True, methods=['GET'])
    def regis_card(self, regis_id, **post):
        # find image
        res = request.env['rohaniawan.pendaftaran'].browse(regis_id)

        if not res.card:
            return request.not_found()

        # filecontent = res.card.decode(encoding='ISO-8859-1')
        filecontent = base64.b64decode(res.card)

        return request.make_response(filecontent, [
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', content_disposition('card.pdf'))])

    @route('/my/regis/new', type='http', auth='user', website=True, methods=['GET'])
    def new_regis(self, **post):
        values = self._prepare_portal_layout_values()
        values['countries'] = request.env['res.country'].sudo().search([])
        values['institutions'] = request.env['rohaniawan.institution'].sudo().search([])

        # assign default value
        partner = request.env.user.partner_id
        values['rname'] = partner.name

        return request.render("custom_pendaftaran.portal_my_regis_new", values)
