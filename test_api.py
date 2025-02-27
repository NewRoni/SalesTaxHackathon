import requests

URL = "http://127.0.0.1:5000"
response = requests.post(f"{URL}/inference", data={"state": "connecticut",
                                                   "price": "100",
                                                   "quantity": "2",
                                                   "product_type": "digital"})
print(response.content)