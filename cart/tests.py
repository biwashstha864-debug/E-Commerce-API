from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from products.models import Product, Category
from cart.models import Cart, CartItem


class CartTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123"
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

        self.client.force_authenticate(
            user=self.user
        )

    def test_add_product_to_cart(self):

        response = self.client.post(
            "/api/cart/items/",
            {
                "product": self.product.id,
                "quantity": 2
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertEqual(
            response.data["quantity"],
            2
        )

    def test_cannot_add_more_than_stock(self):

        response = self.client.post(
            "/api/cart/items/",
            {
                "product": self.product.id,
                "quantity": 20
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_user_cannot_modify_other_users_cart(self):

        other_user = get_user_model().objects.create_user(
            email="other@test.com",
            password="password123"
        )

        other_cart = Cart.objects.create(
            user=other_user
        )

        cart_item = CartItem.objects.create(
            cart=other_cart,
            product=self.product,
            quantity=1
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            f"/api/cart/items/{cart_item.id}/",
            {
                "quantity": 5
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            404
        )