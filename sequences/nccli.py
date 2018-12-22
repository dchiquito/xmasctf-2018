
from subprocess import *
import re


class NC:
	def __init__(self, cmd, debug=False):
		self.cmd = cmd
		self.debug = debug
		self._proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)

	def close(self):
		self._proc.kill()
	
	def write(self, msg):
		if self.debug: print msg
		self._proc.stdin.write(msg)

	def readline(self):
		if self.debug: print ".",
		line = self._proc.stdout.readline()
		if self.debug: print line,
		return line

	def read(self, regex):
		pattern = re.compile(regex)
		while True:
			line = self.readline()
			match = pattern.search(line)
			if match:
				return match


