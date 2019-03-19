# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class account_payment(models.Model):
	_inherit = 'account.payment'

	@api.model
	def default_get(self, default_fields):
		default_it_type_document = False
		default_nro_comprobante = False

		t = self.env['account.invoice'].browse(self._context.get('active_id'))
		if t:
			default_it_type_document = t.it_type_document.id
			default_nro_comprobante = t.reference

		contextual_self = self.with_context(default_it_type_document=default_it_type_document, default_nro_comprobante=default_nro_comprobante)
		return super(account_payment, contextual_self).default_get(default_fields)


	@api.multi
	def unlink(self):
		for rec in self:
			rec.move_name = False
		return super(account_payment,self).unlink()



	@api.multi
	def post(self):
		for inv in self:
			if inv.currency_id.name == 'USD':
				currency_obj = self.env['res.currency'].search([('name','=','USD')])
				if len(currency_obj)>0:
					currency_obj = currency_obj[0]
				else:
					raise UserError( 'Error!\nNo existe la moneda USD' )

				fecha = inv.payment_date if inv.payment_date else fields.Date.context_today(inv)
				tipo_cambio = self.env['res.currency.rate'].search([('name','=',fecha),('currency_id','=',currency_obj.id)])

				if len(tipo_cambio)>0:
					tipo_cambio = tipo_cambio[0]
				else:
					raise UserError( 'Error!\nNo existe el tipo de cambio para la fecha: '+ str(fecha) )
				
				vactual = 0
				ractual = 0

				if inv.check_currency_rate:
					vactual = tipo_cambio.type_sale
					ractual = tipo_cambio.rate

					tipo_cambio.type_sale = inv.change_type
					tipo_cambio.rate = 1.0 / inv.change_type

				else:
					inv.change_type = tipo_cambio.type_sale


				t = super(account_payment,inv).post()

				inv.refresh()
				for i in inv.move_line_ids[0].move_id.line_ids:
					i.tc = tipo_cambio.type_sale
					if i.tax_amount:
						i.tax_amount = i.debit + i.credit

				if inv.check_currency_rate:
					tipo_cambio.type_sale = vactual
					tipo_cambio.rate = ractual


				if inv.move_line_ids.ids:
					inv.move_line_ids[0].move_id.means_payment_it = inv.means_payment_id
					for elem in inv.move_line_ids:
						nro_c = inv.nro_comprobante
						if elem.account_id.id == inv.journal_id.default_debit_account_id.id:
							elem.move_id.rendicion_id = inv.rendicion_id.id
							elem.rendicion_id = inv.rendicion_id.id
							nro_c = inv.rendicion_id.name
						elem.nro_comprobante = nro_c 
						elem.type_document_it = inv.it_type_document.id
						if elem.account_id.user_type_id.type == 'liquidity':								
							elem.nro_comprobante =  self.nro_caja
							elem.type_document_it = False
			else:
				t = super(account_payment,inv).post()

				if inv.move_line_ids.ids:
					inv.move_line_ids[0].move_id.means_payment_it = inv.means_payment_id
					for elem in inv.move_line_ids:
						nro_c = inv.nro_comprobante
						if elem.account_id.id == inv.journal_id.default_debit_account_id.id and inv.rendicion_id.id:
							elem.move_id.rendicion_id = inv.rendicion_id.id
							elem.rendicion_id = inv.rendicion_id.id
							nro_c = inv.rendicion_id.name
						elem.nro_comprobante = nro_c 
						elem.type_document_it = inv.it_type_document.id
						if elem.account_id.user_type_id.type == 'liquidity' and  not inv.rendicion_id.id:
							elem.nro_comprobante =  self.nro_caja
							elem.type_document_it = False
