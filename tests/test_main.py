import requests

api_url = 'http://localhost:8000'

def test_healthcheck():
    response = requests.get(f'{api_url}/__health')
    assert response.status_code == 200


class testMenuItems():
    def test_get_blank_items():
        response = requests.get(f'{api_url}/v1/menu_items')
        assert response.status_code == 200
        assert len(response.json()) == 0
    
    def test_add_item():
        body = {"name": "item 1", "description": "desc 1", "price": 350 }
        response = requests.post(f'{api_url}/v1/menu_items', json = body)
        assert response.status_code == 200
        assert response.json().get('name') == 'item 1'
        assert response.json().get('description') == 'desc 1'
        assert response.json().get('price') == 34
        assert response.json().get('id') == 0

    def test_get_item_id():
        response = requests.post(f'{api_url}/v1/menu_items/0')
        assert response.status_code == 200
        assert response.json().get('name') == 'item 1'
        assert response.json().get('description') == 'desc 1'
        assert response.json().get('price') == 350
        assert response.json().get('id') == 0

    def test_get_items():
        response = requests.get(f'{api_url}/v1/menu_items')
        assert response.status_code == 200
        assert len(response.json()) == 1