# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
import base64
import sys
from odoo.exceptions import UserError
import pprint
from odoo.exceptions import ValidationError

class product_product(models.Model):
	_inherit = 'product.product'

	@api.multi
	def actualizar_costo_promedio(self):

		for p_i in self.env['product.product'].search([]):
			s_prod = [-1,-1,-1]
			s_loca = [-1,-1,-1]
			productos='{0,'
			almacenes='{0,'
			
			lst_products  = self.env['product.product'].browse(p_i.id)

			for producto in lst_products:
				productos=productos+str(producto.id)+','
				s_prod.append(producto.id)
			productos=productos[:-1]+'}'

			lst_locations  = self.env['stock.location'].search([('usage','in',('internal','inventory','transit','procurement','production'))])

			for location in lst_locations:
				almacenes=almacenes+str(location.id)+','
				s_loca.append(location.id)
			almacenes=almacenes[:-1]+'}'

			param = self.env['main.parameter'].search([])
			date_ini= str(param.fiscalyear) + '-01-01'
			date_fin= str(param.fiscalyear) + '-12-31'


			self.env.cr.execute(""" 
				 select 
				CASE WHEN coalesce(sum(ingreso),0) != 0 THEN coalesce(sum(coalesce(debit)),0) / coalesce(sum(coalesce(ingreso,0)),0) else 0 end as pu
				from get_kardex_v("""+ str(date_ini).replace('-','') + "," + str(date_fin).replace('-','') + ",'" + productos + """'::INT[], '""" + almacenes + """'::INT[]) 
			""")
			valor = 0
			for inte in self.env.cr.fetchall():
				valor = inte[0]

			p_i.standard_price = valor              
			#m.product_id.unidad_kardex = producto_uom_r


class stock_picking(models.Model):
	_inherit = 'stock.picking'
 
	@api.multi
	def do_transfer(self):

		t = super(stock_picking,self).do_transfer()

		

		currency_obj = self.env['res.currency'].search([('name','=','USD')])
		if len(currency_obj)>0:
			currency_obj = currency_obj[0]
		else:
			raise UserError( 'Error!\nNo existe la moneda USD' )

		fecha = self.fecha_kardex
		tipo_cambio = self.env['res.currency.rate'].search([('name','=',fecha),('currency_id','=',currency_obj.id)])

		if len(tipo_cambio)>0:
			tipo_cambio = tipo_cambio[0]
		else:
			raise UserError( 'Error!\nNo existe el tipo de cambio para la fecha: '+ str(fecha) )        
		
		
		for m in self.move_lines:
			#if m.location_id.usage == 'supplier' and m.location_dest_id.usage == 'internal':
			if True:


				producto_uom_r = m.product_id.unidad_kardex.id
				m.product_id.unidad_kardex = False

				s_prod = [-1,-1,-1]
				s_loca = [-1,-1,-1]
				productos='{0,'
				almacenes='{0,'
				
				lst_products  = self.env['product.product'].search([('id','=',m.product_id.id )])

				for producto in lst_products:
					productos=productos+str(producto.id)+','
					s_prod.append(producto.id)
				productos=productos[:-1]+'}'

				lst_locations  = self.env['stock.location'].search([('usage','in',('internal','inventory','transit','procurement','production'))])

				for location in lst_locations:
					almacenes=almacenes+str(location.id)+','
					s_loca.append(location.id)
				almacenes=almacenes[:-1]+'}'

				import datetime
				fecha_final = self.fecha_kardex
				if not fecha_final:
					fecha_final = str (datetime.datetime.now() )[:10]
				date_ini=fecha_final.split('-')[0] + '-01-01'
				date_fin=fecha_final.split('-')[0] + '-12-31'


				self.env.cr.execute(""" 
					 select 
					CASE WHEN coalesce(sum(ingreso),0) != 0 THEN coalesce(sum(debit),0) / coalesce(sum(ingreso),0) else 0 end as pu
					from get_kardex_v("""+ str(date_ini).replace('-','') + "," + str(date_fin).replace('-','') + ",'" + productos + """'::INT[], '""" + almacenes + """'::INT[]) 
				""")
				valor = 0
				for inte in self.env.cr.fetchall():
					valor = inte[0]

				m.product_id.standard_price = valor              
				#m.product_id.unidad_kardex = producto_uom_r

		return t

	@api.multi
	def action_revert_done(self):
		t = super(stock_picking,self).action_revert_done()
		for m in self.move_lines:
			#if m.location_id.usage == 'supplier' and m.location_dest_id.usage == 'internal':
			if True:

				producto_uom_r = m.product_id.unidad_kardex.id
				m.product_id.unidad_kardex = False

				s_prod = [-1,-1,-1]
				s_loca = [-1,-1,-1]
				productos='{0,'
				almacenes='{0,'
				
				lst_products  = self.env['product.product'].search([('id','=',m.product_id.id )])

				for producto in lst_products:
					productos=productos+str(producto.id)+','
					s_prod.append(producto.id)
				productos=productos[:-1]+'}'

				lst_locations  = self.env['stock.location'].search([('usage','in',('internal','inventory','transit','procurement','production'))])

				for location in lst_locations:
					almacenes=almacenes+str(location.id)+','
					s_loca.append(location.id)
				almacenes=almacenes[:-1]+'}'

				import datetime
				fecha_final = self.fecha_kardex
				if not fecha_final:
					fecha_final = str (datetime.datetime.now() )[:10]
				date_ini=fecha_final.split('-')[0] + '-01-01'
				date_fin=fecha_final.split('-')[0] + '-12-31'


				self.env.cr.execute(""" 
					 select 
					 CASE WHEN coalesce(sum(ingreso),0) != 0 THEN coalesce(sum(debit),0) / coalesce(sum(ingreso),0) else 0 end as pu
					from get_kardex_v("""+ str(date_ini).replace('-','') + "," + str(date_fin).replace('-','') + ",'" + productos + """'::INT[], '""" + almacenes + """'::INT[]) 
				""")
				valor = 0
				for inte in self.env.cr.fetchall():
					valor = inte[0]

				m.product_id.standard_price = valor
				#m.product_id.unidad_kardex = producto_uom_r

		return t
		
