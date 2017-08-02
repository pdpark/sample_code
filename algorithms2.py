'''Code is my own, but accomplished with a little help from python docs, 
stackoverflow, quora, etc.'''

from collections import deque

''' Determine if all characters of second string are found in first string '''
def chars_in(s, t):
    if s == '' or t == '':
        return False
    
    # Dictionary of chars in s - value is count of char in s 
    schars = {c: s.lower().count(c) for c in s.lower()}
    
    # go through chars in t
    for c in t.lower():
        # if char found in schars with a count gt zero, decrement the count
        if c in schars and schars[c] > 0:
            schars[c] -= 1
        # otherwise char not found or we ran out of that char, so return false
        else:
            return False
    # if we made it this far, all the chars in t were found somewhere in s
    #    so return true
    return True

''' Find the largest palindrome (if one exists) in the input string'''
def pal(a):
    if a is None or len(a) < 2: return ''
    
    maxpal = ''
    maxchk = len(a)
    
    ndx = 1
    # At each character in the input string, compare chars on either side 
    #    (right side includes index) at same distance from index, building the 
    #    palindrome until the chars at the same distance from the current index 
    #    don't match
    while ndx < maxchk:
        # Chars up to but not including the index 
        left = list(a[:ndx])
        # Chars from the index to the end of the string, reversed
        right = list(reversed(a[ndx:]))
        # A place to store the palndrome as we discover it
        pal = deque()
        # The Left and Right chars at same distance from index to be compared
        lc = rc = ''
        # Continue building palindrome as long as the left and Right chars
        #    match and we have something in left and right strings to 
        #    continue to check
        while lc == rc and left and right:
            # Take the right-most char from the left string and lower-case it
            lc = left.pop().lower()
            # Take the right-most char from the right string and lower-case it
            #    (remember it is reversed, so the chars to the right are 
            #    closest to the index)
            rc = right.pop().lower()
            # if they match we have part of our palindrome
            if lc == rc:
                # build up the palindrome from the matching left & right chars
                pal.appendleft(lc)
                pal.append(rc)
                # This is the case where the middle letters of the palindrome 
                #    are all the same char
                if len(pal) == 2:
                    # While we have chars on the right and the last char in 
                    #    the palindrome matches the first char on the right, 
                    #    build up the palindrome from those chars
                    while right and pal[-1] == right[-1]:
                        pal.append(right.pop().lower())
                # If the palindrome we have built is longer than the current
                #    longest palindrome, replace current max palindrome
                #    with the one we just built
                if len(pal) > len(maxpal):
                    maxpal = ''.join(pal)
            # This is the case where the middle letter of an odd-length
            #    palindrome differs from the two letters on either side of it
            elif len(pal) == 0 and len(a) > 2:
                # So we didn't find an even-length palindrome at the first
                #    two letters (the index being one of them). Let's pretend
                #    we did and start building the palindrome from the char
                #    at the index (last char on the reversed right)
                pal.append(rc)
                # Put the left char back into the left string for comparison
                #    with the char to the right of the index when we go back
                #    to the top of the loop
                left.append(lc)
                # Make these equal so the loop-check will succeed
                lc = rc
        # Stop checking at the index of "a" which is the lesser of:
        #   - The current max-index
        #   - Length of "a" minus half of the length of maxpal plus 1        
        maxchk = min(maxchk, len(a)-int((len(maxpal)+1)/2))
        ndx += 1
    return maxpal

''' Find minimum spanning tree in graph stored as adjacency lists '''
def min_span(G):
    if len(G) == 0: return None    
    # pick a starting vertex by arbitrarily selecting the minimum vertex #
    start_v = min(G)
    # create a dictionary for the minimum spanning tree with starting vertex
    mst = {start_v: []}
    
    while True:
        # Get edges of vertices in mst
        for frv, edges in [(frv, edges) for frv, edges in G.items() 
        if frv in mst]:
            # get candidate edges linked to vertices not in mst
            candidate_edges = [(cost, frv, tov) for tov, cost in edges
            if tov not in mst]
        # if none of the mst vertices have edges to vertices not in mst,
        #   we're done
        if not candidate_edges:
            break
        # get lowest cost edge from candidate edges
        cost, from_v, to_v = min(candidate_edges)
        # add lowest cost edge to mst
        mst[from_v].append((to_v, cost))
        mst[to_v] = [(from_v, cost)]
    
    return mst

