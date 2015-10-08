__author__ = 'isac3'


class Problem:
	def __init__(self, judge_id, mem, time, lang, code_len):
		self.judge_id = judge_id
		self.memory_size = mem
		self.time = time
		self.language = lang
		self.code_length = code_len

	def __lt__(self, other):
		if self.time == other.time:
			if self.memory_size == other.memory_size:
				return self.code_length < other.code_length
			else:
				return self.memory_size < other.memory_size
		else:
			return self.time < other.time

	def __str__(self):
		return "{0} {1}KB {2}MS {3} {4}B".format(self.judge_id, self.memory_size, self.time, self.language,
												self.code_length)

	def __repr__(self):
		return self.__str__()


if __name__ == '__main__':
	a = Problem('a', 'b', 'c', 'd', 'e')

	print(a.code_length)
