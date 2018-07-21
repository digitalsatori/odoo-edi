"""EDI product tutorial tests"""

from .common import EdiProductCase


class TestTutorial(EdiProductCase):
    """EDI product tutorial tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doc_type_tutorial = cls.env.ref(
            'edi_product.tutorial_document_type'
        )
        cls.units = cls.env.ref('product.product_uom_unit')
        cls.dozens = cls.env.ref('product.product_uom_dozen')
        cls.dozens.name = "Dozen(s)"

    @classmethod
    def create_tutorial(cls, *filenames):
        """Create product tutorial document"""
        return cls.create_input_document(cls.doc_type_tutorial, *filenames)

    def test01_basic(self):
        """Basic document execution"""
        doc = self.create_tutorial('books01.csv')
        self.assertTrue(doc.action_execute())
        products = doc.mapped('product_tutorial_ids.product_id')
        self.assertEqual(len(products), 3)
        products_by_code = {x.default_code: x for x in products}
        self.assertEqual(products_by_code['9780552146166'].uom_id, self.dozens)
        self.assertEqual(products_by_code['9780552145428'].name, "Hogfather")
        doc = self.create_tutorial('fruit01.csv')
        self.assertTrue(doc.action_execute())
        products = doc.mapped('product_tutorial_ids.product_id')
        self.assertEqual(len(products), 3)

    def test02_identical(self):
        """Document and subsequent identical document"""
        doc1 = self.create_tutorial('books01.csv')
        self.assertTrue(doc1.action_execute())
        self.assertEqual(len(doc1.product_tutorial_ids), 3)
        doc2 = self.create_tutorial('books01.csv')
        self.assertTrue(doc2.action_execute())
        self.assertEqual(len(doc2.product_tutorial_ids), 0)

    def test03_correction(self):
        """Document and subsequent corrected document"""
        doc1 = self.create_tutorial('books01.csv')
        self.assertTrue(doc1.action_execute())
        self.assertEqual(len(doc1.product_tutorial_ids), 3)
        doc2 = self.create_tutorial('books02.csv')
        self.assertTrue(doc2.action_execute())
        self.assertEqual(len(doc2.product_tutorial_ids), 1)
        product = doc2.product_tutorial_ids.product_id
        self.assertEqual(product.barcode, '9780552146166')
        self.assertEqual(product.uom_id, self.units)
        self.assertEqual(product.name, "The Fifth Elephant")
