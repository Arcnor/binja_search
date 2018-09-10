import os
import configparser
import json
from binaryninja import *

class BSTextSearch(BackgroundTaskThread):
	def __init__(self, bv, text, location, cache, *args, **kwargs):
		BackgroundTaskThread.__init__(self, '', True)
		self.progress = "Starting Binja Search..."
		self.bv = bv
		self.text = text
		self.location = location
		self.cache = cache

	def _search(self, text):
		result = []
		basic_blocks = None
		if self.location == 0:
			basic_blocks = self.bv.mlil_basic_blocks
		elif self.location == 1:
			basic_blocks = self.bv.llil_basic_blocks
		elif self.location == 2:
			basic_blocks = self.bv.basic_blocks
		else:
			show_message_box("Binja Search Error", "Invalid selected representation", icon = MessageBoxIcon.ErrorIcon)
			return

		if "total" in self.cache:
			total = str(self.cache["total"])
		else:
			total = "unknown"

		count = 0
		lowerText = text.lower()
		for bb in basic_blocks:
			count += 1
			self.progress = "Searching basic blocks %i/%s..." % (count, total)
			for line in bb.disassembly_text:
				lineStr = str(line).lower()
				if lowerText in lineStr:
					result.append(line)

		self.cache["total"] = count

		self.progress = "Searching finished"

		return result

	def _showSearchResult(self, text, result):
		strList = map(lambda t: "0x%X - %s" % (t.address, str(t)), result)
		textResult = "\n".join(strList)
		self.bv.show_plain_text_report("Search for '%s'" % text, textResult)

	def run(self):
		result = self._search(self.text)
		self._showSearchResult(self.text, result)
