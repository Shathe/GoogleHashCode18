import Loader
import Ride
import Car
import Extractor
import numpy as np
import random
import math

# Manhatan distance
def distance_to_from(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Por hacer
def value_solution(cars):
	pass

files=['a_example','b_should_be_easy','c_no_hurry','d_metropolis','e_high_bonus']

for file in files:
	print(file)

	loader = Loader.Loader(file+'.in')
	# Init variables and rides
	[rides, rows, cols, carsN, ridesN, bonus, steps] = loader.readfile()
	# Init cars
	cars = []
	for i in range(carsN):
		car = Car.Car()
		cars = cars + [car]





	while len(rides) > 0 :
		#coger siguiente coche
		cars.sort(key=lambda x:  x.step_available, reverse=False)
		car_next = cars[0]

		# Asignar siguiente tarea disponible al coche
		rides.sort(key=lambda x: x.time_init + distance_to_from(car_next.position, x.position_init), reverse=False)
		ride_next = rides[0]
		rides.pop(0)				

		# Asignar al coche su posicion siguiente
		car_next.position=ride_next.position_final
		time_to_go = distance_to_from(car_next.position, ride_next.position_init)
		time_to_start = ride_next.time_init 
		# Siguiente momento diponible es la suma de max(lo que le cueste llegar o cuando empiece la tarea) es decir, de cuadno empieza la tarea
		# y a eso le sumas a la distancia a recorrer del ride
		car_next.step_available=max(time_to_start, time_to_go) + distance_to_from(ride_next.position_init, ride_next.position_final)
		car_next.rides=car_next.rides + [ride_next]





	ex = Extractor.Extractor(cars, file)
	ex.write()

# Creo que eta solucion da 40496957: 40.5 M

