# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    # Your code here
    # do odd palindromes first
    text = text.lower()
    maxLeft, maxRight = 0, 0

    for i in range(len(text)):
        left, right = longest_subpalindrome_centered(text, i, i)
        if maxRight - maxLeft < right-left: # if new max, update it
            maxLeft, maxRight = left, right

    if len(text)>1:
        for i in range(len(text)-1):
            left, right = longest_subpalindrome_centered(text, i, i+1)
            if maxRight - maxLeft < right-left: # if new max, update it
                maxLeft, maxRight = left, right

    return maxLeft, maxRight

def longest_subpalindrome_centered(text,left, right):
    "Returns (i,j) the longest palindrome in text centered at text[left:right+1]"
    if text[left] != text[right]:   # if its a 2 digit and they're not equal 
        return left, left+1
    else:
        while left>0 and right<len(text)-1:
            if text[left-1] == text[right+1]:
                left -= 1
                right += 1
            else:
                break

    return left, right+1 # make the slice to include index right but not right+1 


def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print(test())