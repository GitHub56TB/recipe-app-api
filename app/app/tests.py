# Run=> docker-compose run app sh -c "python manage.py test"

from django.test import TestCase

from app.calc import add, subtract


class CalcTestCase(TestCase):

    def test_add_numbers(self):  # Name must began with "test"
        """Test that two numbers are added together"""
        self.assertEqual(add(3, 8), 11)

    def test_subtract_numbers(self):  # Name must began with "test"
        """Test that two numbers are subtracted and returned"""
        self.assertEqual(subtract(5, 11), 6)
