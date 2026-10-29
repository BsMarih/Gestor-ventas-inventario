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


class EditElementTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Comida", slug="comida")
        self.product_type = Type.objects.create(
            name="Carne",
            slug="comida-carne",
            category=self.category,
        )
        self.element = Element.objects.create(
            name="Bife",
            slug="bife",
            category=self.category,
            type=self.product_type,
        )

    def test_edit_page_loads_existing_product_and_type_values(self):
        response = self.client.get(
            reverse("edit_product", args=[self.element.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"]["category"].value(), "Comida")
        self.assertEqual(response.context["form"]["type"].value(), "Carne")

    def test_post_updates_product_and_category_type_relationship(self):
        response = self.client.post(
            reverse("edit_product", args=[self.element.pk]),
            {
                "name": "Jugo",
                "description": "Jugo natural",
                "content": "1 litro",
                "price": "25",
                "quantity": "8",
                "min_quantity": "2",
                "available": "on",
                "category": "Bebidas",
                "type": "Jugo natural",
                "distributor": "",
                "prod_website": "",
            },
        )

        self.assertRedirects(response, reverse("inventory"))
        self.element.refresh_from_db()
        self.assertEqual(self.element.name, "Jugo")
        self.assertEqual(self.element.category.name, "Bebidas")
        self.assertEqual(self.element.type.name, "Jugo natural")
        self.assertEqual(self.element.type.category, self.element.category)
        self.assertEqual(self.element.price, 25)
        self.assertEqual(self.element.quantity, 8)

    def test_invalid_edit_keeps_product_and_renders_errors(self):
        response = self.client.post(
            reverse("edit_product", args=[self.element.pk]),
            {
                "name": "Bife",
                "price": "-1",
                "quantity": "5",
                "min_quantity": "1",
                "category": "Comida",
                "type": "Carne",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.element.refresh_from_db()
        self.assertEqual(self.element.price, 0)

    def test_delete_action_removes_product_and_redirects_to_inventory(self):
        response = self.client.post(
            reverse("edit_product", args=[self.element.pk]),
            {"action": "delete"},
        )

        self.assertRedirects(response, reverse("inventory"))
        self.assertFalse(Element.objects.filter(pk=self.element.pk).exists())


class PrioritizedProductPreviewTests(TestCase):
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
                    name=f"Prioridad {quantity}",
                    slug=f"prioridad-{quantity}",
                    quantity=quantity,
                    min_quantity=6,
                    category=category,
                    type=product_type,
                )
                for quantity in range(7)
            ]
            + [
                Element(
                    name="Stock suficiente",
                    slug="stock-suficiente",
                    quantity=8,
                    min_quantity=6,
                    category=category,
                    type=product_type,
                )
            ]
        )

    def test_index_shows_at_most_five_most_urgent_products(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        products = response.context["prioritized_products"]
        self.assertEqual(len(products), 5)
        self.assertEqual(
            [product.name for product in products],
            [f"Prioridad {quantity}" for quantity in range(5)],
        )
        self.assertNotContains(response, "Stock suficiente")

    def test_index_shows_empty_message_when_no_products_need_restocking(self):
        Element.objects.filter(quantity__lte=6).delete()

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["prioritized_products"]), 0)
        self.assertContains(
            response,
            "No hay productos que cumplan con el criterio de cantidad mínima.",
        )
