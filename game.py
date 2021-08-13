import random

class Range:
	def __init__(self, start, end):
		self.start = start
		self.end = end
	
	def __repr__(self):
		if self.start != self.end:
			return f"{self.start}-{self.end}"
		else:
			return f"{self.start}"

	def contains(self, n):
		return self.start <= n <= self.end
	
	def edge(self, n):
		if self.start-1 == n:
			self.start = n
			return True
		if self.end+1 == n:
			self.end = n
			return True
		return False

	def contains_r(self, r):
		return self.start <= r.start and self.end >= r.end

save = {
	"diff":0,
	"hoard":[Range(1,1)],
	"ops":list("+-*/%^"),
	"cur":0,
	"win":None
}

def repeat_until_valid_int():
	while c := input(">"):
		try:
			return int(c)
		except:
			print("Please enter an integer...")

def repeat_until_valid_char(valid):
	while c := input(">"):
		if c in valid and len(c)==1:
			return c
		else:
			print(f"Please enter a valid operation [{valid}]...")

def hoard_contains(n):
	for r in save['hoard']:
		if r.contains(n):
			return True

def hoard_add(n):
	hoard = save['hoard']
	if not hoard_contains(n):
		for r in hoard:
			if r.contains(n):
				break # already existed
			elif r.edge(n):
				break # added to range successfully
		if not hoard_contains(n):
			ix = 0
			while ix < len(hoard) and hoard[ix].end < n:
				ix += 1
			hoard.insert(ix, Range(n,n)) # create new range
	
	ix = 0
	while ix < len(hoard)-1:
		if hoard[ix].end == hoard[ix+1].start-1:
			hoard[ix].end=hoard[ix+1].end
			del hoard[ix+1]
		ix += 1
		# add range check later maybe


def try_int(n):
	try:
		int(n)
		return True
	except:
		return False

def title():
	print("Numbers Game")
	print("\nCollect all the numbers to win.\n")

def diff():
	print("Select your difficulty (Size of maximum number in bits to collect)")
	print("Suggested:\n8 - Easy\n16 - Normal\n24 - Hard\n32 - Tedious")
	print("Goals are the SIGNED INTEGERS in that range, so 8 would be [-128,127]")
	save['diff'] = repeat_until_valid_int()
	save['win'] = Range(2**(save['diff']-1)-2**save['diff'], 2**(save['diff']-1))

def instruct():
	print("Enter an operator and a number you have collected.")
	print("h=help, r=random, q=quit")

def rand():
	n = random.randint(0,save['diff'])
	if not hoard_contains(n):
		hoard_add(n)

call_ops = {
	"+": lambda x : save['cur'] + x,
	"-": lambda x : save['cur'] - x,
	"*": lambda x : save['cur'] * x,
	"/": lambda x : save['cur'] / x,
	"%": lambda x : save['cur'] % x,
	"^": lambda x : None if save['cur'] > pow(save['diff'], 1/x) else save['cur'] ** x,
}

def choice():
	for r in save['hoard']:
		if r.contains_r(save['win']):
			print("You've won! You can continue collecting, or use 'q' to quit")

	print(f"Current number: {save['cur']}")
	print(f"Current collection: {save['hoard']}\n")
	
	while not len(choice := input(">")):
		pass
	op = choice[0]
	dat = choice[1:]
	if op == "h":
		instruct()
	if op == "r":
		rand()
	if op in save['ops'] and try_int(dat):
		n = int(dat)
		save['cur'] = call_ops[op](n)
		hoard_add(save['cur'])
	
	return op != "q"

title()
diff()
instruct()
while choice():
	pass
print(f"Good game! Final collection: {save['hoard']}")
