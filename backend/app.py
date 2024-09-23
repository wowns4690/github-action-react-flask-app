import os
from flask import Flask, jsonify
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)

# AWS 자격 증명을 환경 변수에서 가져옴
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# AWS DynamoDB 클라이언트 설정
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-2',  # AWS 리전 설정
    aws_access_key_id=AWS_ACCESS_KEY_ID,  # 환경 변수로부터 가져온 AWS 액세스 키
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY  # 환경 변수로부터 가져온 AWS 시크릿 키
)

# DynamoDB 테이블 설정
table = dynamodb.Table('crud-table')

#DB crud-table 항목 가져오기
@app.route('/api/list', methods=['GET'])
def get_list():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify(items), 200
    except ClientError as e:
        return jsonify({"error":str(e)}), 500



@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

if __name__ == '__main__':
    app.run(debug=True)
