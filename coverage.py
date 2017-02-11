#!/usr/bin/python
import sys
import os
from operator import itemgetter
from itertools import groupby

def coverage_parse(lines_result, covered_result, missed_result):
	current_file_path = ""
	current_file_lines_count = 0
	current_file_covered_count = 0
	for line in sys.stdin:
		line_type = check_line_type(line)
		if line_type == "LINE_NEGLECTABLE":
			continue
		elif line_type == "LINE_NEW_FILE":
			if current_file_path:
				lines_result[current_file_path] = current_file_lines_count
				covered_result[current_file_path] = current_file_covered_count
			current_file_path = line
			current_file_lines_count = 0
			current_file_covered_count = 0
		elif line_type == "LINE_UNCOVERED":
			current_file_lines_count += 1
			if current_file_path and get_line_number(line) > 0:
				current_line_number = get_line_number(line)
				add_to_missed_result(missed_result, current_file_path, current_line_number)
		elif line_type == "LINE_COVERED":
			current_file_lines_count += 1
			current_file_covered_count += 1
	if current_file_path:
		lines_result[current_file_path] = current_file_lines_count
		covered_result[current_file_path] = current_file_covered_count

def add_to_missed_result(missed_result, key, line_number):
	if key in missed_result:
		missed_result[key].append(line_number)
	else:
		missed_result[key] = [line_number]


def get_line_number(line):
	segments = line.split('|')
	if len(segments) > 1 and segments[1].strip():
		return int(segments[1].strip())
	return -1


def print_output(lines_result, covered_result, missed_result):
	total_lines = 0
	total_covered_lines = 0
	print '------------------------------------------------------------------------------'
	print 'File                                         Lines     Exec  Cover  Missing'
	print '------------------------------------------------------------------------------'
	for key in sorted(lines_result.keys()):
		if lines_result[key] > 0 and (not check_contains_keywords(key)):
			if base_dir and key.startswith(base_dir):
				file_name = os.path.relpath(key, base_dir)
			elif base_dir == "":
				file_name = key
			else:
				continue
			print file_name, repr(lines_result[key]).rjust(50), repr(covered_result[key]).rjust(8), repr(covered_result[key] * 100 / lines_result[key]).rjust(5) + '% ',
			if key in missed_result:
				print_missed_lines(missed_result[key])
			print '' #print out end of line
			total_lines += lines_result[key]
			total_covered_lines += covered_result[key]
	if total_lines > 0:
		print '------------------------------------------------------------------------'
		print "Total:", repr(total_lines).rjust(43), repr(total_covered_lines).rjust(8), repr(total_covered_lines * 100 / total_lines).rjust(5) + '%'
		print '------------------------------------------------------------------------'

def print_missed_lines(lines):
	for k, g in groupby(enumerate(lines), lambda (i,x):i-x):
		group = map(itemgetter(1), g)
		if len(group) > 1:
			print repr(group[0])+'-'+repr(group[-1]),
		else:
			print repr(group[0]),

def check_line_type(line):
	if line.strip() == "" or line.strip().startswith('|'):
		return "LINE_NEGLECTABLE"
	elif not line.startswith(' '):
		return "LINE_NEW_FILE"
	elif line.strip().startswith('0'):
		return "LINE_UNCOVERED"
	else:
		return "LINE_COVERED"

def check_contains_keywords(filepath):
	for keyword in exclude_keywords:
		if filepath.find(keyword) != -1:
			return True
	return False

#initialize variables
lines_result = {}
covered_result = {}
missed_result = {}
exclude_keywords = ['Cell', 'View.', 'Tests/', 'Pods/', 'Pods.build/', 'AppConfig/', 'ThirdPartySource/', 'Training/', '/iPhoneSimulator.platform/', '/XcodeDefault.xctoolchain/']
base_dir = ""
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
	base_dir = os.path.abspath(sys.argv[1])

coverage_parse(lines_result, covered_result, missed_result)
print_output(lines_result,covered_result, missed_result)
