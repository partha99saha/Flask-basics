from unittest.mock import patch, MagicMock
import jwt
from flask import Flask, request, jsonify
from your_module import auth_required

app = Flask(__name__)


@app.route('/protected')
@auth_required
def protected_route(user):
    return jsonify({'message': 'Access granted'})


def test_auth_required():
    with app.test_request_context('/protected'):
        # Mocking request headers and token
        headers = {'Authorization': 'Bearer test_token'}
        request.headers = headers

        # Mocking JWT decoding
        mock_jwt_decode = MagicMock(return_value={'id': 1})
        with patch('jwt.decode', mock_jwt_decode):
            # Mocking User.query.filter_by()
            mock_user_query = MagicMock()
            mock_user_query.first.return_value = MagicMock()
            with patch('models.User.User.query.filter_by', mock_user_query):
                response = protected_route()

    assert response.status_code == 200
    assert response.json == {'message': 'Access granted'}


# if __name__ == '__main__':
#     test_auth_required()
