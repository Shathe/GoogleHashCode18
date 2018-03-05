import numpy as np
import Car
import Ride

class Extractor:
    """A simple example class"""
    def __init__(self, cars, name):
        self.cars=cars
        self.name=name

    # Write solution
    def write(self):
    	file = open(self.name+'.out', 'w') 
    	for car in self.cars:
    		file.write(str(len(car.rides)) + ' ')
    		for ride in car.rides:
    			file.write(str(ride.id) + ' ')

	    	file.write('\n')

