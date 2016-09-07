#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import threading
import time
from getpass import getpass

from NetworkTool import down_file, login, get_soup
from Problem import Problem

__author__ = 'isac322'


def get_solved_problems(sp):
	problems = set()

	for tag in sp.find(class_='panel-body').findAll('span', class_='problem_number'):
		problems.add(tag.a.text)

	return problems


working_dir = ''


def make_code_file(problem_num, language):
	extension = get_extension(language)

	file_name = problem_num + '.' + extension
	directory = os.path.join(working_dir, problem_num)

	return open(os.path.join(directory, file_name), 'w+', encoding='utf-8')


def analyze_problem(problem_num):
	url = 'https://www.acmicpc.net/status/?'
	query = {'problem_id': problem_num, 'user_id': user_id, 'result_id': '4', 'language_id': '-1', 'from_mine': '1'}

	for k, v in query.items():
		url += k + '=' + v + '&'

	table = dict()

	page = get_soup(url, query)
	rows = page.find('tbody').find_all('tr')

	if len(rows) is 0:
		return table

	for row in rows:
		column = row.find_all('td')

		language = column[6].text.strip()

		length = None
		length_text = column[7].text.strip()
		if len(length_text) != 0:
			length = length_text.split()[0]

		element = Problem(judge_id=column[0].text,
						  mem=column[4].contents[0],
						  time=column[5].contents[0],
						  code_len=length)

		if table.get(language) is None:
			table[language] = element
		else:
			table[language] = min(table[language], element)

	problem_name = rows[0].find_all('td')[2].a['title']
	print("{:5s} {:15s} ".format(problem_num, problem_name), table)

	return table


def analyze_and_make(problem_num):
	submitted_codes = analyze_problem(problem_num)

	directory = os.path.join(working_dir, problem_num)

	if not os.path.exists(directory):
		os.makedirs(directory)

	for language, source_code in submitted_codes.items():
		file = make_code_file(problem_num, language)
		downloaded = down_file(source_code.judge_id, full_cookie)
		file.write(str(downloaded.decode('utf-8')))
		file.close()


def get_submitted_files(problems):
	for problem_num in problems:
		thread_file_maker = threading.Thread(target=analyze_and_make, args=(problem_num,))
		thread_file_maker.start()
		time.sleep(0.02)


def get_extension(language):
	# todo add extensions
	if language in ['C++', 'C++ (Clang)']:
		return 'cpp'
	elif language in ['C++11']:
		return 'cpp11.cpp'
	elif language in ['C++14']:
		return 'cpp14.cpp'
	elif language in ['C', 'C (Clang)']:
		return 'c'
	elif language in ['Python']:
		return 'py'
	elif language in ['Python3']:
		return 'py3.py'
	elif language in ['PyPy']:
		return 'pypy.py'
	elif language in ['Java']:
		return 'java'
	elif language in ['Text']:
		return 'txt'
	elif language in ['PHP']:
		return 'php'
	elif language in ['Ruby 1.8', 'Ruby 1.9']:
		return 'rb'
	elif language in ['C# 2.0', 'C# 4.0']:
		return 'cs'
	elif language in ['Pascal']:
		return 'pas'
	elif language in ['D']:
		return 'd'
	elif language in ['Go']:
		return 'go'
	elif language in ['awk']:
		return 'awk'
	elif language in ['VB.NET 2.0']:
		return 'vb'
	elif language in ['Ada']:
		return 'ada'
	elif language in ['Perl', 'Perl6', 'Prolog']:
		return 'pl'
	elif language in ['node.js', 'SpiderMonkey']:
		return 'js'
	elif language in ['Lua']:
		return 'lua'
	elif language in ['Objective-C']:
		return 'm'
	elif language in ['Objective-C++']:
		return 'mm'
	elif language in ['Fortran']:
		return 'f95'
	elif language in ['Scheme']:
		return 'scm'
	elif language in ['OCaml']:
		return 'ml'
	elif language in ['Brainfuck']:
		return 'bf'
	elif language in ['Whitespace']:
		return 'ws'
	elif language in ['Groovy']:
		return 'groovy'
	elif language in ['Tcl']:
		return 'tcl'
	elif language in ['Assembly']:
		return 'asm'
	elif language in ['Clojure']:
		return 'clj'
	elif language in ['Rhino']:
		return 'Rhino.js'
	elif language in ['Pike']:
		return 'pike'
	elif language in ['sed']:
		return 'sed'
	elif language in ['Boo']:
		return 'boo'
	elif language in ['Intercal']:
		return 'i'
	elif language in ['bc']:
		return 'bc'
	elif language in ['Nemerle']:
		return 'n'
	elif language in ['Cobra']:
		return 'cobra'
	elif language in ['Nimrod']:
		return 'nim'
	elif language in ['Io']:
		return 'io'
	elif language in ['아희']:
		return 'aheui'


if __name__ == '__main__':
	user_id = input('enter nickname : ')
	user_pw = getpass('enter password : ')
	full_cookie = login(user_id, user_pw)
	# print(full_cookie)

	soup = get_soup('https://acmicpc.net/user/' + user_id)

	working_dir = os.path.join(os.getcwd(), user_id)

	if not os.path.exists(working_dir):
		os.makedirs(working_dir)

	problem_set = get_solved_problems(soup)

	get_submitted_files(problem_set)
