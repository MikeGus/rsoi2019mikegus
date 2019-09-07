import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Sweet
from .serializers import SweetSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_sweet(title, calories=0):
        Sweet.objects.create(title=title, calories=calories)

    def make_request(self, request_type, **kwargs):
        if request_type == "get":
            return self.client.get(
                reverse(
                    "sweet",
                    kwargs={
                        "pk": kwargs["pk"]
                    }
                )
            )
        elif request_type == "post":
            return self.client.post(
                reverse("sweets"),
                data=json.dumps(kwargs["data"]),
                content_type="application/json"
            )
        elif request_type == "put":
            return self.client.put(
                reverse(
                    "sweet",
                    kwargs={
                        "pk": kwargs["pk"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type="application/json"
            )
        elif request_type == "delete":
            return self.client.delete(
                reverse(
                    "sweet",
                    kwargs={
                        "pk": kwargs["pk"]
                    }
                )
            )

    def setUp(self):
        self.create_sweet("Pie", 100)
        self.create_sweet("Chocolate bar", 50)
        self.create_sweet("Chocolate paste", 150)
        self.valid_pk = 1
        self.invalid_pk = 100500


class GetAllSweetsTest(BaseViewTest):
    def test_get_all_sweets(self):
        expected = Sweet.objects.all()
        serialized = SweetSerializer(expected, many=True)

        response = self.client.get(reverse("sweets"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)


class GetSweetTest(BaseViewTest):
    def test_get_sweet_valid_pk(self):
        response = self.make_request("get", pk=self.valid_pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected = Sweet.objects.get(pk=self.valid_pk)
        serialized = SweetSerializer(expected)
        self.assertEqual(response.data, serialized.data)

    def test_get_sweet_invalid_pk(self):
        response = self.make_request("get", pk=self.invalid_pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["msg"],
            "Sweet with id: {:d} does not exist".format(self.invalid_pk)
        )


class CreateSweetTest(BaseViewTest):
    def test_create_sweet_valid(self):
        new_sweet = {
            "title": "soda",
            "calories": 20
        }
        response = self.make_request("post", data=new_sweet)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, new_sweet)

    def test_create_sweet_negative_calories(self):
        new_sweet = {
            "title": "soda",
            "calories": -20
        }

        response = self.make_request("post", data=new_sweet)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["msg"],
            "Calories can't be negative"
        )


class UpdateSweetTest(BaseViewTest):
    def test_update_sweet_valid(self):
        original_sweet = Sweet.objects.get(pk=self.valid_pk)
        original_sweet_serialized = SweetSerializer(original_sweet)
        expected_updated_sweet = {
            "title": "Cherry pie",
            "calories": 1000
        }
        self.assertNotEqual(expected_updated_sweet, original_sweet_serialized.data)

        updated_sweet_response = self.make_request("put", pk=self.valid_pk, data=expected_updated_sweet)
        self.assertEqual(expected_updated_sweet, updated_sweet_response.data)

    def test_update_sweet_invalid_pk(self):
        expected_updated_sweet = {
            "title": "Cherry pie",
            "calories": 1000
        }
        updated_sweet_response = self.make_request("put", pk=self.invalid_pk, data=expected_updated_sweet)
        self.assertEqual(updated_sweet_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            updated_sweet_response.data["msg"],
            "Sweet with id: {:d} does not exist".format(self.invalid_pk)
        )


class DeleteSweetTest(BaseViewTest):
    def test_delete_sweet_valid(self):
        delete_response = self.make_request("delete", pk=self.valid_pk)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        get_response = self.make_request("get", pk=self.valid_pk)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            get_response.data["msg"],
            "Sweet with id: {:d} does not exist".format(self.valid_pk)
        )

    def test_delete_sweet_invalid_pk(self):
        response = self.make_request("delete", pk=self.invalid_pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["msg"],
            "Sweet with id: {:d} does not exist".format(self.invalid_pk)
        )
