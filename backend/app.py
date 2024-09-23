from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
import json
import uuid

app = Flask(__name__)
CORS(app)

s3 = boto3.client('s3')
bucket_name = 'simple-react-web'

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!!")

@app.route('/api/diaries', methods=['POST'])
def create_memo():
    data = request.json

    if 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400

    id = str(uuid.uuid4())

    diary = {
        'id': id,
        'title': data['title'],
        'content': data['content']
    }
    s3.put_object(Bucket=bucket_name, Key=f'{id}.json', Body=json.dumps(diary))
    
    return jsonify(diary), 201

if __name__ == '__main__':
    app.run(debug=True)
