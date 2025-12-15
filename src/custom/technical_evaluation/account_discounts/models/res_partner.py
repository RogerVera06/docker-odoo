from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    #Fields
    customer_type_id = fields.Many2one(
        'account.discount',
        string='Customer type',
        help='Customer type: This may add discounts based on the customer type'
        )