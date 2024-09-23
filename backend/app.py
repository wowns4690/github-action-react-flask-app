import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)

# AWS DynamoDB 클라이언트 설정
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-2'  # AWS 리전 설정
)

# DynamoDB 테이블 설정
table = dynamodb.Table('crud-table')

def get_next_id():
    response = table.scan()
    if 'Items' in response and len(response['Items']) > 0:
        ids = max([item['id'] for item in response['Items']])
        return ids + 1
    return 1

next_id = get_next_id()

#DB crud-table 항목 가져오기
@app.route('/api/list', methods=['GET'])
def get_list():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify(items), 200
    except ClientError as e:
        return jsonify({"error":str(e)}), 500

@app.route("/api/diaries", methods=['POST'])
def create_diary():
    global next_id
    data = request.json

    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    
    diary = {
        'id': next_id,
        'title': data['title'],
        'content': data['content']
    }

    table.put_item(Item=diary)
    next_id += 1
    return jsonify(diary), 201

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

if __name__ == '__main__':
    app.run(debug=True)
