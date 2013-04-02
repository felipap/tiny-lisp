#!/usr/bin/env python3
# -*- encoding: utf8 -*-
# A *tiny* lisp interpreter in python. Good luck understanding that.
# f03lipe, 2013

def tokenize(code): # What? You don't know what a tokenizer is?
	def nest(prog, i=0): # Nests the tokenized code, recursively.
		array = [] # The content for the current nest level.
		while i < len(prog): # Reading (i) starts where parent call left.
			i += 1
			if prog[i] == ')': break # Bracket from parent level: return.
			elif prog[i:i+2] == ['(',')']: # empty list = nil
				d = 'nil'
			elif prog[i] == '(': # Nested expression:
				d, i = nest(prog, i) # get content (d) and update the index.
			else: d = prog[i] # Else, just a symbol.
			array.append(d)
		return array, i # Tell parent call how far your reading went.

	import re
	tokens = re.split('(\(|\)|\s+|".*?[^\\\\]")', code)
	return nest([c for c in tokens if c and not c.isspace()])[0] # Ignore blank.

def proc(argn, proc, env):
	# print("creating procedure with args:{%s}, body:{%s}." % (argn, proc), argn)
	def wrapper(*args):
		nenv = env.copy()
		for i in range(len(argn)):
			nenv[argn[i]] = args[i]
		return eval(proc, nenv)
	return wrapper

listify = lambda x: [x] if not type(x)==list else x # Turns into list what isn't
unlistify = lambda x: x[0] if type(x)==list and len(x)==1 else x
	
def eval(exp, env):
	# print("eval(%s) >> %s" % (exp, env))
	exp = unlistify(exp)
	if isinstance(exp, list): # If exp is a list
		if isinstance(exp[0], str): # which starts with a string:
			if exp[0].startswith('cond'): # It's a condition statement
				for cond, retv in exp[1:]: # => loop through conditions.
					if eval(cond, env):
						return eval(retv, env)
				return 3.1415 # Nothing evaluated to True, return Pie.
			elif exp[0] in ('lambda', 'λ'): # or a lambda.
				return proc(listify(exp[1]), exp[2], env) # => make procedure.
		elif exp[0][0] == 'define': # It's a define statement!
			nenv = env.copy() # Create new environment for nested expressions.
			for i in range(len(exp)): # Loop through (define ...) statements.
				if exp[i][0] != 'define': break # Exp to return was found
				else:
					nenv[exp[i][1]] = eval(exp[i][2], nenv)
			return eval(exp[-1], nenv) # Eval expression to return.
		# Not lambda nor cond: it's a procedure! Eval proc and args, then apply!
		return apply(eval(exp[0], env), [eval(i,env) for i in exp[1:]], env)
	else: # exp isn't a list: it's a constant.
		try: # Check if it's a number.
			return float(exp) # Use float for everything. Hex not allowed (yet?)
		except: pass
		if exp[0] in ('\'', '\"'): # Quoted name.
			return exp.replace('\'', '')
		else: # It's a symbol => lookup it up.
			return env[exp]

def apply(proc, args, env): # Apply the procedure to evaluated args.
	# print("applying %s with args %s." % (proc, args))
	return proc(*args)

if __name__ == "__main__":
	s = input('>> ') or '((define pow (lambda (x n) (cond ((= n 1) x) (else (* x (pow x (- n 1))))))) (pow 2 3))'

	from lib import lib
	print(eval(tokenize(s), lib.copy()))
