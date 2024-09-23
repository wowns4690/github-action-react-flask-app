#--- 기존 test_app.py ---#
# import pytest
# import json
# from app import app  # 경로를 수정

# # pytest에서 사용하는 Fixture를 통해 테스트 클라이언트를 생성
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client


# def test_hello(client):
#     """GET /api/hello 테스트"""
#     response = client.get('/api/hello')
#     assert response.status_code == 200
#     assert response.json == {"message": "Hello, World!!!!!!!!!!!!"}


# def test_create_diary(client):
#     """POST /api/diaries 테스트"""
#     diary_data = {
#         "title": "My first diary",
#         "content": "Today was a good day!"
#     }
#     response = client.post('/api/diaries', 
#                            data=json.dumps(diary_data), 
#                            content_type='application/json')

#     assert response.status_code == 201
#     assert response.json['title'] == "My first diary"
#     assert response.json['content'] == "Today was a good day!"


# def test_update_diary(client):
#     """PUT /api/diaries/<id> 테스트"""
#     update_data = {
#         "title": "Updated diary",
#         "content": "Updated content"
#     }
#     # diary id 1을 업데이트한다고 가정
#     response = client.put('/api/diaries/1', 
#                           data=json.dumps(update_data), 
#                           content_type='application/json')

#     assert response.status_code == 200
#     assert response.json['title'] == "Updated diary"
#     assert response.json['content'] == "Updated content"


# def test_delete_diary(client):
#     """DELETE /api/diaries/<id> 테스트"""
#     # diary id 1을 삭제한다고 가정
#     response = client.delete('/api/delete/1')

#     assert response.status_code == 200
#     assert response.json['message'] == "아이템이 성공적으로 삭제되었습니다."


# def test_get_list(client):
#     """GET /api/list 테스트"""
#     response = client.get('/api/list')

#     assert response.status_code == 200
#     assert isinstance(response.json, list)  # 결과가 리스트인지 확인

#--- 수정된 test_app.py ---#
import pytest
import json
from unittest.mock import patch  # mock을 사용하여 DynamoDB 호출을 대체
from app import app

# pytest에서 사용하는 Fixture를 통해 테스트 클라이언트를 생성
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# DynamoDB를 mock 처리하는 pytest fixture
@pytest.fixture
def mock_dynamodb():
    with patch('app.table') as mock_table:
        yield mock_table

def test_hello(client):
    """GET /api/hello 테스트"""
    response = client.get('/api/hello')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!!!!!!!!!!!!"}


def test_create_diary(client, mock_dynamodb):
    """POST /api/diaries 테스트"""
    diary_data = {
        "title": "My first diary",
        "content": "Today was a good day!"
    }

    # DynamoDB의 put_item 호출을 mock 처리
    mock_dynamodb.put_item.return_value = {}

    response = client.post('/api/diaries', 
                           data=json.dumps(diary_data), 
                           content_type='application/json')

    assert response.status_code == 201
    assert response.json['title'] == "My first diary"
    assert response.json['content'] == "Today was a good day!"


def test_update_diary(client, mock_dynamodb):
    """PUT /api/diaries/<id> 테스트"""
    update_data = {
        "title": "Updated diary",
        "content": "Updated content"
    }

    # mock 처리: get_item, put_item
    mock_dynamodb.get_item.return_value = {'Item': {'id': 1, 'title': 'Old diary', 'content': 'Old content'}}
    mock_dynamodb.put_item.return_value = {}

    response = client.put('/api/diaries/1', 
                          data=json.dumps(update_data), 
                          content_type='application/json')

    assert response.status_code == 200
    assert response.json['title'] == "Updated diary"
    assert response.json['content'] == "Updated content"


def test_delete_diary(client, mock_dynamodb):
    """DELETE /api/diaries/<id> 테스트"""
    # mock 처리: delete_item
    mock_dynamodb.delete_item.return_value = {'Attributes': {'id': 1}}

    response = client.delete('/api/delete/1')

    assert response.status_code == 200
    assert response.json['message'] == "아이템이 성공적으로 삭제되었습니다."


def test_get_list(client, mock_dynamodb):
    """GET /api/list 테스트"""
    # mock 처리: scan
    mock_dynamodb.scan.return_value = {'Items': [{'id': 1, 'title': 'My diary', 'content': 'Content'}]}

    response = client.get('/api/list')

    assert response.status_code == 200
    assert isinstance(response.json, list)  # 결과가 리스트인지 확인
    assert len(response.json) > 0  # 항목이 있는지 확인