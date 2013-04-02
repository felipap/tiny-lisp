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
			if prog[i:i+2] == ['(',')']: # empty list = nil
				d = 'nil'
			elif prog[i] == '(': 
				if prog[i+2] == ')': # Single element within brackets:
					d = prog[i+1] # don't nest: get element
					i += 2 # and jump brackets.
				else: # A nested expression.
					d, i = nest(prog, i) # Get content (d) and update i.
			else: d = prog[i] # Else, just a symbol.
			array.append(d)
		return array, i # Tell parent call how far your reading went.

	import re
	tokens = re.split('(\(|\)|\s+|".*?[^\\\\])', code)
	return nest([c for c in tokens if c and not c.isspace()])[0] # Ignore blank.

def proc(argn, proc, env):
	# print("making procedure (%s) (%s)" % (argn, proc), argn)
	def wrapper(*args):
		nenv = env.copy()
		for i in range(len(argn)):
			nenv[argn[i]] = args[i]
		return eval(proc, nenv)
	return wrapper

listify = lambda x: [x] if not type(x)==list else x # Turns to list what isn't.
	
def eval(exp, env):
	# print("eval", exp, env.keys())
	if isinstance(exp, list): # If expression is a list
		if isinstance(exp[0], str): # which starts with a string:
			if exp[0].startswith('cond'): # It's a condition statement
				for cond, retv in exp[1:]: # => loop through conditions.
					if eval(cond, env):
						return retv
				return None # Nothing evaluated to True, return None.
			elif exp[0].startswith('lambda') or exp[0] == 'λ': # or a lambda.
				return proc(listify(exp[1]), exp[2], env) # => make procedure.
		# Not lambda nor cond: it's a procedure! Eval proc and args, then apply!
		return apply(eval(exp[0], env), [eval(i,env) for i in exp[1:]], env)
	else: # Expressipon is not a list: it's a constant.
		try: # Duck typing to check if it's a number.
			return float(exp) # Use float for all numbers. Hex not allowed.
		except: pass
		if exp[0] in ('\'', '\"'): # Quoted name.
			return exp
		else: # It's a symbol => lookup it up.
			# print("Looking up %s in %s" % (exp, env.keys()))
			return env[exp]

def apply(proc, args, env): # Apply the procedure to evaluated args.
	# print("applying %s with args %s." % (proc, args))
	return proc(*args)

if __name__ == "__main__":
	s = input('>> ') or '(list "2 3)' or '((λ x (+ x 2)) 3)'

	from lib import lib
	print(tokenize(s))
	print(eval(tokenize(s), lib.copy()))
