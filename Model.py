import Loader
import Ride
import Car
import Extractor
import numpy as np
import random
import math
import Solution
import copy
import os.path
import pickle 




# Manhatan distance
def distance_to_from(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1])



files=['e_high_bonus','d_metropolis','c_no_hurry','b_should_be_easy','a_example']

old_best_scores= [21465945, 10296018, 15793338, 176877, 10]
best_scores= [21465945, 10296018, 15793338, 176877, 10]
best_global = 45664825
suma_total = 0
solutions = []
index_total=1
veces_mejorado = 0

load_from_numpy = False
genetic = False
while True:
	index_file = 0
	for file, score in zip(files, best_scores):
		print(file)
		solution = None

		if load_from_numpy and os.path.exists(file+'.obj'):
			filehandler = open(file+'.obj', 'r') 
			solution = pickle.load(filehandler)
		else:
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
					# coger aleatoria mente uno de los mejores coches (no siempre el mejor para probar varcioens buenas)
					random_number = random.randint(0,4)
					coger_otro_coche = random_number != 0
					if next_index_car + random_number >= len(cars):
						random_number = 0
						random_number = False

					car_next = cars[next_index_car + random_number]

					# Ahora se ordena para la tarea que empezarias antes
					rides.sort(key=lambda x:max(distance_to_from(car_next.position, x.position_init) + car_next.step_available, x.time_init ) , reverse=False)
					
					if next_index_ride < len(rides):

					# coger aleatoria mente uno de los mejores coches (no siempre el mejor para probar varcioens buenas)

						random_number = random.randint(0,0)
						if next_index_ride + random_number >= len(rides):
							random_number = 0

						ride_next = rides[next_index_ride + random_number]
						rides.pop(next_index_ride + random_number)				

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
						elif coger_otro_coche == 0:
							#esta tarea se descarta
							rule_out_rides = rule_out_rides + [ride_next]

					elif coger_otro_coche == 0:
						#Esto paasara cuadno un coche no pueda hacer ninguna tarea
						next_index_car = next_index_car + 1

				else:
					fin = True


			solution = Solution.Solution(cars, rule_out_rides, bonus, steps)
		if genetic:
			solutions =  solutions + [solution]

			print('genetic algorithm:')

			solution = Solution.genetic_alg([solution], num_generations=1000, max_size_gen=500, size_final_gen=50, mutations_per_solution_max=50, name=file)

		score_new = solution.get_score()
		suma_total = suma_total + score_new
		print('solution score ' + str(score_new))
		if score_new > score:
			print('NUEVA MEJORA DE PUNTUACION EN EL FICHERO: ' + file)
			best_scores[index_file]=score_new
			ex = Extractor.Extractor(solution.cars, file)
			ex.write()
			veces_mejorado = veces_mejorado + 1

		index_file =  index_file + 1

	print('score: ' + str(suma_total/1000000.0) + ' M')
	if best_global < suma_total:
		print('Has mejorado el algoritmo!')

	print('llevas mejoradas veces: ' + str(veces_mejorado) + '/' + str(index_total))
	print('mejora: ' + str(sum(best_scores)-sum(old_best_scores)))
	suma_total=0
	index_total=index_total+1


	

'''
IDEAS:

dar peso el time_ini * BONUS y a la distancia * distancia * 2*(steps-time_final)/steps


'''
