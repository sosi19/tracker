from flask import Flask, jsonify
from faunadb import query as q
from fauna_config import get_client, VISITS_COLLECTION

app = Flask(__name__)

@app.route('/test')
def test():
    print("Rota /test acessada")  # Log para debug
    return jsonify({
        'success': True,
        'message': 'API está funcionando'
    })

@app.route('/test-db')
def test_db():
    print("Rota /test-db acessada")  # Log para debug
    try:
        client = get_client()
        result = client.query(
            q.get_collection(VISITS_COLLECTION)
        )
        return jsonify({
            'success': True,
            'message': 'Conexão com FaunaDB estabelecida com sucesso',
            'collection': result['name']
        })
    except Exception as e:
        print("Erro ao conectar com FaunaDB:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 