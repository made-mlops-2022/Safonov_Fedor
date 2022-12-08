import unittest
import requests


FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal", "id"]

DATA = [[69.0, 1.0, 0.0, 140.0, 239.0, 1.0, 2.0,
        151.0, 0.0, 1.8, 2.0, 0.0, 1.0, 6.0],
       [71.0, 0.5, 0.0, 145.0, 200.0, 1.0, 2.0,
        151.0, 0.0, 1.8, 2.0, 0.0, 1.0, 8.0]]


class TestInferenceModelServer(unittest.TestCase):

    def setUp(self):
        host = "localhost"
        port = "8000"
        self.url = f"http://{host}:{port}"

    def test_initialize(self):
        response = requests.get(self.url + "/model")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "[OK]: Model initialized")

    def test_query_pred(self):
        response = requests.get(
            self.url + "/predict/",
            json={"data": DATA, "features": FEATURES}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_root(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Model online inference")



if __name__ == "__main__":
    unittest.main()