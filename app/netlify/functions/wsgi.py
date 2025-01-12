from api import app
import json

def handler(event, context):
    # Log do evento para debug
    print("Evento recebido:", json.dumps(event))
    
    # Tratamento de CORS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': ''
        }

    try:
        # Extrair informações da requisição
        path = event.get('path', '').replace('/api/', '/')
        method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        body = event.get('body', '')

        # Criar contexto Flask
        context = app.test_request_context(
            path=path,
            method=method,
            headers=headers,
            data=body
        )

        with context:
            # Processar a requisição
            response = app.full_dispatch_request()
            
            return {
                'statusCode': response.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': response.get_data(as_text=True)
            }

    except Exception as e:
        print("Erro no handler:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        } 