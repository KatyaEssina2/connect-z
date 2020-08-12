CONNECTZ

CONSIDERATIONS:
Approaching this problem I had 2 original ideas:

1) Create a matrix to represent the grid 
2) Model the the game as Objects

I chose route 2 because I think it is neater and conceptually easier to understand. I really enjoyed the Object design.

CHALLENGES:
- I reached the Python default max recursion depth pretty fast
- I tried implementing the solution to count the winning streak iteratively, but the solution was clunky and slow.
- I implemented an LRU cache to get around the recursion depth limit and cache streak calculations from nodes, although I have set the max size parameter=None which could cause memory errors with really huge files.


FUTURE IMPROVEMENTS
- use numpy/pandas and switch matrix modelling of game (option 1 in considerations) for highly optimised matrix/dataframe processing. I could use slice methods to evaluate the horizontal and vertical directions for a streak, and maybe create a custom slice to count on the diagonal.