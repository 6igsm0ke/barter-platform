from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ads.models import Ad, Category, Condition, ExchangeProposal
from django.contrib.auth import get_user_model

User = get_user_model()

class AdViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass123", is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Books")
        self.condition = Condition.objects.create(name="New")

    def test_create_ad(self):
        url = reverse("ads:ad-list")
        data = {
            "title": "Test Phone",
            "description": "Brand new phone",
            # "image_url": "http://example.com/phone.jpg",
            "category": self.category.id,
            "condition": self.condition.id
        }
        response = self.client.post(url, data)
        print(response.data)  
        self.assertEqual(response.status_code, 201)

    def test_list_ads(self):
        Ad.objects.create(
            user=self.user,
            title="Laptop",
            description="Used laptop",
            # image_url="http://example.com/laptop.jpg",
            category=self.category,
            condition=self.condition,
        )
        url = reverse("ads:ad-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)  

class ExchangeProposalViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="pass123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="pass123")
        self.client.force_authenticate(user=self.user1)
        self.category = Category.objects.create(name="Books")
        self.condition = Condition.objects.create(name="Used")
        self.ad1 = Ad.objects.create(user=self.user1, title="Phone", description="Used", category=self.category, condition=self.condition)
        self.ad2 = Ad.objects.create(user=self.user2, title="Headphones", description="New", category=self.category, condition=self.condition)

    def test_create_exchange_proposal(self):
        url = reverse("ads:proposal-list")
        data = {
            "ad_sender": self.ad1.id,
            "ad_receiver": self.ad2.id,
            "comment": "Interested in trading"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "pending")

    def test_list_exchange_proposals(self):
        ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment="Offer", status="pending")
        url = reverse("ads:proposal-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)