# needs refactoring 
# turn into OOP

# class Poker():
#     '''
#     Poker game
#     '''
    
import itertools

ALLRANKS = '23456789TJQKA'

def poker(hands):
    '''Returns the winning hands as a list if there is more than one, or a single hand if it's only one winner
    '''
    winningHands = allmax(hands, key=hand_rank)
    return winningHands if len(winningHands) > 1 else winningHands[0]

def allmax(iterable, key=None):
    '''Return a list of all items equal to the max of the iterable.
    '''
    keyT = key or (lambda x:x)
    maxHand = max(iterable, key=keyT)
    return [hand for hand in iterable if keyT(hand) == keyT(maxHand)]


def kind(n, ranks) -> int:
    '''
    Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand.
    '''
    from collections import Counter
    ranksDict = Counter(ranks)  # counts how many of each rank are in ranks and puts it in a dictionary
    return next((key for key, value in ranksDict.items() if value == n), None)  # if there is a value of n return the largest one

def hand_rank(hand):
    '''
    Returns a tuple indicating the ranking of a hand 
    '''
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))  # have to make an exception for A,2,3,4,5
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks))
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    from collections import Counter
    ranksDict = Counter(ranks)  # counts how many of each rank are in ranks and puts it in a dictionary
    pairs = []
    for key,val in ranksDict.items():
        if val == 2:
            pairs.append(key)
    if len(pairs) == 2: 
        return max(pairs), min(pairs)

def card_ranks(cards):
    '''Return a list of the ranks, sorted with higher first
    '''
    ranks = [('--' + ALLRANKS).index(r) for r,s in cards]
    ranks.sort(reverse=True)
    return ranks if ranks != [14, 5, 4, 3, 2] else [5,4,3,2,1]

def straight(ranks):
    '''Return true if the ordered ranks form a 5-card straight
    Assuming the input is always ordered decreasingly
    Might have to correct for A being 1 
    '''
    # first line is unique ranks, second is the difference between them
    return ( len(set(ranks)) == len(ranks) ) \
        and ( max(ranks) - min(ranks) == len(ranks)-1 )

def flush(hand):
    '''Return true if the suits of all the cards in hand are the same
    '''
    suits = [s for r,s in hand]
    return len(set(suits)) == 1 



def deal(numHands, numCards = 5, deck=[r+s for r in '23456789TJQKA' for s in 'cdhs'] ):
    from random import shuffle
    shuffle(deck)
    return [deck[numCards*i:numCards*(i+1)] for i in range(numHands)]

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    return max(itertools.combinations(hand,5), key=hand_rank)
    # Your code here


def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    hands = set(best_hand(h)
                for h in itertools.product(*map(replacements,hand)))    # all the possible 5 hand combinations using jokers 
    return max(hands, key=hand_rank)

def replacements(card:str):
    '''Return a list of the possible replacements for a card
    There will be more than 1 only for wild cards like jokers 
    '''
    blackDeck, redDeck = [r+s for r in ALLRANKS for s in 'cs'], [r+s for r in ALLRANKS for s in 'dh']
    if card == '?b':
        return blackDeck
    elif card == '?r':
        return redDeck
    else:
        return [card]

'''VARIOUS TESTS HERE 
'''

def test_best_hand():
    assert (sorted(best_hand("6c 7c 8c 9c Tc 5c Js".split()))
            == ['6c', '7c', '8c', '9c', 'Tc'])
    assert (sorted(best_hand("Td Tc Th 7c 7d 8c 8s".split()))
            == ['8c', '8s', 'Tc', 'Td', 'Th'])
    assert (sorted(best_hand("Jd Tc Th 7c 7d 7s 7h".split()))
            == ['7c', '7d', '7h', '7s', 'Jd'])
    return 'test_best_hand passes'

def test():
    sf = "6c 7c 8c 9c Tc".split()
    fk = "9c 9d 9h 9s 7d".split()
    fh = "Td Tc Th 7c 7d".split()
    tp = "5s 5d 9h 9c 6s".split()
    al = "Ac 2d 4h 3d 5s".split() # Ace-Low Straight
    sf1 = "6c 7c 8c 9c Tc".split() # Straight Flush
    sf2 = "6d 7d 8d 9d Td".split() # Straight Flush
    
    assert straight(card_ranks(al)) == True 
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2] 
    assert straight([9,8,7,6,5]) == True
    assert straight([9,8,8,6,5]) == False
    assert flush(sf) == True
    assert flush(fh) == False
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert two_pair(fkranks) == None
    assert kind(1, fkranks) == 7
    assert card_ranks(sf) == [10,9,8,7,6]
    assert card_ranks(fk) == [9,9,9,9,7]
    assert card_ranks(fh) == [10,10,10,7,7]
    assert hand_rank(sf) == (8,10)
    assert hand_rank(fk) == (7,9,7)
    assert hand_rank(fh) == (6,10,7)
    assert poker([sf]) == sf
    assert poker([sf1, sf2, 88*fh]) == [sf1,sf2]
    assert poker([sf1, sf2]) == [sf1,sf2]
    assert poker([fk, fh]) == fk
    
    return "tests pass"

def test_best_wild_hand():
    assert (sorted(best_wild_hand("6c 7c 8c 9c Tc 5c ?b".split()))
             == ['7c', '8c', '9c', 'Jc', 'Tc'])
    assert (sorted(best_wild_hand("Td Tc 5h 5c 7c ?r ?b".split()))
            == ['7c', 'Tc', 'Td', 'Th', 'Ts'])
    assert (sorted(best_wild_hand("Jd Tc Th 7c 7d 7s 7h".split()))
            == ['7c', '7d', '7h', '7s', 'Jd'])
    return 'test_best_wild_hand passes'


print(test())
print(test_best_hand())
# test_best_wild_hand()