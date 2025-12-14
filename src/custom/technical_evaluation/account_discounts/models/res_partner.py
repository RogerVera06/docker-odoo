from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_type_id = fields.Many2one(
        'account.discount',
        string='Customer type',
        )