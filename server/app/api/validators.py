from flask import Response, current_app, request

from . import api
from .utils import make_yaml_response, parse_yaml


@api.route('/validator/dictionary_info', methods=['POST'])
def dictionary_info_valid() -> 'Response':
	dictionary_info = parse_yaml(request.get_data())
	return make_yaml_response({
		'valid': current_app.extensions['dictionaries'].settings.dictionary_info_valid(dictionary_info),
	})

@api.route('/validator/source', methods=['POST'])
def source_valid() -> 'Response':
	source = parse_yaml(request.get_data())['source']
	return make_yaml_response({
		'valid': current_app.extensions['dictionaries'].settings.source_valid(source),
	})
