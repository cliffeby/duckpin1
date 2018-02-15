# Pins [(606, 187), (331, 188), (469, 188), (188, 190), (549, 206), (397, 207), (243, 208), (483, 231), (312, 232), (401, 262)]
#Pins [(605, 164), (186, 165), (471, 165), (549, 184), (395, 185), (241, 186), (484, 210), (401, 243)]
mpins = [(606, 187), (331, 188), (469, 188), (188, 190), (549, 206), (397, 207), (243, 208), (483, 231), (312, 232), (401, 262)]
bpins = [(605, 164), (186, 165), (471, 165), (549, 184), (395, 185), (241, 186), (484, 210), (401, 262)]
if len(mpins) == 10:
    masterPinLocation = mpins
for index, pin in enumerate(masterPinLocation):
    print (index, pin)
print ('______________')
A = sorted(masterPinLocation, key = lambda k: [-k[1], k[0]])
B = sorted(bpins, key = lambda k: [-k[1], k[0]])
dec = [512,256,128,64,32,16,8,4,2,1]
print (A,B)

 ##
pattern =0
for pin10 in B:
    for index, pin in enumerate(A):
        diff = (pin10[0]-pin[0])**2 + (pin10[1]-pin[1])**2
        if (diff < 800):
            print(index,pin10,pin)
            pattern = pattern + dec[index]
            print(pattern,bin(pattern))
            print("FFFF", str(bin(pattern)))
print(str(bin(pattern))[3:7])