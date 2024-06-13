from django.test import TestCase
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Farm, Status

class FarmModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='manager', password='password')
        self.farm = Farm.objects.create(
            name='Green Acres',
            location='123 Farm Lane',
            description='A lovely farm with lots of greenery.',
            slogan='Green is life!',
            status=Status.ACTIVE,
            verified=True
        )
        self.farm.managers.add(self.user)
        self.farm.save()

    def test_farm_creation(self):
        self.assertEqual(self.farm.name, 'Green Acres')
        self.assertEqual(self.farm.slug, slugify(self.farm.name))
        self.assertEqual(self.farm.location, '123 Farm Lane')
        self.assertEqual(self.farm.description, 'A lovely farm with lots of greenery.')
        self.assertEqual(self.farm.slogan, 'Green is life!')
        self.assertEqual(self.farm.status, Status.ACTIVE)
        self.assertTrue(self.farm.verified)
        self.assertEqual(self.farm.managers.first(), self.user)

    def test_farm_email_validation(self):
        with self.assertRaises(ValueError):
            self.farm.email = 'invalid-email'
            self.farm.full_clean()

    def test_farm_phone_validation(self):
        with self.assertRaises(ValueError):
            self.farm.phone = 'invalid-phone'
            self.farm.full_clean()

        valid_phones = ['+1234567890', '1234567890']
        for phone in valid_phones:
            self.farm.phone = phone
            self.farm.full_clean()

    def test_farm_ordering(self):
        farm2 = Farm.objects.create(
            name='Sunny Fields',
            location='456 Farm Road',
            description='A bright and sunny farm.',
        )
        farms = Farm.objects.all()
        self.assertEqual(farms.first(), farm2)

    def test_str_method(self):
        self.assertEqual(str(self.farm), 'Green Acres')

    def test_indexes(self):
        index_fields = [index.fields for index in Farm._meta.indexes]
        self.assertIn(['created'], index_fields)
        self.assertIn(['verified'], index_fields)
        self.assertIn(['name'], index_fields)
