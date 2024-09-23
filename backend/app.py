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

# DB crud-table 항목 가져오기
@app.route('/api/list', methods=['GET'])
def get_list():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify(items), 200
    except ClientError as e:
        return jsonify({"error":str(e)}), 500

# Update 항목
@app.route('/api/update/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()  # 클라이언트에서 전송한 JSON 데이터
    if not data:
        return jsonify({"message": "업데이트할 데이터가 없습니다."}), 400

    try:
        # DynamoDB 테이블에서 항목 업데이트
        response = table.update_item(
            Key={
                'id': item_id  # 'id'를 실제 기본 키 속성 이름으로 교체하세요
            },
            UpdateExpression="set #name = :name, age = :age",  # name과 age 필드를 업데이트
            ExpressionAttributeNames={
                '#name': 'name'
            },
            ExpressionAttributeValues={
                ':name': data.get('name'),
                ':age': data.get('age')
            },
            ReturnValues='ALL_NEW'  # 업데이트된 항목의 새 값을 반환
        )

        # 업데이트된 항목의 속성이 반환되었는지 확인
        if 'Attributes' in response:
            return jsonify({"message": "아이템이 성공적으로 업데이트되었습니다.", "updated_item": response['Attributes']}), 200
        else:
            return jsonify({"message": "아이템을 찾을 수 없습니다."}), 404
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

# Delete 항목
@app.route('/api/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        # DynamoDB 테이블에서 항목 삭제
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

# 기본 Hello API
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!!!!!!!!!!!!")

if __name__ == '__main__':
    app.run(debug=True)
