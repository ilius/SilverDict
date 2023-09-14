from flask import (
	Response,
	current_app,
	make_response,
	render_template,
	request,
	send_from_directory,
)

from .. import db_manager
from ..dictionaries import simplify
from . import api
from .utils import make_yaml_response


@api.route('/suggestions/<group_name>/<key>')
def suggestions(group_name: 'str', key: 'str') -> 'Response':
	key_simplified = simplify(key)
	dicts = current_app.extensions['dictionaries']
	if not dicts.settings.group_exists(group_name):
		response = make_response('<p>Group %s not found</p>' % group_name, 404)
	else:
		suggestions = dicts.suggestions(group_name, key_simplified)
		response = make_yaml_response(suggestions)
	return response

@api.route('/query/<group_name>/<key>')
def query(group_name: 'str', key: 'str') -> 'Response':
	key_simplifed = simplify(key)
	dicts = current_app.extensions['dictionaries']
	if not dicts.settings.group_exists(group_name):
		response = make_response('<p>Group %s not found</p>' % group_name, 404)
	elif not db_manager.entry_exists_in_dictionaries(key_simplifed, dicts.settings.dictionaries_of_group(group_name)):
		response = make_response('<p>Entry {} not found in group {}</p>'.format(key_simplifed, group_name), 404)
	else:
		articles = dicts.query(group_name, key_simplifed)
		dicts.settings.add_word_to_history(key) # We can't do this inside Dictionaries because the key passed inside is simplified.
		articles_html = render_template('articles.html', articles=articles)
		including_dictionaries = request.args.get('dicts', False)
		if including_dictionaries:
			response = make_yaml_response(
				{
					'articles': articles_html,
					'dictionaries': [article[0] for article in articles],
				},
			)
		else:
			response = make_response(articles_html)
	return response

@api.route('/lookup/<dictionary_name>/<key>')
def lookup(dictionary_name: 'str', key: 'str') -> 'Response':
	"""Legacy API, preserved for compatibility."""
	key_simplified = simplify(key)
	dicts = current_app.extensions['dictionaries']
	if not db_manager.dictionary_exists(dictionary_name):
		response = make_response('<p>Dictionary %s not found</p>' % dictionary_name, 404)
	elif not db_manager.entry_exists_in_dictionary(key_simplified, dictionary_name):
		response = make_response('<p>Entry {} not found in dictionary {}</p>'.format(key_simplified, dictionary_name), 404)
	else:
		dicts.settings.add_word_to_history(key)
		response = make_response(dicts.lookup(dictionary_name, key_simplified))
	return response

@api.route('/cache/<path:path_name>')
def send_cached_resources(path_name: 'str') -> 'Response':
	return send_from_directory(current_app.extensions['dictionaries'].settings.CACHE_ROOT, path_name)
