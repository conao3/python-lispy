# Lispy

Lispy from [(How to Write a (Lisp) Interpreter (in Python))](https://norvig.com/lispy.html) with some modernizations based on Python 3.12.

This Lispy is based on [lis.py](https://norvig.com/lis.py) at 2023-12-01.


# Usage

```bash
poetry install
poetry run python lis.py
```

# Sample

```lisp
$ poetry run python lis.py
lis.py> (define circle-area (lambda (r) (* pi (* r r))))
<__main__.Procedure object at 0x102ab4f20>
lis.py> (circle-area 3)
28.274333882308138
lis.py> (define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))
<__main__.Procedure object at 0x102ab7950>
lis.py> (fact 10)
3628800
lis.py> (fact 100)
93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
lis.py> (circle-area (fact 10))
41369087205782.695
lis.py> (define first car)
<function standard_env.<locals>.<lambda> at 0x102ac8400>
lis.py> (define rest cdr)
<function standard_env.<locals>.<lambda> at 0x102ac85e0>
lis.py> (define count (lambda (item L) (if L (+ (equal? item (first L)) (count item (rest L))) 0)))
<__main__.Procedure object at 0x102ad8320>
lis.py> (count 0 (list 0 1 2 3 0 0))
3
lis.py> (count (quote the) (quote (the more the merrier the bigger the better)))
4
lis.py> (define twice (lambda (x) (* 2 x)))
<__main__.Procedure object at 0x102ad98b0>
lis.py> (twice 5)
10
lis.py> (define repeat (lambda (f) (lambda (x) (f (f x)))))
<__main__.Procedure object at 0x102a7f8f0>
lis.py> ((repeat twice) 10)
40
lis.py> ((repeat (repeat twice)) 10)
160
lis.py> ((repeat (repeat (repeat twice))) 10)
2560
lis.py> ((repeat (repeat (repeat (repeat twice)))) 10)
655360
lis.py> (pow 2 16)
65536.0
lis.py> (define fib (lambda (n) (if (< n 2) 1 (+ (fib (- n 1)) (fib (- n 2))))))
<__main__.Procedure object at 0x102ad9670>
lis.py> (define range (lambda (a b) (if (= a b) (quote ()) (cons a (range (+ a 1) b)))))
<__main__.Procedure object at 0x102ad8e00>
lis.py> (range 0 10)
(0 1 2 3 4 5 6 7 8 9)
lis.py> (map fib (range 0 10))
(1 1 2 3 5 8 13 21 34 55)
lis.py> (map fib (range 0 20))
(1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765)
lis.py> C-c
```


# Contributing

Before commit, install pre-commit hooks:

```bash
poetry run pre-commit install
```


# License

Unfortunately, we could not find the licence in the original article.
Please let me know if there is a problem.
As for the changes I have made, they are available under Apache-2.0.
