from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestStockStorageTag(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        #Producto de prueba
        cls.product = cls.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
        })
        
        cls.tag_model = cls.env['stock.storage.tag']

    def test_create_storage_tag_successfully(self):
        #Creacion de etiqueta
        tag = self.tag_model.create({
            'name': 'Fragile',
            'color': '#FF5733',
            'description': 'Handle with care',
        })
        self.assertEqual(tag.name, 'Fragile')
        self.assertEqual(tag.color, '#FF5733')
        self.assertEqual(tag.description, 'Handle with care')

    def test_assign_tag_to_product(self):
        tag = self.tag_model.create({
            'name': 'Perishable',
            'color': '#33FF57',
        })
        
        #Asignacion de etiqueta
        self.product.stock_storage_tag_ids = [(4, tag.id)]
        
        #Debe estar asignada
        self.assertIn(tag, self.product.stock_storage_tag_ids)
        self.assertEqual(len(self.product.stock_storage_tag_ids), 1)