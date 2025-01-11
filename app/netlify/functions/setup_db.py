from fauna_config import setup_database

def handler(event, context):
    try:
        setup_database()
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Database setup completed successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 