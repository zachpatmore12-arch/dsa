from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        payload = request.get_json()
        discord_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        if not discord_url:
            return jsonify({'error': 'DISCORD_WEBHOOK_URL not set'}), 400
        
        response = requests.post(discord_url, json={
            'content': f'```json\n{json.dumps(payload, indent=2)}\n```'
        })
        
        if response.status_code != 204:
            return jsonify({'error': 'Failed to send to Discord'}), 500
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
