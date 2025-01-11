from faunadb import query as q
from faunadb.client import FaunaClient

# Chave direta do FaunaDB (não é a melhor prática, mas funciona para demonstração)
FAUNA_SECRET_KEY = "419824314391461952"

def get_client():
    return FaunaClient(secret=FAUNA_SECRET_KEY)

# Schemas das coleções
LINKS_COLLECTION = 'links'
VISITS_COLLECTION = 'visits'

# Índices necessários
INDEXES = {
    'all_links': {
        'name': 'all_links',
        'source': LINKS_COLLECTION
    },
    'visits_by_link': {
        'name': 'visits_by_link',
        'source': VISITS_COLLECTION,
        'terms': [{'field': ['data', 'link_id']}]
    }
}

def setup_database():
    client = get_client()
    
    # Criar coleções
    try:
        client.query(q.create_collection({'name': LINKS_COLLECTION}))
        client.query(q.create_collection({'name': VISITS_COLLECTION}))
        print("Coleções criadas com sucesso!")
    except Exception as e:
        print(f"Erro ou coleções já existem: {str(e)}")
    
    # Criar índices
    for index in INDEXES.values():
        try:
            client.query(q.create_index(index))
            print(f"Índice {index['name']} criado com sucesso!")
        except Exception as e:
            print(f"Erro ou índice já existe: {str(e)}") 