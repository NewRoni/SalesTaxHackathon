import requests

URL = "http://127.0.0.1:5000"
response = requests.post(f"{URL}/tax_inference", data={"state": "connecticut",
                                                   "price": "100",
                                                   "quantity": "2",
                                                   "product_type": "digital"})


response2 = requests.post(f"{URL}/text_inference", data={"product_name": "Nike sneakers"})

response3 = requests.post(f"{URL}/save_calculation", data={"itemName": "Mercedes Car",
                                                           "price": 4000.0,
                                                           "quantity": 3,
                                                            "product_type": "Automobile",
                                                            "state": "New York",
                                                            "tax_paid": 10.5})
print(f"Tax: {response.content.decode()}")
print(f"Product category: {response2.content.decode()}")
print(f"Saved calculation: {response3.text}") # database response message