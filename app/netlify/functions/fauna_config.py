from faunadb import query as q
from faunadb.client import FaunaClient

# Chave direta do FaunaDB
FAUNA_SECRET_KEY = "419824314391461952"

def get_client():
    return FaunaClient(secret=FAUNA_SECRET_KEY)

# Schemas das coleções
TRACKING_COLLECTION = 'tracking'
VISITS_COLLECTION = 'visits'

# Índices necessários
INDEXES = {
    'all_tracking': {
        'name': 'all_tracking',
        'source': TRACKING_COLLECTION
    }
} 