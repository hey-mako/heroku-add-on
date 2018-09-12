"""This module contains endpoint definitions for provisioning add-ons
in Heroku.
"""
from base64 import b64decode
from functools import wraps
from http import HTTPStatus

from bson.objectid import ObjectId
from flask import jsonify, request
from flask.views import MethodView
from pymongo.collection import ReturnDocument

from . import application, database


def login_required(function):
    """Checks if the Authorization header exists in the HTTP request and
    decodes it. The decoded value contains an id and password separated
    via a colon. If the id and password do not match the values defined
    in the addon-manifest.json, then a 401 Unauthorized is returned.
    """
    @wraps(function)
    def decorated(*args, **kwargs): # pylint: disable=missing-docstring
        header = request.headers.get('Authorization')
        if header is None:
            return '', HTTPStatus.BAD_REQUEST
        _id, password = b64decode(header.split()[-1].encode('UTF-8')).decode('UTF-8').split(':')
        if not (
                _id == application.config['KENSA_ID'] and
                password == application.config['KENSA_PASSWORD']
            ):
            return '', HTTPStatus.UNAUTHORIZED
        return function(*args, **kwargs)
    return decorated


class ResourceController(MethodView):
    """Manage Heroku add-ons."""

    def delete(self, resource_uuid): # pylint: disable=no-self-use
        """This endpoint deletes a Heroku add-on."""
        document = database.resources.find_one_and_delete(
            filter={
                '_id': ObjectId(resource_uuid),
            }
        )
        if document is None:
            return '', HTTPStatus.NOT_FOUND
        return '', HTTPStatus.OK

    def post(self): # pylint: disable=no-self-use
        """This endpoint creates a Heroku add-on."""
        if not request.is_json:
            return '', HTTPStatus.BAD_REQUEST
        data = request.json
        result = database.resources.insert_one(data)
        response = {
            'config': {
                'MYADDON_URL': request.url,
            },
            'id': str(result.inserted_id),
        }
        return jsonify(response), HTTPStatus.OK

    def put(self, resource_uuid): # pylint: disable=no-self-use
        """This endpoint updates a Heroku add-on."""
        if not request.is_json:
            return '', HTTPStatus.BAD_REQUEST
        data = request.json
        document = database.resources.find_one_and_update(
            filter={
                '_id': ObjectId(resource_uuid),
            },
            update={
                '$set': {
                    'plan': data['plan'],
                },
            },
            return_document=ReturnDocument.AFTER
        )
        if document is None:
            return '', HTTPStatus.NOT_FOUND
        return '', HTTPStatus.OK


view = login_required(ResourceController.as_view('resources'))
application.add_url_rule('/heroku/resources', view_func=view)
application.add_url_rule(
    '/heroku/resources/<resource_uuid>',
    view_func=view,
    methods=['DELETE', 'PUT']
)
