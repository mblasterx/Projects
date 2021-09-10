def solve_recurrence(target: int, lines: list) -> str:
    '''Recurrence solution
    Returns a str with some GOOD/BAD characters at the end, we will strip them later
    '''
    vertex, rows = lines[0][0], len(lines)

    if target % vertex: return BAD   # if the target isn't divisible by vertex we end this tree here
    if rows == 1:   # lines iterator should never be empty; this is the base case in the recurrence
        return GOOD if target == vertex else BAD

    # recurrence step
    leftSolution = solve_recurrence(target//vertex, [lines[i][:-1] for i in range(1, len(lines))])
    rightSolution = solve_recurrence(target//vertex, [lines[i][1:] for i in range(1, len(lines))])

    # append the direction to the result string, or just BAD if we don't have a possibility at all
    if leftSolution[-1] is GOOD: return LEFT + leftSolution
    elif rightSolution[-1] is GOOD: return RIGHT + rightSolution
    else: return BAD

def solve_dp(target: int, lines: list, flag = False) -> str:
    '''Dynamic programming solution
    We go up from the last row, checking all the outputs of all the possible paths
    We could make it slightly more efficient by stopping when we found a solution on the bottom row
    Flag optional attribute; if True creates a list of all possible targets that have a solution for the given pyramid 
    '''
    dp = [[{}]*len(x) for x in lines] # initiate the dp array of dictionaries

    dp[0][0][''] = lines[0][0]
    for i in range(1, len(dp)):
        for j in range(len(dp[i])):
            if j == 0:  # edge on the left of the pyramid
                dp[i][j] = { key + LEFT: lines[i][j]*val for key,val in dp[i-1][0].items() }
            elif j == len(dp[i])-1: # edge on the right of the pyramid
                dp[i][j] = { key + RIGHT: lines[i][j]*val for key,val in dp[i-1][j-1].items() }
            else:   # inside the pyramid
                dp[i][j] = { key + RIGHT: lines[i][j]*val for key,val in dp[i-1][j-1].items() } \
                    | { key + LEFT: lines[i][j]*val for key,val in dp[i-1][j].items() }
    
    # now we solve looking at the last row
    results = { key:val for d in dp[-1] for key,val in d.items() if val == target or flag}
    
    # if we wanted we can change to find all possible good values for target and return those? aka construct all the possible good puzzles
    if flag:
        return '\n'.join([str(val) for val in results.values()])

    if results:
        for key in results.keys():
            # this just returns the first way, we can easily modify to return all the ways 
            return key
    else: return 'No solution' # need to write something in the file


def solve_rec(target: int, lines: list) -> str:
    '''Returns the solved puzzle in proper format, without the end strings
    '''
    return solve_recurrence(target, lines).strip(BAD+GOOD)

def read_input(fileName = 'pyramid_sample_input.txt'):
    '''Read the input puzzle to solve
    First line: Target: (int)
    Rest of Lines: int, int, int, etc.'''
    target, lines = 0, []
    with open(FILE_DIR_PATH + fileName) as file:
        for line in file:
            if line.startswith('Target: '):
                target = int(line.replace('Target: ', ''))
            else:   # we get all the variables in a double list, making sure each element is an int, we will need that in the solve_recurrence function for the modulo % operator 
                lines.append(list(map(int, line.strip().split(','))))
    return target, lines

def write_output(s: str, fileName = 'pyramid_sample_output.txt') -> None:
    '''Write to the output file'''
    with open(FILE_DIR_PATH + fileName, 'w') as file:
        file.write(s)

def test() -> None:
    '''Just some basic testing for edge cases and such, and the given sample
    More testing was done once the file_input/output methods were established'''
    testCases = [
        (5,
            [5],
        '',
        ),
        (6,
            [2],
            [4,3],
        RIGHT,
        ),
        (720, 
            [2], 
            [4,3],
            [3,2,6],
            [2,9,5,2],
            [10,5,2,15,5],
        LEFT+RIGHT+LEFT+LEFT,
        ),
    ]

    for target, *lines, expectedOutput in testCases:
        assert solve_rec(target, lines) == expectedOutput # ,(target, lines, expectedOutput, solve_rec(target,lines))
    print('All tests passed')


def main() -> None:
    '''Main program body
    You can change the filename for input and output here, should work if input file in the same directory'''
    global FILE_DIR_PATH
    FILE_DIR_PATH = ''

    target, lines = read_input()
    write_output(solve_dp(target, lines))
    # write_ouput(solve_dp(target, lines, True))
    # write_output(solve_rec(target, lines))

# some global vars for making the code look cleaner
BAD, GOOD, LEFT, RIGHT = 'B', 'G', 'L', 'R'

main()
# test()