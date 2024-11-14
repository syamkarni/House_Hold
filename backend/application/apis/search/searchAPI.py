from flask import Blueprint
from flask_restful import Resource, Api

search_bp = Blueprint('search_bp', __name__)
search_api = Api(search_bp)

class SearchAPI(Resource):
    def get(self):
        #testing search api
        return {'message': 'Search results'}, 200

search_api.add_resource(SearchAPI, '/search')
