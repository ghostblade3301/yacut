from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .exceptions import IncorrectShortURLException, NonUniqueException
from .models import (SHORT_URL_INCORRECT_NAME, SHORT_URL_NAME_ALREADY_EXISTS,
                     URLMap)

EMPTY_BODY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
NOT_FOUND_ID = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsageError(EMPTY_BODY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsageError(URL_REQUIRED_FIELD)
    try:
        return jsonify(
            URLMap.create(
                data.get('url'),
                data.get('custom_id'),
            ).to_dict()
        ), HTTPStatus.CREATED
    except IncorrectShortURLException:
        raise InvalidAPIUsageError(
            SHORT_URL_INCORRECT_NAME,
            HTTPStatus.BAD_REQUEST,
        )
    except NonUniqueException:
        raise InvalidAPIUsageError(
            SHORT_URL_NAME_ALREADY_EXISTS.format(
                data.get('custom_id')
            ), HTTPStatus.BAD_REQUEST
        )


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsageError(NOT_FOUND_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK