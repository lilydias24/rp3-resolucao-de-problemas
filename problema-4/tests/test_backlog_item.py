import requests

# Configuração
API_URL = "http://localhost:8000"
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUyNTQwNjExfQ.cPZKO__c7IGvuFzaYJMpA3bLE_eX5rs5vq-F_FQomt4'
}

print("=== TESTE DE CRIAÇÃO DE ITEM DE BACKLOG ===")

# Testar criação de item no backlog ID 1 (produto 6)
print("\n1. TESTANDO CRIAÇÃO DE ITEM NO BACKLOG 1:")
backlog_id = 1

# Obter informações do backlog
resp = requests.get(f"{API_URL}/products/backlogs/{backlog_id}", headers=headers)
if resp.status_code == 200:
    backlog = resp.json()
    product_id = backlog["product_id"]
    print(f"Backlog '{backlog['name']}' pertence ao produto ID: {product_id}")
    
    # Listar épicos do produto
    resp_epics = requests.get(f"{API_URL}/products/{product_id}/epics", headers=headers)
    if resp_epics.status_code == 200:
        epics = resp_epics.json()
        print(f"Épicos encontrados: {len(epics)}")
        
        # Listar histórias
        stories = []
        for epic in epics:
            resp_stories = requests.get(f"{API_URL}/products/{epic['epic_id']}/stories", headers=headers)
            if resp_stories.status_code == 200:
                epic_stories = resp_stories.json()
                stories.extend(epic_stories)
                print(f"Épico {epic['epic_id']}: {len(epic_stories)} histórias")
        
        if stories:
            print(f"\nTotal de histórias: {len(stories)}")
            print("Primeiras 3 histórias:")
            for i, story in enumerate(stories[:3]):
                print(f"  {i+1}. ID: {story['story_id']} | {story['as_a']} | {story['i_want']}")
            
            # Tentar criar item de backlog
            story_id = stories[0]['story_id']
            data = {
                "backlog_id": int(backlog_id),
                "story_id": int(story_id),
                "position": 1
            }
            
            print(f"\n2. CRIANDO ITEM DE BACKLOG:")
            print(f"Dados: {data}")
            
            resp_create = requests.post(f"{API_URL}/products/backlogs/{backlog_id}/items", json=data, headers=headers)
            print(f"Status: {resp_create.status_code}")
            print(f"Response: {resp_create.text}")
        else:
            print("Nenhuma história encontrada")
    else:
        print(f"Erro ao listar épicos: {resp_epics.status_code}")
else:
    print(f"Erro ao obter backlog: {resp.status_code}")

# Testar criação de item no backlog ID 4 (produto 7)
print("\n3. TESTANDO CRIAÇÃO DE ITEM NO BACKLOG 4:")
backlog_id = 4

# Obter informações do backlog
resp = requests.get(f"{API_URL}/products/backlogs/{backlog_id}", headers=headers)
if resp.status_code == 200:
    backlog = resp.json()
    product_id = backlog["product_id"]
    print(f"Backlog '{backlog['name']}' pertence ao produto ID: {product_id}")
    
    # Listar épicos do produto
    resp_epics = requests.get(f"{API_URL}/products/{product_id}/epics", headers=headers)
    if resp_epics.status_code == 200:
        epics = resp_epics.json()
        print(f"Épicos encontrados: {len(epics)}")
        
        # Listar histórias
        stories = []
        for epic in epics:
            resp_stories = requests.get(f"{API_URL}/products/{epic['epic_id']}/stories", headers=headers)
            if resp_stories.status_code == 200:
                epic_stories = resp_stories.json()
                stories.extend(epic_stories)
                print(f"Épico {epic['epic_id']}: {len(epic_stories)} histórias")
        
        if stories:
            print(f"Total de histórias: {len(stories)}")
        else:
            print("Nenhuma história encontrada - este é o problema!")
    else:
        print(f"Erro ao listar épicos: {resp_epics.status_code}")
else:
    print(f"Erro ao obter backlog: {resp.status_code}") 