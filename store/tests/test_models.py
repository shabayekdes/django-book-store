from django.test import TestCase

from store.models import Category


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data = Category.objects.create(name="Django", slug="django")

    def test_category_model_entry(self):

        self.assertTrue(isinstance(self.data, Category))
