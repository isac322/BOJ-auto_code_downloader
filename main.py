#!/usr/bin/env python3
# coding: utf-8

import os
import threading
from getpass import getpass

import extensions
from network_tools import down_file, get_soup, login
from submit_record import SubmitRecord

__author__ = 'isac322'


def get_solved_problems(sp):
    problems = set()

    for tag in sp.find(class_='panel-body').findAll('span', class_='problem_number'):
        problems.add(tag.a.text)

    return problems


working_dir = ''


def make_code_file(problem_num, language):
    extension = extensions.extension_name[language]

    file_name = problem_num + '.' + extension
    directory = os.path.join(working_dir, "{:05d}".format(int(problem_num)))

    return open(os.path.join(directory, file_name), 'w+', encoding='utf-8')


screenLock = threading.Lock()


def analyze_problem(problem_num):
    url = 'https://www.acmicpc.net/status?'
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

        element = SubmitRecord(judge_id=column[0].text,
                               mem=column[4].contents[0],
                               time=column[5].contents[0],
                               code_len=length)

        if table.get(language) is None:
            table[language] = element
        else:
            table[language] = min(table[language], element)

    problem_name = rows[0].find_all('td')[2].a['title']

    screenLock.acquire()
    print('{:5s} {}'.format(problem_num, problem_name))
    for l, e in table.items():
        print('\t{:10s} {}'.format(l, e))
    screenLock.release()

    return table


def analyze_and_make(problem_num):
    submitted_codes = analyze_problem(problem_num)

    for language, source_code in submitted_codes.items():
        with make_code_file(problem_num, language) as file:
            downloaded = down_file(source_code.judge_id, full_cookie)
            file.write(downloaded.decode())


ignore_list = frozenset(('10947', '9999', '13757'))


def get_submitted_files(problems):
    for problem_num in problems:
        directory = os.path.join(working_dir, "{:05d}".format(int(problem_num)))

        if not os.path.exists(directory):
            os.makedirs(directory)

        thread_file_maker = threading.Thread(target=analyze_and_make, args=(problem_num,), daemon=False)
        thread_file_maker.start()


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
