
# Insert here the primitive functions.

from functools import reduce

lib = {
	'*': lambda a, *b: a*reduce(lambda x,y:x*y, b) or 3, # to make sure more than one
	'+': lambda a, *b: a+reduce(lambda x,y:x+y, b) or 3, # argument is passed.
	'=': lambda a, *b: all(a == e for e in b) or 3,
	
	'list': lambda *els: els,
	'map': lambda proc, array: [proc(e) for e in array],

	'else': True,
	'true': True,
	'false': False,
	'nil': None,
}
