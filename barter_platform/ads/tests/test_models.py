from django.test import TestCase
from django.contrib.auth import get_user_model
from ads.models import Ad, Category, Condition, ExchangeProposal

User = get_user_model()

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass123")
        self.category = Category.objects.create(name="Books")
        self.condition = Condition.objects.create(name="New")

    def test_create_ad(self):
        ad = Ad.objects.create(
            user=self.user,
            title="Test Ad",
            description="A test description",
            image_url="http://example.com/image.jpg",
            category=self.category,
            condition=self.condition,
        )
        self.assertEqual(ad.title, "Test Ad")
        self.assertEqual(ad.user, self.user)
        self.assertEqual(ad.category.name, "Books")
        self.assertEqual(ad.condition.name, "New")

class ExchangeProposalModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="pass123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="pass123")

        self.category = Category.objects.create(name="Tech")
        self.condition = Condition.objects.create(name="Used")

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title="Phone",
            description="Used phone",
            image_url="http://example.com/phone.jpg",
            category=self.category,
            condition=self.condition
        )

        self.ad2 = Ad.objects.create(
            user=self.user2,
            title="Headphones",
            description="Almost new",
            image_url="http://example.com/headphones.jpg",
            category=self.category,
            condition=self.condition
        )

    def test_create_exchange_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment="Let's trade!",
            status="pending"
        )

        self.assertEqual(proposal.ad_sender, self.ad1)
        self.assertEqual(proposal.ad_receiver, self.ad2)
        self.assertEqual(proposal.status, "pending")
        self.assertEqual(proposal.comment, "Let's trade!")
        
