import Car
import Ride
import numpy as np
class Loader:

    def __init__(self, file):
    	self.file=file

    # Read file in
    def readfile(self):
        with open(self.file, 'r') as file:
            line1 = file.readline()
            line1Vec = line1.strip().split()
            ridesList = []
            n = 0
            for txt in file:
                ls = txt.strip().split()
                ride = Ride.Ride(n, [int(ls[0]),int(ls[1])], [int(ls[2]), int(ls[3])], int(ls[4]), int(ls[5]))
                ridesList = ridesList + [ride]
                n = n + 1

            return ridesList, int(line1Vec[0]), int(line1Vec[1]), int(line1Vec[2]),int(line1Vec[3]), int(line1Vec[4]), int(line1Vec[5])

