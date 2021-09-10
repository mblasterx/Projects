import re, itertools

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            print(f)
            # return f if we want to end it once we found 1 answer
    
def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(set(x for x in formula if x.isalpha()))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = str.maketrans(letters, ''.join(digits))
        yield formula.translate(table)
    
def valid(f):
    """Formula f is valid if and only if it has no 
    numbers with leading zero, and evals true."""
    try: 
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False

# MODIFY HERE THE STRINGS YOU WANT THE PUZZLE TO GO
solve('ODD+ ANY == EVEN')

# import cProfile
# cProfile.run("solve('')")