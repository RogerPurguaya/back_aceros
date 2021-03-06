# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 - 2014 Agile Business Group sagl
#    (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Account Move Template",
    'version': '9.0.1.0.0',
    'category': 'Generic Modules/Accounting',
    'summary': "Templates for recurring Journal Entries",
    'author': "ITGRUPO-COMPATIBLE-BO",
    'website': 'http://www.agilebg.com , http://www.auriumtechnologies.com',
    'license': 'AGPL-3',
    'depends': ['account_accountant', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'view/move_template.xml',
        'wizard/select_template.xml',
    ],
    'test': [
        'test/generate_move.yml',
    ],
   
    'installable': True,
}
