import Loader
import Ride
import Car
import Extractor
import numpy as np
import random
import math
import Solution
# Manhatan distance
def distance_to_from(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1])



files=['a_example','b_should_be_easy','c_no_hurry','d_metropolis','e_high_bonus']
files=['b_should_be_easy']

best_scores=[10, 176877, 15777925, 10296018, 21465945]
best_global = 45664825
suma_total = 0
solutions = []

for file, score in zip(files, best_scores):
	print(file)

	loader = Loader.Loader(file+'.in')
	# Init variables and rides
	[rides, rows, cols, carsN, ridesN, bonus, steps] = loader.readfile()
	# Init cars
	cars = []
	for i in range(carsN):
		car = Car.Car()
		cars = cars + [car]

	rule_out_rides = []

	next_index_ride = 0
	next_index_car = 0
	fin = False
	while len(rides) > 0 and not fin:
		#coger siguiente coche
		cars.sort(key=lambda x:  x.step_available, reverse=False)
		if next_index_car < len(cars):
			car_next = cars[next_index_car]

			# Asignar siguiente tarea disponible al coche
			rides.sort(key=lambda x:max(distance_to_from(car_next.position, x.position_init) + car_next.step_available, x.time_init ) , reverse=False)
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

					# actualizar valor de la sigueitne tarea a mirar, ya sera otro coche
					next_index_ride = 0


				elif car_next.step_available < ride_next.time_init :
					#Aun se podria coger esta por otro coche puede que si
					rides = rides + [ride_next]
					# y el mismo coche se que cogera, probar con la siguiente tarea a ver si podra
					next_index_ride = next_index_ride + 1
				else:
					#esta tarea se descarta
					rule_out_rides = rule_out_rides + [ride_next]

			else:
				#Esto paasara cuadno un coche no pueda hacer ninguna tarea
				next_index_car = next_index_car + 1

		else:
			fin = True


	solution = Solution.Solution(cars, rule_out_rides, bonus)
	solutions =  solutions + [solution]



	score_new = solution.get_score()
	suma_total = suma_total + score_new
	print('solution score ' + str(score_new))
	if score_new > score:
		print('NUEVA MEJORA DE PUNTUACION EN EL FICHERO: ' + file)

	ex = Extractor.Extractor(cars, file)
	ex.write()

print('score: ' + str(suma_total/1000000.0) + ' M')
if best_global < suma_total:
	print('Has mejorado el algoritmo!')




	

'''
IDEAS:

dar peso el time_ini * BONUS y a la distancia * distancia * 2*(steps-time_final)/steps


'''
