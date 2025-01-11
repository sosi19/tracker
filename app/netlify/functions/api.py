from flask import Flask, request, jsonify, redirect
from flask_serverless import FlaskServerless
import json
from datetime import datetime
import requests
from user_agents import parse
from faunadb import query as q
from fauna_config import get_client, TRACKING_COLLECTION, VISITS_COLLECTION

app = Flask(__name__)
handler = FlaskServerless(app)

@app.route('/')
def dashboard():
    client = get_client()
    try:
        result = client.query(
            q.map_(
                lambda x: q.merge(
                    {'id': q.select(['ref', 'id'], x)},
                    q.select(['data'], x)
                ),
                q.paginate(q.documents(q.collection(TRACKING_COLLECTION)))
            )
        )
        return jsonify(result['data'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/track', methods=['POST'])
def track():
    try:
        data = json.loads(request.data)
        
        # Coletar dados do visitante
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent_string = request.headers.get('User-Agent')
        user_agent = parse(user_agent_string)
        
        tracking_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'browser': user_agent.browser.family,
            'browser_version': user_agent.browser.version_string,
            'os': user_agent.os.family,
            'os_version': user_agent.os.version_string,
            'device': user_agent.device.family,
            'geolocation': get_geolocation(ip),
            'page_url': data.get('page_url'),
            'referrer': data.get('referrer'),
            'user_data': data.get('user_data', {})
        }
        
        client = get_client()
        result = client.query(
            q.create(
                q.collection(TRACKING_COLLECTION),
                {'data': tracking_data}
            )
        )
        
        return jsonify({
            'success': True,
            'tracking_id': result['ref'].id()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    client = get_client()
    try:
        result = client.query(
            q.map_(
                lambda x: q.select(['data'], x),
                q.paginate(
                    q.documents(q.collection(TRACKING_COLLECTION)),
                    size=1000
                )
            )
        )
        
        visits = result['data']
        
        # Análise dos dados
        stats = {
            'total_visits': len(visits),
            'browsers': {},
            'operating_systems': {},
            'devices': {},
            'countries': {},
            'recent_visits': sorted(visits, key=lambda x: x['timestamp'], reverse=True)[:10]
        }
        
        for visit in visits:
            stats['browsers'][visit['browser']] = stats['browsers'].get(visit['browser'], 0) + 1
            stats['operating_systems'][visit['os']] = stats['operating_systems'].get(visit['os'], 0) + 1
            stats['devices'][visit['device']] = stats['devices'].get(visit['device'], 0) + 1
            stats['countries'][visit['geolocation']['country']] = stats['countries'].get(visit['geolocation']['country'], 0) + 1
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_geolocation(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        return {
            'country': data.get('country_name', 'Unknown'),
            'city': data.get('city', 'Unknown'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }
    except:
        return {
            'country': 'Unknown',
            'city': 'Unknown',
            'latitude': None,
            'longitude': None
        }

@app.route('/setup', methods=['GET'])
def setup():
    try:
        client = get_client()
        
        # Criar coleções
        try:
            client.query(q.create_collection({'name': TRACKING_COLLECTION}))
            client.query(q.create_collection({'name': VISITS_COLLECTION}))
        except:
            pass
            
        # Criar índices
        try:
            client.query(
                q.create_index({
                    'name': 'all_tracking',
                    'source': q.collection(TRACKING_COLLECTION)
                })
            )
        except:
            pass
            
        return jsonify({
            'success': True,
            'message': 'Database setup completed successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def handler(event, context):
    return handler.handle(event, context) 