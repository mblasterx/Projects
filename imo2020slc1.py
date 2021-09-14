'''IMO 2020 Short List C1 problem solver for n
'''
import itertools

def main(n: int) -> int:
    badPermutations = 0
    for permutation in itertools.permutations(range(1,n+1)):
        for key, val in enumerate(permutation):
            if key < n-1 and (key+1)* val > (key+2) * permutation[key+1]:
                badPermutations += 1 
                break
    return fact(n) - badPermutations  

def fact(n:int) -> int:
    factorial = 1 
    for i in range(1,n+1): 
        factorial *= i 
    return factorial

n = int(input('What n would you like to solve the IMO 2020 ShortList problem C1 for? (anything over n=10 going to take a long time!) '))
print('The solution for n=' + str(n) + ' is: ' + str(main(n)))