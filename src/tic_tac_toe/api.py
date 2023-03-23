# tic_tac_toe/api.py
from flask import Flask, request, jsonify, abort
from utilities import tic_tac_toe_winner

app = Flask(__name__)


@app.route('/winner', methods=['GET'])
def winner():
    board = request.args.get('board', '').replace('_', ' ')
    try:
        return jsonify({
            'winner': tic_tac_toe_winner(board)
        })
    except ValueError:
        abort(400)


def test_api_response_is_json():
    response = app.test_client().get('/winner?board=_________')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert isinstance(response.json, dict)
    assert 'winner' in response.json
