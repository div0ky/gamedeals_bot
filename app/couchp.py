import requests

response = requests.get("http://192.168.2.10:8081/api/d0ba0bcaf06948168ad121bbe35b715d/movie.add?identifier=tt2404435&force_readd=False")
response = response.json()
print(response.get('success'))
print(response['movie']['releases'][0]['status'])