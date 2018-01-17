# Template matching returns two arrays in the 'loc' variable.  The following
# line is a sample from print(loc)
# loc =(array([100, 200, 300, 400, 374, 374, 374], dtype=int32), array([10, 20, 30, 40, 302, 303, 304], dtype=int32))
# Use the following code to understand - for pt in zip(*loc[::-1]): 

import numpy as np
loc =(([100, 200, 300, 400, 374, 374, 374]), ([10, 20, 30, 40, 302, 303, 304]))
print (loc)
print (loc[::-1])
print (*loc[::-1])
for pt in zip(*loc[::-1]):      
    print (pt)
# 
# Typical y,x tuple of 10 pin locations.  Sort by Y(descending) then X
mpins = [(606, 187), (331, 188), (469, 188), (188, 190), (549, 206), (397, 207), (243, 208), (483, 231), (312, 232), (401, 262)]
A = sorted(mpins, key = lambda k: [-k[1], k[0]])
print (A)

B =[(1, 0b1000000000),(2,0b0100000000),(3,0b0010000000),(4,0b000100000),(5,0b0000100000), \
 (6,0b0000010000),(7,0b0000001000),(8,0b0000000100),(9,0b0000000010),(10,0b0000000001)]
print (B)

AxB = [(401, 262), (312, 232), (483, 231), (243, 208), (397, 207), (549, 206), (188, 190), (331, 188), (469, 188), (606, 187)], \
 [(1, 0b1000000000),(2,0b0100000000),(3,0b0010000000),(4,0b000100000),(5,0b0000100000), \
 (6,0b0000010000),(7,0b0000001000),(8,0b0000000100),(9,0b00000000010),(10,0b0000000001)]
C = A+B
print ('C', C)
print (C[0][0],C[0][1], C[10][0], C[10][1])

D = tuple(tuple(map(tuple, sub)) for sub in AxB)
print ('D', D)
print (D[0][0][0], D[0][0][1], D[1][0][0], D[1][0][1])
for pt in zip(*D[::1]):      
    print (pt)