class gastos_vinculados_it(models.Model):
	_inherit = 'gastos.vinculados.it'
	
	@api.one
	def procesar(self):
		t = super(gastos_vinculados_it,self).procesar()

		for m in self.detalle_ids:
			if True:


				producto_uom_r = m.producto_rel.unidad_kardex.id
				m.producto_rel.unidad_kardex = False

				s_prod = [-1,-1,-1]
				s_loca = [-1,-1,-1]
				productos='{0,'
				almacenes='{0,'
				
				lst_products  = self.env['product.product'].search([('id','=',m.stock_move_id.product_id.id )])

				for producto in lst_products:
					productos=productos+str(producto.id)+','
					s_prod.append(producto.id)
				productos=productos[:-1]+'}'

				lst_locations  = self.env['stock.location'].search([('usage','in',('internal','inventory','transit','procurement','production'))])

				for location in lst_locations:
					almacenes=almacenes+str(location.id)+','
					s_loca.append(location.id)
				almacenes=almacenes[:-1]+'}'

				import datetime
				fecha_final = self.date_invoice if self.tomar_valor == 'factura' else self.date_purchase
				if not fecha_final:
					fecha_final = str (datetime.datetime.now() )[:10]
				date_ini=fecha_final.split('-')[0] + '-01-01'
				date_fin=fecha_final.split('-')[0] + '-12-31'


				self.env.cr.execute(""" 
					 select 
					 CASE WHEN coalesce(sum(ingreso),0) != 0 THEN coalesce(sum(debit),0) / coalesce(sum(ingreso),0) else 0 end as pu
					from get_kardex_v("""+ str(date_ini).replace('-','') + "," + str(date_fin).replace('-','') + ",'" + productos + """'::INT[], '""" + almacenes + """'::INT[]) 
				""")
				valor = 0
				for inte in self.env.cr.fetchall():
					valor = inte[0]

				m.producto_rel.standard_price = valor              
				#m.product_id.unidad_kardex = producto_uom_r

		return t
	
	@api.one
	def borrador(self):
		t = super(gastos_vinculados_it,self).borrador()

		for m in self.detalle_ids:
			if True:


				producto_uom_r = m.producto_rel.unidad_kardex.id
				m.producto_rel.unidad_kardex = False

				s_prod = [-1,-1,-1]
				s_loca = [-1,-1,-1]
				productos='{0,'
				almacenes='{0,'
				
				lst_products  = self.env['product.product'].search([('id','=',m.stock_move_id.product_id.id )])

				for producto in lst_products:
					productos=productos+str(producto.id)+','
					s_prod.append(producto.id)
				productos=productos[:-1]+'}'

				lst_locations  = self.env['stock.location'].search([('usage','in',('internal','inventory','transit','procurement','production'))])

				for location in lst_locations:
					almacenes=almacenes+str(location.id)+','
					s_loca.append(location.id)
				almacenes=almacenes[:-1]+'}'

				import datetime
				fecha_final = self.date_invoice if self.tomar_valor == 'factura' else self.date_purchase
				if not fecha_final:
					fecha_final = str (datetime.datetime.now() )[:10]
				date_ini=fecha_final.split('-')[0] + '-01-01'
				date_fin=fecha_final.split('-')[0] + '-12-31'


				self.env.cr.execute(""" 
					 select 
					 CASE WHEN coalesce(sum(ingreso),0) != 0 THEN coalesce(sum(debit),0) / coalesce(sum(ingreso),0) else 0 end as pu
					from get_kardex_v("""+ str(date_ini).replace('-','') + "," + str(date_fin).replace('-','') + ",'" + productos + """'::INT[], '""" + almacenes + """'::INT[]) 
				""")
				valor = 0
				for inte in self.env.cr.fetchall():
					valor = inte[0]

				m.producto_rel.standard_price = valor              
				#m.product_id.unidad_kardex = producto_uom_r

		return t