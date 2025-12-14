from odoo import models, fields,api,_

class AccountMove(models.Model):
    _inherit = "account.move"

    customer_type_id = fields.Many2one(
        'account.discount',
        string='Customer type',
        related='partner_id.customer_type_id'
        )
    
    def action_post(self):
        for move in self:
            if move.move_type == 'out_invoice':
                for line in move.invoice_line_ids:
                    line.discount = move.customer_type_id.percentage
        
        return super(AccountMove, self).action_post()