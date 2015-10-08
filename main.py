__author__ = 'isac3'

from urllib.request import urlopen, Request
from urllib.parse import urlencode
import http.client
import urllib.error
import sys
import os
import re

from bs4 import BeautifulSoup as Bs

import Tools


def get_soup(url, query=None):
	response = get_response(url, query)
	ret = Bs(response, 'html.parser')
	response.close()
	return ret


def get_response(url, query=None, header=None):
	if header is None:
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
		header = {
			'Connection': 'keep-alive',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': user_agent,
			'Content-Type': 'application/x-www-form-urlencoded'
		}

	data = None
	if query is not None:
		data = urlencode(query).encode('utf-8')

	req = Request(url, data, header)

	try:
		response = urlopen(req)
		return response

	except urllib.error.HTTPError:
		print('invalid username')
		sys.exit(1)


def get_solved_problems(sp):
	problems = set()

	for tag in sp.find(class_='panel-body').findAll('span', class_='problem_number'):
		problems.add(tag.a.text)

	return problems


working_dir = ''


def make_code_file(problem_num, language):
	# todo : implement

	extension = Tools.get_extension(language)

	file_name = problem_num + '.' + extension
	directory = os.path.join(working_dir, language)

	return open(os.path.join(directory, file_name), 'wb+')


def analyze_problem(problem_num):
	# todo : analyze implement
	url = 'https://www.acmicpc.net/status/?'
	query = {'problem_id': problem_num, 'user_id': user_id, 'result_id': '4'}

	for k, v in query.items():
		url += k + '=' + v + '&'

	table = dict()
	language_set = set()

	page = get_soup(url)
	for row in page.find('tbody').find_all('tr'):
		column = row.find_all('td')

		language = column[6].text.strip()

		element = Tools.Problem(judge_id=column[0].text,
								mem=column[4].contents[0],
								time=column[5].contents[0],
								lang=language,
								code_len=column[7].text.strip().split()[0])

		language_set.add(language)

		if table.get(language) is None:
			table[language] = element
		else:
			table[language] = min(table[language], element)

	print(problem_num, table)

	return table, language_set


def get_submitted_files(problems):
	for problem_num in problems:
		submitted_codes, language_set = analyze_problem(problem_num)

		for language in language_set:
			directory = os.path.join(working_dir, language)
			if not os.path.exists(directory):
				os.makedirs(directory)

		for language, source_code in submitted_codes.items():
			file = make_code_file(problem_num, language)
			file.write(down_file(source_code.judge_id, full_cookie))
			file.close()
		# todo : implement


def login(id, pw):
	cookie_response = get_response('https://www.acmicpc.net')

	cookie = ''
	patt = re.compile('^.*((__cfduid|OnlineJudge)[=].*);.*&', re.MULTILINE)
	searched = patt.finditer(str(cookie_response.info()))
	print('fffffffffffffffff')
	for v in searched:
		print(v.string)
		cookie += v.group(1) + '; '

	print(cookie)

	cookie_response.close()

	query = {'login_user_id': user_id, 'login_password': user_pw, 'auto_login': 'on'}
	data = urlencode(query)
	header = {
		'Host': 'www.acmicpc.net',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Origin': 'https://www.acmicpc.net',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': 'https://www.acmicpc.net/login/?next=/',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
		'Cookie': cookie
	}

	conn = http.client.HTTPSConnection("www.acmicpc.net")
	conn.request('POST', '/signin', data, header)
	response = conn.getresponse()
	print(response.info())
	response.close()
	# print(response.msg)

	return cookie


def down_file(judge_id, cookie):
	header = {
		'Host': 'www.acmicpc.net',
		'Connection': 'keep-alive',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Origin': 'https://www.acmicpc.net,.',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': 'https://www.acmicpc.net/source/' + judge_id,
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
		'Cookie': cookie
	}

	conn = http.client.HTTPSConnection("www.acmicpc.net")
	conn.request('POST', '/source/download/' + judge_id, None, header)

	response = conn.getresponse()
	code = response.read()

	response.close()

	return code


if __name__ == '__main__':
	working_dir = os.getcwd()

	user_id = input('enter user id : ')
	user_pw = input('enter password : ')
	full_cookie = login(user_id, user_pw)
	print(full_cookie)

	soup = get_soup('https://acmicpc.net/user/' + user_id)

	problem_set = get_solved_problems(soup)

	print(problem_set)

	get_submitted_files(problem_set)
