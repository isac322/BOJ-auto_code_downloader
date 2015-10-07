__author__ = 'isac3'

from urllib.request import urlopen, Request
import urllib.error
import sys
import os

from bs4 import BeautifulSoup


def get_soup(url):
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	hdr = {'User-Agent': user_agent}
	req = Request(url, headers=hdr)

	try:
		response = urlopen(req)
		return BeautifulSoup(response, 'html.parser')

	except urllib.error.HTTPError:
		print('invalid username')
		sys.exit(1)


def get_solved_problems(sp):
	problems = set()

	for tag in sp.findAll('span', class_='problem_number'):
		problems.add(tag.a.text)

	return problems


working_dir = ""


def make_code_file(problem_num, extension):
	# todo : implement
	file_name = problem_num + '.' + extension


def analyze_problem(problem_num):
	# todo : analyze implement
	pass


def get_source_files(problems):
	for problem in problems:
		analyze_problem(problem)
	# todo : implement


if __name__ == '__main__':
	working_dir = os.getcwd()
	user = input('user nick name : ')

	soup = get_soup('https://acmicpc.net/user/' + user)

	problem_set = get_solved_problems(soup)
	print(problem_set)
