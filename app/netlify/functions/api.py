from flask import Flask, request, jsonify, redirect
from flask_serverless import FlaskServerless
import json
import os
from datetime import datetime
from uuid import uuid4
import requests
from user_agents import parse
from faunadb import query as q
from fauna_config import get_client, LINKS_COLLECTION, VISITS_COLLECTION

app = Flask(__name__)
handler = FlaskServerless(app)

def save_to_fauna(collection, data):
    client = get_client()
    result = client.query(
        q.create(
            q.collection(collection),
            {'data': data}
        )
    )
    return result['ref'].id()

def get_from_fauna(collection, ref_id):
    client = get_client()
    try:
        result = client.query(
            q.get(q.ref(q.collection(collection), ref_id))
        )
        return result['data']
    except:
        return None

def get_real_ip(event):
    headers = event.get('headers', {})
    if headers.get('x-forwarded-for'):
        return headers['x-forwarded-for'].split(',')[0]
    return headers.get('client-ip', 'unknown')

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

@app.route('/links', methods=['GET'])
def get_links():
    client = get_client()
    try:
        result = client.query(
            q.map_(
                lambda x: q.merge(
                    {'id': q.select(['ref', 'id'], x)},
                    q.select(['data'], x)
                ),
                q.paginate(q.documents(q.collection(LINKS_COLLECTION)))
            )
        )
        return jsonify(result['data'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_link', methods=['POST'])
def create_link():
    try:
        data = json.loads(request.body)
        link_data = {
            'target_url': data['target_url'],
            'description': data.get('description', ''),
            'created_at': datetime.now().isoformat(),
            'visits': 0
        }
        
        link_id = save_to_fauna(LINKS_COLLECTION, link_data)
        return jsonify({'success': True, 'link_id': link_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/l/<link_id>', methods=['GET'])
def redirect_link(link_id):
    client = get_client()
    try:
        # Buscar link
        link = get_from_fauna(LINKS_COLLECTION, link_id)
        if not link:
            return "Link não encontrado", 404
            
        # Incrementar contador de visitas
        client.query(
            q.update(
                q.ref(q.collection(LINKS_COLLECTION), link_id),
                {'data': {'visits': link['visits'] + 1}}
            )
        )
        
        # Registrar visita
        visit_data = {
            'link_id': link_id,
            'timestamp': datetime.now().isoformat(),
            'ip': get_real_ip(request.event),
            'user_agent': request.headers.get('User-Agent'),
            'geolocation': get_geolocation(get_real_ip(request.event))
        }
        save_to_fauna(VISITS_COLLECTION, visit_data)
        
        return redirect(link['target_url'])
    except Exception as e:
        return str(e), 500

@app.route('/stats/<link_id>', methods=['GET'])
def get_stats(link_id):
    client = get_client()
    try:
        # Buscar link
        link = get_from_fauna(LINKS_COLLECTION, link_id)
        if not link:
            return "Link não encontrado", 404
            
        # Buscar visitas
        visits = client.query(
            q.map_(
                lambda x: q.select(['data'], x),
                q.paginate(
                    q.match(q.index('visits_by_link'), link_id)
                )
            )
        )
        
        return jsonify({
            'link': link,
            'visits': visits['data']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def handler(event, context):
    return handler.handle(event, context) 