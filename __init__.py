import os
from binaryninja import *
from text_search import *

_choiceField = ChoiceField("Representation", ["Medium Level IL", "Low Level IL", "Assembly"])
_textField = TextLineField("Text to search")
_tempCache = {}

def doSearch(bv):
	if get_form_input([_choiceField, _textField], "Binja Text Search"):
		if not _textField.result:
			show_message_box("Binja Search Error", "Please enter a valid string to search", icon = MessageBoxIcon.ErrorIcon)
			return
		search = BSTextSearch(bv, _textField.result, _choiceField.result, _tempCache)
		search.start()

PluginCommand.register("[Search] Text search", "Search", doSearch)
