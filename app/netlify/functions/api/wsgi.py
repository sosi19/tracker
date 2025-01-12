from api import app
from flask_serverless import FlaskServerless

handler = FlaskServerless(app)

def handler(event, context):
    print("Evento recebido:", event)  # Log para debug
    
    # Tratamento de CORS para requisições OPTIONS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            }
        }
    
    try:
        # Usar o FlaskServerless para processar a requisição
        result = handler.handle(event, context)
        
        # Garantir que os headers CORS estejam presentes
        if isinstance(result, dict) and 'headers' in result:
            result['headers'].update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            })
        
        return result
    except Exception as e:
        print("Erro no handler:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': '{"success": false, "error": "' + str(e) + '"}'
        } 