__author__ = 'isac3'


class Problem:
	def __init__(self, judge_id, mem, time, code_len=None):
		self.judge_id = judge_id
		self.memory_size = mem
		self.time = time
		self.code_length = code_len

	def __lt__(self, other):
		if self.time == other.time:
			if self.memory_size == other.memory_size and self.code_length and other.code_length:
				return self.code_length < other.code_length
			else:
				return self.memory_size < other.memory_size
		else:
			return self.time < other.time

	def __str__(self):
		if self.code_length:
			return "{0} {1} KB {2} MS {3} B".format(self.judge_id, self.memory_size, self.time, self.code_length)
		else:
			return "{0} {1} KB {2} MS".format(self.judge_id, self.memory_size, self.time)

	def __repr__(self):
		return self.__str__()


def get_extension(language):
	if language in ['C++', 'C++11']:
		return 'cpp'
	elif language in ['C']:
		return 'c'
	elif language in ['Python', 'Python3', 'PyPy']:
		return 'py'
	elif language in ['Java']:
		return 'java'
	elif language in ['Text']:
		return 'txt'
	elif language in ['PHP']:
		return 'php'
