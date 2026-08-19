from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from products.models import Product
from orders.models import Order
from products.models import Category

class OrderTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123"
        )

        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="password123",
            is_staff=True
        )
        
        self.category = Category.objects.create(
            name="Electronics"
    )

        self.product = Product.objects.create(
            name="Laptop",
            description="Test laptop",
            price=100000,
            stock=10,
            category=self.category
        )
        
    def test_user_can_see_own_orders(self):
        order = Order.objects.create(
            user=self.user,
            total_price=100000
        )

        other_user = get_user_model().objects.create_user(
            email="other@test.com",
            password="password123"
        )

        Order.objects.create(
            user=other_user,
            total_price=50000
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            1
        )
        
        def test_admin_can_see_all_orders(self):

            other_user = get_user_model().objects.create_user(
                email="other@test.com",
                password="password123"
            )

            Order.objects.create(
                user=self.user,
                total_price=100000
            )

            Order.objects.create(
                user=other_user,
                total_price=50000
            )

            self.client.force_authenticate(
                user=self.admin
            )

            response = self.client.get(
                "/api/orders/"
            )

            self.assertEqual(
                response.status_code,
                200
            )

            self.assertEqual(
                len(response.data),
                2
            )
            
    def test_user_can_cancel_pending_order(self):

        order = Order.objects.create(
            user=self.user,
            total_price=100000,
            status=Order.Status.PENDING
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            f"/api/orders/{order.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            Order.Status.CANCELED
        )
        
    def test_cannot_cancel_shipped_order(self):

        order = Order.objects.create(
            user=self.user,
            total_price=100000,
            status=Order.Status.SHIPPED
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            f"/api/orders/{order.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            400
        )
        
    def test_unauthenticated_user_cannot_see_orders(self):

        response = self.client.get(
            "/api/orders/"
        )

        self.assertEqual(
            response.status_code,
            401
        )