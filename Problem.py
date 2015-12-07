# -*- coding: utf-8 -*-

__author__ = 'isac322'


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


if __name__ == '__main__':
	print('please run main.py')
