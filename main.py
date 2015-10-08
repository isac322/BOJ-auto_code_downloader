import os
import threading
import time

from NetworkTool import down_file, login, get_soup
from Problem import Problem

__author__ = 'isac3'


def get_solved_problems(sp):
	problems = set()

	for tag in sp.find(class_='panel-body').findAll('span', class_='problem_number'):
		problems.add(tag.a.text)

	return problems


working_dir = ''


def make_code_file(problem_num, language):
	extension = get_extension(language)

	file_name = problem_num + '.' + extension
	directory = os.path.join(working_dir, language)

	return open(os.path.join(directory, file_name), 'w+', encoding='utf-8')


def analyze_problem(problem_num):
	url = 'https://www.acmicpc.net/status/?'
	query = {'problem_id': problem_num, 'user_id': user_id, 'result_id': '4', 'language_id': '-1', 'from_mine': '1'}

	for k, v in query.items():
		url += k + '=' + v + '&'

	table = dict()
	language_set = set()

	page = get_soup(url, query)
	for row in page.find('tbody').find_all('tr'):
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

		language_set.add(language)

		if table.get(language) is None:
			table[language] = element
		else:
			table[language] = min(table[language], element)

	print(problem_num, table)

	return table, language_set


semaphore = threading.Semaphore(1)
total_language_set = set()


def analyze_and_make(problem_num):
	submitted_codes, language_set = analyze_problem(problem_num)

	for language in language_set:
		directory = os.path.join(working_dir, language)

		if language not in total_language_set:
			semaphore.acquire()
			if not os.path.exists(directory):
				os.makedirs(directory)

			total_language_set.add(language)
			semaphore.release()

	for language, source_code in submitted_codes.items():
		file = make_code_file(problem_num, language)
		downloaded = down_file(source_code.judge_id, full_cookie)
		file.write(str(downloaded.decode('utf-8')))
		file.close()


def get_submitted_files(problems):
	for problem_num in problems:
		thread_file_maker = threading.Thread(target=analyze_and_make, args=(problem_num,))
		thread_file_maker.start()
		time.sleep(0.1)


def get_extension(language):
	# todo add extensions
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


if __name__ == '__main__':
	working_dir = os.getcwd()

	user_id = input('enter user id : ')
	user_pw = input('enter password : ')
	full_cookie = login(user_id, user_pw)
	# print(full_cookie)

	soup = get_soup('https://acmicpc.net/user/' + user_id)

	problem_set = get_solved_problems(soup)

	print(problem_set)

	get_submitted_files(problem_set)
