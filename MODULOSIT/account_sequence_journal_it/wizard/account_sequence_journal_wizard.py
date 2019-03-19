# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp import models, fields, api


class account_sequence_journal_wizard(osv.TransientModel):
	_name='account.sequence.journal.wizard'
	
	journal_ids =fields.Many2many('account.journal','account_journal_sequence_wizard_rel','sequence_wizard_id','journal_id','Diarios',required=True)
	fiscal_id = fields.Many2one('account.fiscalyear','Año Fiscal',required=True)
	


	@api.multi
	def do_rebuild(self):
		from datetime import datetime, timedelta
		for i in self.journal_ids:
			day = 1
			month = 1
			year = int(self.fiscal_id.name)

			i.sequence_id.use_date_range = True
			i.sequence_id.prefix = '%(month)s-'
			i.sequence_id.padding = 6
			for fech in range(12):
				dia_1 = datetime(day=day,month=month,year=year)
				month+= 1
				if month == 13:
					month= 1
					year+= 1

				dia_2 = datetime(day=day,month=month,year=year) - timedelta(days=1)
				busqueda = self.env['ir.sequence.date_range'].search([('date_from','=',str(dia_1)[:10]),('date_to','=',str(dia_2)[:10]),('sequence_id','=',i.sequence_id.id)])
				if len(busqueda)==0:
					data = {
						'date_from':str(dia_1)[:10],
						'date_to':str(dia_2)[:10],
						'sequence_id':i.sequence_id.id,
						'number_next_actual':1,
					}
					self.env['ir.sequence.date_range'].create(data)


