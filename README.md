# f03lipe/tiny-lisp

A tiny **TINY** *REEEEALY TINY* interpreter for a lisp-like language.<br>

### What is this for?
Nothing, obviously.

### License:
MIT License.

## What is supported

### Nested s-expressions: 

```lisp
>> (+ (* (/ 3 4) 100) 45)
120
```
### Anon functions: `lambda` or `λ`
```lisp
>> ((λ (x y) (+ x y)) 3 4)
7
>> ((lambda m m) 0)
0
```
### Conditions: `cond`
```lisp
>> ((λ (x) (cond ((% x 2) 'odd) (else 'even))) 4)
'even
```
### Literals: `'`
```lisp
>> (list 'one '2 3)
("a", "2", 3)
```
### Strings: doubles-quotes only
```lisp
>> (list "a "3)
("a", 3)
```
### Assigning: `define`s at the beggining of any block (evaluating to last element)
```lisp
>> (+ ((define a 3) (* 10 a)) 5)
35
```
#### To define procedures, use `lambda`
```lisp
>> ((define pow (lambda (x n) (cond ((= n 1) x) (else (* x (pow x (- n 1))))))) (pow 2 4))
16.0
```
