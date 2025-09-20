from rest_framework.test import APITestCase


class OfferListUnhappyPathTests(APITestCase):
    def test_offers_wrong_delivery_time_returns_400(self):
        url = '/api/offers/?max_delivery_time="test"'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 400)
        self.assertIn('max_delivery_time', res.data)
