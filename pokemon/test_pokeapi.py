import requests

url = "https://pokeapi.co/api/v2/pokemon/pikachu"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()
    print("¡Conexión exitosa!")
    print(f"Nombre: {datos['name']}")
    print(f"Altura: {datos['height']}")
else:
    print("Error al conectar con la API")