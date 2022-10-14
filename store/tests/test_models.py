from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Django", slug="django")

    def test_category_model_entry(self):
        data = self.category
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'Django')


class TestProductsModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Django", slug="django")
        self.user = User.objects.create(username='admin')
        self.product = Product.objects.create(category=self.category, title='django beginners', created_by=self.user,
                                              slug='django-beginners', price='20.00', image='django')

    def test_product_model_entry(self):
        data = self.product
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')