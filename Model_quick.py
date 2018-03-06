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
	for car in cars:
		for ride in car.ride:
			print(ride.id)
	pass

suma_total = 0
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

		#puede: - distance_to_from(x.position_init, x.position_final) o  - car_next.available_in
		#MEJORA max(distance_to_from(car_next.position, x.position_init) + car_next.step_available, x.time_init ) 
		rides.sort(key=lambda x: x.time_init  + distance_to_from(car_next.position, x.position_init) , reverse=False)
		ride_next = rides[0]
		rides.pop(0)				

		time_to_go = distance_to_from(car_next.position, ride_next.position_init) + car_next.step_available
		time_to_start_expected = ride_next.time_init 
		time_to_start_real = max(time_to_go, time_to_start_expected ) 
		distance = distance_to_from(ride_next.position_init, ride_next.position_final)


 


		# catch only if the car is able to make it in time
		if time_to_start_real + distance <= ride_next.time_final:
			# Asignar al coche su posicion siguiente
			car_next.position=ride_next.position_final
			car_next.step_available=time_to_start_real + distance
			car_next.rides=car_next.rides + [ride_next]

			# Calculate score
			suma = suma + distance
			car_next.score = car_next.score + distance
			if time_to_start_real == time_to_start_expected:
				suma = suma + bonus
				car_next.score = car_next.score + bonus

	suma_total = suma_total + sum(c.score for c in cars)


	ex = Extractor.Extractor(cars, file)
	ex.write()

print('score: ' + str(suma_total/1000000.0) + ' M')

'''
IDEAS:

dar peso el time_ini * BONUS y a la distancia * distancia * 2*(steps-time_final)/steps


'''
