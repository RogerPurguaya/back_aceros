# -*- encoding: utf-8 -*-
from openerp.osv import osv
import base64
from openerp import models, fields, api , exceptions, _

class account_payment(models.Model):
	_inherit='account.payment'

	small_cash = fields.Many2one('small.cash.another','Caja Chica', readonly=True, domain=[('state','=','done'),], states={'draft':[('readonly',False)]} )
	hide_small = fields.Boolean('Oculto',related='journal_id.is_small_cash')

	@api.one
	def write(self,vals):
		t = super(account_payment,self).write(vals)
		if len(self.move_line_ids) >0:
			for i in self.move_line_ids[0].move_id.line_ids:
				if i.account_id.id == self.journal_id.default_debit_account_id.id:
					i.small_cash_id = self.small_cash.id if self.journal_id.is_small_cash else False
					i.move_id.small_cash_id = self.small_cash.id if self.journal_id.is_small_cash else False
		return t

	@api.multi
	def post(self):
		for inv in self:
			res = super(account_payment,inv).post()
			inv.refresh()

			for i in inv.move_line_ids[0].move_id.line_ids:
				if i.account_id.id == self.journal_id.default_debit_account_id.id:
					i.small_cash_id = self.small_cash.id if self.journal_id.is_small_cash else False
					i.move_id.small_cash_id = self.small_cash.id if self.journal_id.is_small_cash else False

