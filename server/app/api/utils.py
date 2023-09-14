import logging

import yaml
from flask import Response, make_response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
	from yaml import CDumper as Dumper
	from yaml import CSafeLoader as Loader
except ImportError:
	from yaml import Dumper
	from yaml import SafeLoader as Loader
	logger.warning('Using pure Python YAML parser. Consider installing libyaml for faster speed.')

YAML_CONTENT_TYPE = 'text/plain; charset=utf-8'

def make_yaml_response(data: 'list | dict') -> 'Response':
	return make_response(yaml.dump(data, Dumper=Dumper), 200, {'Content-Type': YAML_CONTENT_TYPE})

def parse_yaml(data: 'str') -> 'list | dict':
	return yaml.load(data, Loader=Loader)