import abc
import unicodedata

from ..settings import Settings


class BaseReader(abc.ABC):

	"""Abstract base class for reading dictionaries."""

	_CACHE_ROOT = Settings.CACHE_ROOT
	_ARTICLE_SEPARATOR = '\n<hr>\n'

	@staticmethod
	def strip_diacritics(text: 'str') -> 'str':
		return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn' and not unicodedata.combining(c))

	@staticmethod
	def remove_punctuation_and_spaces(text: 'str') -> 'str':
		return ''.join(c for c in text if unicodedata.category(c)[0] not in ['P', 'Z'])

	@staticmethod
	def simplify(text: 'str') -> 'str':
		"""Removes accents and punctuation, expand ligatures, and converts to lowercase."""
		return BaseReader.remove_punctuation_and_spaces(BaseReader.strip_diacritics(text)).casefold()

	def __init__(self,
	      		 name: 'str',
				 filename: 'str',
				 display_name: 'str') -> None:
		"""
		:param name: the name of the dictionary, deduced by removing the extension(s) from the filename, used internally
		:param filename: the name of the main file of the dictionary with extension(s)
		:param display_name: the name of the dictionary as it should be displayed to the user
		"""
		self.name = name
		self.filename = filename
		self.display_name = display_name

	@abc.abstractmethod
	def entry_definition(self, entry: 'str') -> 'str':
		"""
		:param entry: the entry to look up, must be simplified
		:return: the definition of the given entry (match by key only; that is, ignore case and diacritics).
		"""
		pass