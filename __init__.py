import os
from binaryninja import *
from text_search import *
from number_search import *

_choiceField = ChoiceField("Representation", ["Medium Level IL", "Low Level IL", "Assembly"])
_textField = TextLineField("Text to search")
_numberField = TextLineField("Number to search (0x for hex, 0b for binary)")
_tempCache = {}

def doTextSearch(bv):
	if get_form_input([_choiceField, _textField], "Binja Text Search"):
		if not _textField.result:
			show_message_box("Binja Search Error", "Please enter a valid string to search", icon = MessageBoxIcon.ErrorIcon)
			return
		search = BSTextSearch(bv, _textField.result, _choiceField.result, _tempCache)
		search.start()

def doNumberSearch(bv):
	if get_form_input([_choiceField, _numberField], "Binja Number Search"):
		if not _numberField.result:
			show_message_box("Binja Search Error", "Please enter a valid number to search", icon = MessageBoxIcon.ErrorIcon)
			return
		trimmed = _numberField.result.strip().lower()
		try:
			if trimmed.startswith("0x"):
				number = int(trimmed, 16)
			elif trimmed.startswith("0b"):
				number = int(trimmed[2:], 2)
			else:
				number = int(trimmed)
		except:
			show_message_box("Binja Search Error", "'%s' doesn't seem to be a valid number" % trimmed, icon = MessageBoxIcon.ErrorIcon)
			return
		search = BSNumberSearch(bv, number, _choiceField.result, _tempCache)
		search.start()

PluginCommand.register("[Search] Text search", "Search", doTextSearch)
PluginCommand.register("[Search] Number search", "Search", doNumberSearch)
