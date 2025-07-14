import requests
import json

def test_register():
    url = "http://localhost:8000/auth/register"
    data = {
        "email": "teste@teste.com",
        "name": "Teste",
        "password": "123456"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registro funcionou!")
        else:
            print("❌ Erro no registro")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_register() 