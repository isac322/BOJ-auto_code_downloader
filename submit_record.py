# coding: utf-8

import sys

__author__ = 'isac322'


class SubmitRecord:
    def __init__(self, judge_id, mem, time, code_len=None):
        try:
            self.judge_id = int(judge_id)
            self.memory_size = int(mem)
            self.time = int(time)
            if code_len:
                code_len = int(code_len)
            self.code_length = code_len

        except ValueError:
            print('Problem record error on judge id : {}. Please re-run. If you have same error in same id, '
                  'check BOJ online.'.format(judge_id),
                  file=sys.stderr)
            exit(1)

    def __lt__(self, other):
        if self.time == other.time:
            if self.memory_size == other.memory_size:
                if self.code_length and other.code_length:
                    return self.code_length < other.code_length
                else:
                    return self.judge_id < other.judge_id
            else:
                return self.memory_size < other.memory_size
        else:
            return self.time < other.time

    def __str__(self):
        if self.code_length:
            return 'ID:{:>8}\tMem:{:>6}KB\tTime:{:>5}MS\tSize:{:>5}B' \
                .format(self.judge_id, self.memory_size, self.time, self.code_length)
        else:
            return 'ID:{:>8}\tMem:{:>6}KB\tTime:{:>5}MS'.format(self.judge_id, self.memory_size, self.time)

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    print('please run main.py')
