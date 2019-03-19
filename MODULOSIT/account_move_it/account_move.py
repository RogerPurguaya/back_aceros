# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class account_move(models.Model):
	_inherit = 'account.move'

	means_payment_it = fields.Many2one('einvoice.means.payment','Medio de Pago')
	fecha_contable = fields.Date('Fecha Contable')

	fecha_modify_ple = fields.Date('Fecha para PLE Diario')
	ple_diariomayor = fields.Selection([('1','FECHA DEL COMPROBANTE CORRESPONDE AL PERIODO'),('8', 'CORRESPONDE A UN PERIODO ANTERIOR Y NO HA SIDO ANOTADO EN DICHO PERIODO'), ('9', 'CORRESPONDE A UN PERIODO ANTERIOR Y SI HA SIDO ANOTADO EN DICHO PERIODO')], 'PLE Diario y Mayor',default="1" )

	fecha_modify_ple_compra = fields.Date('Fecha para PLE Compra')
	ple_compra = fields.Selection([('0', 'ANOTACION OPTATIVAS SIN EFECTO EN EL IGV'), ('1', 'FECHA DEL DOCUMENTO CORRESPONDE AL PERIODO EN QUE SE ANOTO'), ('6', 'FECHA DE EMISION ES ANTERIOR AL PERIODO DE ANOTACION, DENTRO DE LOS 12 MESES'), ('7','FECHA DE EMISION ES ANTERIOR AL PERIODO DE ANOTACION, LUEGO DE LOS 12 MESES'),('9','ES AJUSTE O RECTIFICACION')], 'PLE Compras',default="1")

	fecha_modify_ple_venta = fields.Date('Fecha para PLE Venta')
	ple_venta = fields.Selection([('0', 'ANOTACION OPTATIVA SIN EFECTO EN EL IGV'), ('1', 'FECHA DEL COMPROBANTE CORRESPONDE AL PERIODO'), ('2', 'DOCUMENTO ANULADO'), ('8', 'CORRESPONDE A UN PERIODO ANTERIOR'), ('9', 'SE ESTA CORRIGIENDO UNA ANOTACION DEL PERIODO ANTERIOR')], 'PLE Ventas',default="1")
	
			
	fecha_special = fields.Boolean('Apertura/Cierre',default=False)	
				

	rendicion_id = fields.Many2one('account.rendicion.it','Rendicion',compute="get_rendicion_id",inverse="set_rendicion_id",store=True)
	check_rendicion_rel = fields.Boolean('Check',related='journal_id.check_rendicion')

	es_editable = fields.Boolean('Es editable',related='journal_id.editar_nombre_asiento')


	@api.one
	def set_rendicion_id(self):

		param = self.env['main.parameter'].search([])[0]
		for i in self.line_ids:
			if i.account_id.id in (param.deliver_account_me.id,param.deliver_account_mn.id):
				i.rendicion_id = self.rendicion_id.id

	@api.one
	def get_rendicion_id(self):
		t = False
		for i in self.line_ids:
			if i.rendicion_id.id:
				t = i.rendicion_id.id
		self.rendicion_id = t


	@api.onchange('date')
	def onchange_date(self):
		self.fecha_contable = self.date


	@api.model
	def create(self,vals):

		t = super(account_move,self).create(vals)

		if not t.fecha_contable:
			t.fecha_contable = t.date

		if t.journal_id.asentar_automatic:
			#t.post()
			pass
		t.write({'rendicion_id':t.rendicion_id.id})
		return t

	@api.one
	def change_name(self):
		self.name = '/'

	@api.multi
	def assert_balanced(self):
		for i in self:
			if i.state == 'draft':
				pass
			else:
				super(account_move,i).assert_balanced()
				

	@api.one
	def write(self,vals):
		rendicion = self.rendicion_id.id
		if 'rendicion_id' in vals:
			rendicion = vals['rendicion_id']
		vals['rendicion_id'] = rendicion
		t = super(account_move,self).write(vals)
		self.refresh()
		self.assert_balanced()
		self.env.cr.execute('UPDATE account_invoice SET move_name=%s WHERE move_id=%s',
					   (self.name, self.id))

		self.env.cr.execute("""UPDATE account_payment SET move_name=%s WHERE id in (
							select distinct ap.id from account_payment ap
inner join account_move_line aml on aml.payment_id = ap.id
inner join account_move am on am.id = aml.move_id
where am.id = %s)""",  (self.name, self.id))

		return t

class account_move_line(models.Model):
	_inherit = 'account.move.line'

	tax_amount = fields.Float('Importe impuestos/base',digits=(12,2))

	nro_comprobante = fields.Char('Nro. Comprobante')
	type_document_it = fields.Many2one('einvoice.catalog.01','Tipo de Documento')
	sequence = fields.Integer(help='Used to order Journals in the dashboard view', default=10)
	rendicion_id = fields.Many2one('account.rendicion.it','Rendicion')
	cuo_ple = fields.Char('CUO PLE')
	invoice_line_id = fields.Many2one('account.invoice.line','Linea Factura',copy=False)
	location_id = fields.Many2one('stock.location','Almacen')


	tc = fields.Float('T.C.',digits=(12,3))

	@api.multi
	def prepare_move_lines_for_reconciliation_widget(self, target_currency=False, target_date=False):
		""" Returns move lines formatted for the manual/bank reconciliation widget

			:param target_currency: currency (browse_record or ID) you want the move line debit/credit converted into
			:param target_date: date to use for the monetary conversion
		"""
		t = super(account_move_line,self).prepare_move_lines_for_reconciliation_widget(target_currency,target_date)
		for i in range(len(t)):
			lineas = self.env['account.move.line'].browse(t[i]['id'])
			t[i]['nro_comprobante']= lineas.nro_comprobante
			t[i]['type_document_it']= lineas.type_document_it.code
		return t




		
class account_chart_template(models.Model):
	_inherit = 'account.chart.template'

	code_sunat = fields.Char('Codigo Sunat',size=10)






class product_product(models.Model):
	_inherit = "product.product"

	@api.model
	def _convert_prepared_anglosaxon_line(self, line, partner):
		t = super(product_product,self)._convert_prepared_anglosaxon_line(line,partner)
		linea = line.get('invl_id',False)
		t['invoice_line_id'] = linea
		if linea:
			inv_id = self.env['account.invoice.line'].browse(linea)
			t['location_id'] = inv_id.location_id.id

		return t





class account_journal(models.Model):
	_inherit = 'account.journal'

	editar_nombre_asiento = fields.Boolean('Editar Asiento')