''' Find least common ancestor of two nodes in a binary search tree stored
as an adjancey matrix'''
def lca(bst, root, n1, n2):
    ndx = root
    
    while ndx is not None:
        # if the index is between n1 & n2 then it must be the least common
        #   ancestor - we're done, return ndx
        if min(n1, n2) <= ndx <= max(n1, n2):
            return ndx
        # if the ndx is greater than both n1 & n2, check the left child
        elif ndx > max(n1, n2):
            left = None 
            for left_ndx, val in enumerate(bst[ndx]):
                if val == 1 and left_ndx <= ndx:
                    left = left_ndx
            ndx = left
        # if the ndx is less than both n1 & n2, check the right child
        elif ndx < min(n1, n2):
            right = None
            for right_ndx, val in enumerate(bst[ndx]):
                if val == 1 and right_ndx >= ndx:
                    right = right_ndx
            ndx = right

''' Get value of node "lag" nodes from the end of the singly-linked list '''
def lag_node(linked_list, lag):
    if linked_list is None: 
        return None
    
    maxnodenum = 0
    
    node = linked_list.head
    # loop through the nodes, incrementing maxnodenum
    while node:
        maxnodenum += 1
        node = node.next
    
    # if the length of linked-list isn't at least lag+1, return None
    if maxnodenum - lag <= 0:
        return None
    else:
    # Get the value of "lag" node by running through the list again until 
    #    "lag" node from the end
        nodecount = 1        
        node = linked_list.head
        while node:
            if maxnodenum - lag == nodecount:
                return node.data
            nodecount += 1
            node = node.next

def alg1():
    print "Alg-1 result 1: {}".format(chars_in("Fred Flintstone", "fred"))
    print "Alg-1 result 2: {}".format(chars_in("Barney Rubble", "bubble"))
    print "Alg-1 result 3: {}".format(chars_in("Barney Rubble", ""))
    print "Alg-1 result 4: {}".format(chars_in("", "xyz"))

def alg2():
    print "Alg-2 result 1: {}".format(pal("adda"))
    print "Alg-2 result 2: {}".format(pal("bbaddayyzzyycvc"))
    print "Alg-2 result 3: {}".format(pal(""))
    print "Alg-2 result 4: {}".format(pal("abcdefg"))
    print "Alg-2 result 5: {}".format(pal("gifyfig"))

def alg3():
    test_al =  {'A': [('B', 2)],
                'B': [('A', 2), ('C', 5)], 
                'C': [('B', 5)]}

    print "Alg-3 result 1: {}".format(min_span(test_al))

    test_al =  {'A': [('B', 2), ('C', 1)],
                'B': [('A', 2), ('C', 5)], 
                'C': [('B', 5), ('A', 1)]}

    print "Alg-3 result 2: {}".format(min_span(test_al))

    test_al =  {'A': [('B', 2), ('C', 1), ('D', 5)],
                'B': [('C', 5), ('A', 2), ('D', 3)], 
                'C': [('B', 5), ('A', 1)],
                'D': [('A', 5), ('B', 3)]}

    print "Alg-3 result 3: {}".format(min_span(test_al))

    test_al =  {}

    print "Alg-3 result 4: {}".format(min_span(test_al))

def alg4():
    test_bst = [
        [0,1,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [1,0,0,0,1],
        [0,0,0,0,0]    
    ]
    
    print "Alg-4 result 1: {}".format(lca(test_bst,3,1,4))

    test_bst = [
        [0,0,0,0,0,0,0],
        [1,0,1,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,1,0,0,0,1,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,1,0,1],
        [0,0,0,0,0,0,0],    
    ]
    
    print "Alg-4 result 2: {}".format(lca(test_bst,3,4,6))
    print "Alg-4 result 3: {}".format(lca(test_bst,3,0,1))
    print "Alg-4 result 4: {}".format(lca(test_bst,3,4,5))
    print "Alg-4 result 5: {}".format(lca(test_bst,3,1,6))

def alg5():
    class Node(object):
        def __init__(self, data):
            self.data = data
            self.next = None
    
    class LinkedList(object):
        def __init__(self, head=None):
            self.head = head
            
        def append(self, data):
            if not self.head:
                self.head = Node(data)
            else:
                node = self.head
                while node.next:
                    node = node.next
                node.next = Node(data)
    
    linked_list = LinkedList(Node(1))
    linked_list.append(2)
    linked_list.append(3)
    linked_list.append(4)
    linked_list.append(5)
        
    print "Alg-5 result 1: {}".format(lag_node(linked_list, 1))
    print "Alg-5 result 2: {}".format(lag_node(linked_list, 2))
    print "Alg-5 result 3: {}".format(lag_node(linked_list, 4))
    print "Alg-5 result 4: {}".format(lag_node(linked_list, 6))
    print "Alg-5 result 5: {}".format(None, 0)    
    
def main():
    alg1()
    alg2()
    alg3()
    alg4()
    alg5()

if __name__ == '__main__':
    main()