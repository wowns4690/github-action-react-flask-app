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
    next_id = 0
    response = table.scan()
    if 'Items' in response and len(response['Items']) > 0:
        ids = max([item['id'] for item in response['Items']])
        next_id = ids + 1
        return  next_id
    return next_id


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
    next_id = get_list()
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
    return jsonify(message="Hello, World!!!!!")



@app.route('/api/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        # DynamoDB 테이블에서 아이템 삭제
        response = table.delete_item(
            Key={
                'id': item_id  # 'id'를 실제 기본 키 속성 이름으로 교체하세요
            },
            ReturnValues='ALL_OLD'  # 삭제된 항목의 이전 값을 반환
        )
        # 삭제된 항목의 속성이 반환되었는지 확인
        if 'Attributes' in response:
            return jsonify({"message": "아이템이 성공적으로 삭제되었습니다."}), 200
        else:
            return jsonify({"message": "아이템을 찾을 수 없습니다."}), 404
    except ClientError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)