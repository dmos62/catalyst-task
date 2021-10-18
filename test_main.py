from main import app

def test_main():
    with app.test_client() as c:
        user_token = "123"
        response = c.get(
            '/',
            auth = (user_token, ""),
        )
        response_json = response.get_json()
        assert response.status_code == 200
        assert response_json == { "Hello": user_token }
