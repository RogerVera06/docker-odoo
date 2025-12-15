from odoo import models, fields,api,_

class AccountMove(models.Model):
    _inherit = "account.move"

    #Fields
    customer_type_id = fields.Many2one(
        'account.discount',
        string='Customer type',
        related='partner_id.customer_type_id'
        )
    
    def action_post(self):
        for move in self:
            #Verifica que sea factura de cliente y que exista un tipo de cliente
            if move.move_type == 'out_invoice' and move.customer_type_id:
                for line in move.invoice_line_ids:
                    #Agrega el descuento asociado al tipo de cliente
                    line.discount = move.customer_type_id.percentage
        
        #Permite que el flujo
        return super(AccountMove, self).action_post()