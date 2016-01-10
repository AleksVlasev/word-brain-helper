from nltk.corpus import words
from time import time as tm
from time import sleep
from copy import deepcopy
import numpy as np

yes_no = ['y', 'n']
steps = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]


def prompt(message, choice=False, options=[]):
	print message,
	if choice is False:
		ans = raw_input()
	elif choice is True and len(options) > 0:
		valid = False
		ans = ""
		while not valid:
			ans = raw_input()
			if ans in options:
				valid = True
			else:
				print "Invalid input. Enter one of {}".format(options)
	else:
		print "No options found"
		ans = "42"
	return ans


def time_msg(message, t1, t2):
	print message + " ({:.3f} sec)".format(t2-t1)


def print_line(visible=True, short=False):
	if visible:
		if short:
			print "================"
		else:
			print "================================================================"


def print_grid(grid):
	# take in dictionary
	temp = dict_to_list(grid)
	n = len(temp)
	print_line(True,True)
	for i in range(n):
		for j in range(n):
			print temp[i][j],
		print ""
	print_line(True, True)

"-----------------------------------------------------------------------------------"


def list_minus(A, B):
	temp = A[:]  # copy
	for b in B:
		if b in temp:
			temp.remove(b)
	return temp


def contains(chars, word):
	if len(chars) - len(word) == len(list_minus(chars, word)):
		return True
	else:
		return False


def remove(listing, x):
	temp = listing[:]
	temp.remove(x)
	return temp


def add(listing, x):
	temp = listing[:]
	temp.append(x)
	return temp


def dict_to_grid(grid):
	n = int(np.sqrt(len(grid)))
	grid_temp = [['0' for _ in range(n)] for _ in range(n)]
	for pt in grid:
		grid_temp[pt[0]][pt[1]] = grid[pt]
	return grid_temp


def dict_to_list(grid):
	n = int(np.sqrt(len(grid)))
	grid_temp = [['0' for _ in range(n)] for _ in range(n)]
	for pt in grid:
		grid_temp[pt[0]][pt[1]] = grid[pt]
	return grid_temp


def list_to_dict(grid):
	n = len(grid)
	grid_temp = {}
	for i in range(n):
		for j in range(n):
			grid_temp[(i, j)] = grid[i][j]
	return grid_temp


def update(grid, walk):
	# take in a dictionary and return one

	grid_as_list = dict_to_list(grid)
	for pt in walk[0]:
		grid_as_list[pt[0]][pt[1]] = '0'
	n = len(grid_as_list)
	for stage in range(n):
		for i in range(1, n):
			line = grid_as_list[i]
			for j in range(n):
				if line[j] == '0':
					grid_as_list[i][j] = grid_as_list[i-1][j]
					grid_as_list[i-1][j] = '0'
	return list_to_dict(grid_as_list)


def solution(grid, nums, characters, dictionary, starting_strings, soln, solns, track):
	if nums == []:
		solns.append(soln)
		print " - ",
		for word in soln:
			print word,
		print ''
	else:
		candidates = find_candidates(grid, nums, characters, dictionary, starting_strings, track)
		for walk in candidates:
			new_grid = update(grid, walk)
			new_nums = remove(nums, len(walk[-1]))
			new_soln = add(soln, walk[-1])
			# print_line()
			# print new_nums, new_soln
			# print_line()
			solution(new_grid, new_nums, characters, dictionary, starting_strings, new_soln, solns, track)


def find_candidates(grid, nums, characters, dictionary, starting_strings, track):

	# print "Sleeps..."
	# sleep(3)
	# print "Done. Here is the grid.\n"
	# print_grid(grid)
	flag = False

	starting_walks = []
	for i in range(n):
		for j in range(n):
			pt = (i, j)
			if grid[pt] != '0':
				walk = [{pt: 0}, {0: pt}, 0, grid[pt]]
				starting_walks.append(walk)

	candidates = []
	old_walks = starting_walks
	new_walks = []
	t_begin = tm()
	for k in range(max(nums)-1):
		t_start = tm()
		for step in steps:
			for walk in old_walks:
				walk_temp = deepcopy(walk)
				points, indices, index, word = tuple(walk_temp)
				next_pt = (indices[index][0] + step[0], indices[index][1] + step[1])
				if next_pt not in points and next_pt in grid:
					if grid[next_pt] != '0':
						index += 1
						points[next_pt] = index
						indices[index] = next_pt
						word += grid[next_pt]
						track[1] += 1
						if track[1] % 20000 == 0:
							print "{} walks checked so far.".format(track[1])
						if word in starting_strings:
							new_walk = [points, indices, index, word]
							new_walks.append(new_walk)
							if len(word) in nums and word in dictionary:
								if track[0] == 0:
									flag = True
								track[0] += 1
								if track[0] % 500 == 0:
									print "{} words checked so far.".format(track[0])
								candidates.append(new_walk)
		t_end = tm()
		# time_msg("Time for words of length {}".format(k+2), t_start, t_end)
		old_walks = new_walks
		new_walks = []
	t_end = tm()
	# time_msg("Finding the candidates.", t_begin, t_end)
	candidates.sort(key=lambda x: len(x[-1]))
	candidates.reverse()
	if flag:
		wordings = []
		for walk in candidates:
			wordings.append(walk[-1])
		wordings = list(set(wordings))
		wordings.sort(key=lambda x: len(x), reverse=True)
		for word in wordings:
			print word,
		print ''
	return candidates

if __name__ == "__main__":
	print "Loading..."

	t_start = tm()
	# word_list = words.words()[:100]
	word_list = words.words()
	word_list.append('tv')
	t_end = tm()
	time_msg("Loading words.", t_start, t_end)

	t_start = tm()
	valid_words = []
	for word in word_list:
		ascii = word.encode('ascii', 'ignore')
		if ascii == ascii.lower():
			valid_words.append(ascii)
	t_end = tm()
	time_msg("Validating words.", t_start, t_end)

	play = True
	while play:
		error = False
		# Beware, there is no error handling yet.
		n = int(prompt("Enter the size 'n' of the grid:"))

		characters = ""
		print "Enter the characters in each consecutive line and press enter:"
		for i in range(n):
			characters += prompt("Line {}:".format(i+1))
		characters = list(characters)

		nums = prompt("Enter the numbers of characters in each word, separated by commas:").split(',')
		nums = map(lambda x: int(x), nums)

		if sum(nums) != n**2 or len(characters) != n**2:
			print "ERROR: Not the right number of characters or character lengths."
			error = False

		if not error:
			
			grid = {(i, j): characters[i*n+j] for i in range(n) for j in range(n)}
			
			t_start = tm()
			dictionary = {}
			starting_strings = {}
			for word in valid_words:
				if contains(characters, word):
					dictionary[word] = True
					for ind in range(len(word)):
						starting_strings[word[:ind+1]] = True
			t_end = tm()
			time_msg("Building pruned word list.", t_start, t_end)
			print "Lengths: {}, {}".format(len(dictionary), len(starting_strings))

			print "Here are the possible solutions, one at a time:"
			solns = []
			track = [0, 0]
			solution(grid, nums, characters, dictionary, starting_strings, [], solns, track)

			solns.sort()
			solns = [solns[i] for i in range(len(solns)) if i == 0 or solns[i] != solns[i-1]]
			print "There are {} solutions".format(len(solns))
			print "Here they are:"
			for soln in solns:
				print " - ",
				for word in soln:
					print word,
				print ''
			print "Solutions found in {} iterations.".format(track[0])
		ans = prompt("Play again? (y/n)", choice=True, options=yes_no)
		if ans == 'n':
			play = False
		print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
