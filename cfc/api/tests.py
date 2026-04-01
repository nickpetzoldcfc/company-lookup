import json
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.test.client import Client

from api.rate_limiter import reset_rate_limiter


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
)
class LookupEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()
        reset_rate_limiter()

    def _post(self, data):
        return self.client.post(
            "/api/lookup",
            data=json.dumps(data),
            content_type="application/json",
        )

    def test_valid_lookup_returns_correct_shape(self):
        resp = self._post({"name": "robinson", "website": "", "postcode": "", "address": ""})
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("name", body)
        self.assertIn("address", body)
        self.assertIn("company_number", body)
        self.assertIn("credit_score", body)
        self.assertIn("domain", body)
        self.assertIn("last_default_date", body)
        self.assertIn("match_confidence", body)
        self.assertIn("trade_lines", body)
        self.assertIn(body["match_confidence"], ["no_match", "low", "medium", "high"])

    def test_valid_lookup_returns_address_shape(self):
        resp = self._post({"name": "robinson"})
        self.assertEqual(resp.status_code, 200)
        address = resp.json()["address"]
        self.assertIn("city", address)
        self.assertIn("postcode", address)
        self.assertIn("street", address)

    def test_no_match_returns_no_match_confidence(self):
        resp = self._post({"name": "xyznonexistentcompany123"})
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["match_confidence"], "no_match")
        self.assertIsNone(body["name"])

    def test_422_empty_body(self):
        resp = self._post({})
        self.assertEqual(resp.status_code, 422)
        body = resp.json()
        self.assertIn("detail", body)

    def test_422_no_name(self):
        resp = self._post({"address": "123 Main St"})
        self.assertEqual(resp.status_code, 422)

    def test_422_blank_name(self):
        resp = self._post({"name": "   "})
        self.assertEqual(resp.status_code, 422)

    def test_500_on_unexpected_error(self):
        with patch("api.views.get_company_lookup", side_effect=RuntimeError("boom")):
            resp = self._post({"name": "robinson"})
        self.assertEqual(resp.status_code, 500)
        body = resp.json()
        self.assertEqual(body["detail"], "Internal server error")

    def test_rate_limiting_returns_429(self):
        for _ in range(10):
            resp = self._post({"name": "robinson"})
            self.assertEqual(resp.status_code, 200)

        resp = self._post({"name": "robinson"})
        self.assertEqual(resp.status_code, 429)
        body = resp.json()
        self.assertIn("Rate limit", body["detail"])

    def test_cached_response_returned(self):
        resp1 = self._post({"name": "robinson"})
        self.assertEqual(resp1.status_code, 200)

        with patch("api.views.get_company_lookup", side_effect=RuntimeError("should not be called")):
            resp2 = self._post({"name": "robinson"})
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp1.json(), resp2.json())
