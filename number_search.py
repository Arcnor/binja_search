import os
import configparser
import json
from binaryninja import *

class BSNumberSearch(BackgroundTaskThread):
	def __init__(self, bv, number, location, cache, *args, **kwargs):
		BackgroundTaskThread.__init__(self, '', True)
		self.progress = "Starting Binja Search..."
		self.bv = bv
		self.number = number
		self.location = location
		self.cache = cache

	def _search(self, number):
		result = []
		instructions = None
		if self.location == 0:
			instructions = self.bv.mlil_instructions
		elif self.location == 1:
			instructions = self.bv.llil_instructions
		elif self.location == 2:
			show_message_box("Binja Search Error", "Number search on Assembly not supported yet", icon = MessageBoxIcon.ErrorIcon)
			return
		else:
			show_message_box("Binja Search Error", "Invalid selected representation", icon = MessageBoxIcon.ErrorIcon)
			return

		if "inst_total" in self.cache:
			total = str(self.cache["inst_total"])
		else:
			total = "unknown"

		count = 0
		for inst in instructions:
			count += 1
			if not count % 100:
				self.progress = "Searching instructions %i/%s..." % (count, total)
			for op in inst.prefix_operands:
				if isinstance(op, (int, long)) and op == number:
					result.append(inst)
					break

		self.cache["inst_total"] = count

		self.progress = "Searching finished"

		return result

	def _showSearchResult(self, number, result):
		strList = map(lambda t: "0x%X - %s" % (t.address, str(t)), result)
		textResult = "\n".join(strList)
		self.bv.show_plain_text_report("Search for '0x%X'" % number, textResult)

	def run(self):
		result = self._search(self.number)
		self._showSearchResult(self.number, result)
