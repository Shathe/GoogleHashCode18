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

suma = 0
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



	next_index_ride = 0
	next_index_car = 0
	fin = False
	while len(rides) > 0 and not fin:
		#coger siguiente coche
		cars.sort(key=lambda x:  x.step_available, reverse=False)
		if next_index_car < len(cars):
			car_next = cars[next_index_car]

			# Asignar siguiente tarea disponible al coche
			rides.sort(key=lambda x: x.time_init + distance_to_from(car_next.position, x.position_init), reverse=False)
			if next_index_ride < len(rides):
				ride_next = rides[next_index_ride]
				rides.pop(next_index_ride)				

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
					if time_to_start_real == time_to_start_expected:
						suma = suma + bonus
					# actualizar valor de la sigueitne tarea a mirar, ya sera otro coche
					next_index_ride = 0


				elif car_next.step_available < ride_next.time_init :
					#Aun se podria coger esta por otro coche puede que si
					rides = rides + [ride_next]
					# y el mismo coche se que cogera, probar con la siguiente tarea a ver si podra
					next_index_ride = next_index_ride + 1

			else:
				#Esto paasara cuadno un coche no pueda hacer ninguna tarea
				next_index_car = next_index_car + 1

		else:
			fin = True
		if len(rides) % 300 == 0:
			print(str(len(rides)))



	ex = Extractor.Extractor(cars, file)
	ex.write()

print('score: ' + str(suma/1000000.0) + ' M')
# Creo que eta solucion da 40496957: 40.5 M


'''
IDEAS:

dar peso el time_ini * BONUS y a la distancia * distancia * 2*(steps-time_final)/steps


'''
