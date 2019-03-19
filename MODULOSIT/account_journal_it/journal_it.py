# -*- encoding: utf-8 -*-
from openerp.osv import osv
import base64
from openerp import models, fields, api , exceptions, _

class account_journal(models.Model):
	_inherit = 'account.journal'
	
	register_sunat = fields.Selection((('1','Compras'),
									('2','Ventas'),
									('3','Honorarios'),
									('4','Retenciones'),
									('5','Percepciones')								
									),'Registro Sunat')

	asentar_automatic = fields.Boolean('Asentado Automatico')
	check_rendicion = fields.Boolean('Diario de Rendición')
	check_canje_letras = fields.Boolean('Se usa para Canje de Letras')