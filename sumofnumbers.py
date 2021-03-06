import random

def check_if_sum_is_in_the_array(ary, sum):
    '''Checks is any two elements in the array sum up to a given number
    Returns a tuple with the Boolean and the values that sum up, or just a Boolean
    '''
    complements = set()
    for val in ary:
        if sum-val in complements: return (True, val, sum-val)
        else:
            complements.add(val)
    return False

def test():
    testAry = [random.randrange(1, 20, 1) for i in range(15)]
    sum = random.randint(10,40)
    assert check_if_sum_is_in_the_array(testAry, sum), (testAry, sum)
    print('All tests passed!')
    # also test edge cases

def main():
    # test()

if __name__ == '__main__':
    main()