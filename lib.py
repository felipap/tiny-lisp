
# Insert here the primitive functions.

from functools import reduce

lib = {
	'*': lambda a, *b: a*reduce(lambda x,y:x*y, b), # to make sure more than one
	'+': lambda a, *b: a+reduce(lambda x,y:x+y, b), # argument is passed.
	'=': lambda a, *b: all(a == e for e in b),
	'-': lambda a, b: a-b,
	'/': lambda a, b: a/b,
	'%': lambda a, b: a%b,
	
	'list': lambda *els: els,
	'map': lambda proc, array: [proc(e) for e in array],

	'else': True,
	'true': True,
	'false': False,
	'nil': None,
}
