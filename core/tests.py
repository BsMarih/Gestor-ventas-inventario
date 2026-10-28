from django.test import TestCase
from django.urls import reverse

from .models import Category, Element, Type


class CreateElementTypeTests(TestCase):
    def create_element(self, name, category, type_name):
        return self.client.post(
            reverse("create_element"),
            {
                "name": name,
                "category": category,
                "type": type_name,
                "price": "10",
                "quantity": "5",
                "min_quantity": "1",
            },
        )

    def test_new_type_is_created_for_selected_category(self):
        response = self.create_element("Bife", "Comida", "Carne")

        self.assertRedirects(response, reverse("inventory"))
        element = Element.objects.get(name="Bife")
        self.assertEqual(element.category.name, "Comida")
        self.assertEqual(element.type.name, "Carne")
        self.assertEqual(element.type.category, element.category)

    def test_type_names_can_be_reused_in_different_categories(self):
        self.create_element("Bife", "Comida", "Carne")
        self.create_element("Alimento para perro", "Mascotas", "Carne")

        food_type = Type.objects.get(category__name="Comida", name="Carne")
        pet_type = Type.objects.get(category__name="Mascotas", name="Carne")
        self.assertNotEqual(food_type.pk, pet_type.pk)
        self.assertNotEqual(food_type.slug, pet_type.slug)

    def test_get_types_returns_only_types_for_requested_category(self):
        food = Category.objects.create(name="Comida", slug="comida")
        pets = Category.objects.create(name="Mascotas", slug="mascotas")
        Type.objects.create(name="Carne", slug="comida-carne", category=food)
        Type.objects.create(name="Carne", slug="mascotas-carne", category=pets)

        response = self.client.get(reverse("get_types"), {"category": "Comida"})

        self.assertEqual(response.json(), ["Carne"])


class InventoryPaginationTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Comida", slug="comida")
        product_type = Type.objects.create(
            name="Carne",
            slug="comida-carne",
            category=category,
        )
        Element.objects.bulk_create(
            [
                Element(
                    name=f"Producto {number}",
                    slug=f"producto-{number}",
                    category=category,
                    type=product_type,
                )
                for number in range(11)
            ]
        )

    def test_inventory_shows_ten_products_per_page(self):
        response = self.client.get(reverse("inventory"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["elements"]), 10)
        self.assertEqual(response.context["elements"].paginator.num_pages, 2)

    def test_inventory_next_page_shows_remaining_products(self):
        response = self.client.get(reverse("inventory"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["elements"]), 1)
        self.assertEqual(response.context["elements"].number, 2)
        self.assertContains(response, "Anterior")
        self.assertContains(response, "Siguiente")

    def test_invalid_page_number_falls_back_to_first_page(self):
        response = self.client.get(reverse("inventory"), {"page": "no-es-un-numero"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["elements"].number, 1)
