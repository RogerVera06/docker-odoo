from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestHrPerformanceReview(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        #Empleados
        cls.employee_1 = cls.env['hr.employee'].create({'name': 'Test Employee 1'})
        cls.employee_2 = cls.env['hr.employee'].create({'name': 'Test Employee 2'})
        cls.employee_3 = cls.env['hr.employee'].create({'name': 'Test Reviewer'})

        cls.review_model = cls.env['hr.performance.review']

    def test_create_review_and_link_to_employee(self):
        #Crea la review el empleado 3, el empleado 1 es evaluado
        review = self.review_model.create({
            'employee_id': self.employee_1.id,
            'reviewer_id': self.employee_3.id,
            'score': 8.0,
            'comments': 'Good performance'
        })
        self.assertEqual(review.employee_id, self.employee_1)
        self.assertEqual(review.reviewer_id, self.employee_3)
        self.assertEqual(review.status, 'pending')

    def test_prevent_multiple_pending_reviews(self):
        #Solo sera permitida una review en 'pending' por empleado
        #Primera review
        self.review_model.create({
            'employee_id': self.employee_1.id,
            'reviewer_id': self.employee_3.id,
            'score': 7.0,
        })

        #Segunda review, debe marcar error
        with self.assertRaises(ValidationError):
            self.review_model.create({
                'employee_id': self.employee_1.id,
                'reviewer_id': self.employee_2.id,
                'score': 6.0,
            })

    def test_score_validation(self):
        #El score no puede ser negativo
        with self.assertRaises(ValidationError):
            self.review_model.create({
                'employee_id': self.employee_1.id,
                'reviewer_id': self.employee_3.id,
                'score': -1.0,
            })

        #El score debe ser menor o igual a 10
        with self.assertRaises(ValidationError):
            self.review_model.create({
                'employee_id': self.employee_1.id,
                'reviewer_id': self.employee_3.id,
                'score': 11.0,
            })

        #Cumple con la validacion
        review = self.review_model.create({
            'employee_id': self.employee_1.id,
            'reviewer_id': self.employee_3.id,
            'score': 10.0,
        })
        self.assertEqual(review.score, 10.0)

    def test_only_reviewer_can_complete_review(self):
        #Solo quien hace la review puede completarla
        review = self.review_model.create({
            'employee_id': self.employee_1.id,
            'reviewer_id': self.employee_3.id,
            'score': 8.5,
        })

        #Definimos el usuario como empleado 3
        self.env.user.employee_id = self.employee_3
        #Deberia permitir completar la review
        review.action_complete_review()
        self.assertEqual(review.status, 'completed')

        #Definimos una segunda review
        review2 = self.review_model.create({
        'employee_id': self.employee_1.id,
        'reviewer_id': self.employee_3.id,
        'score': 7.0,
        })
        
        #Definimos el usuario como empleado 2, por lo tanto no deberia permitir completar la review
        self.env.user.employee_id = self.employee_2
        with self.assertRaises(ValidationError):
            review2.action_complete_review()
