import time
import random
import numpy as np
import Extractor
import copy
import pickle 
import math 

# Manhatan distance
def distance_to_from(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1])



class Solution:
	"""A simple example class"""
	def __init__(self, cars, rides_no_assinged, bonus, steps):
		self.cars=cars
		self.rides_no_assinged=rides_no_assinged
		self.bonus = bonus
		self.steps=steps

	def count_rides(self):
		i = 0
		for car in self.cars:
			for ride in car.rides:
				i=i+1
		for ride in self.rides_no_assinged:
			i = i +1
		return i

	def reorder(self):
		
		car_index = random.randint(0, len(self.cars) - 1)
		tries=15
		while(tries > 0 and len(self.cars[car_index].rides) < 2):
			car_index = random.randint(0, len(self.cars) - 1)
			tries = tries - 1

		if tries != 0:
			ride_index = random.randint(0, len(self.cars[car_index].rides) - 2)
			ride1=copy.deepcopy(self.cars[car_index].rides[ride_index])
			ride2=copy.deepcopy(self.cars[car_index].rides[ride_index+1])
			self.cars[car_index].rides[ride_index]=ride2
			self.cars[car_index].rides[ride_index+1]=ride1

	def add_ride_into_car(self, index_car, ride):
		i = 0
		# Get the position the first it can fit (el time_init del ride es menor que el time_final del siguiente en la lista)
		# get the last position to fit: ride.time_final es mayor que el start de la siguiente en la lista
		index_min = 0
		index_max = 0
		while i < len(self.cars[index_car].rides):

			if ride.time_init >= self.cars[index_car].rides[i].time_final:
				index_min = i + 1

			if ride.time_final >= self.cars[index_car].rides[i].time_init:
				index_max = i + 1

			i = i + 1


		index = random.randint(index_min, index_max)
		self.cars[index_car].rides.insert(index, ride)




	def add_no_assigned_ride(self):
		if len(self.rides_no_assinged) > 0:
			# If there is a no assigned ride
			ride_index = random.randint(0, len(self.rides_no_assinged) - 1)
			car_index = random.randint(0, len(self.cars) - 1)
			# Add it into a fittable position
			self.add_ride_into_car(car_index, self.rides_no_assinged[ride_index])
			self.rides_no_assinged.pop(ride_index)

	def swap_rides(self):
		# get two cars (indexes)
		car_index_1 = random.randint(0, len(self.cars) - 1)
		car_index_2 = random.randint(0, len(self.cars) - 1)
		while car_index_2 == car_index_1:
			car_index_2 = random.randint(0, len(self.cars) - 1)

		car1 = self.cars[car_index_1]
		car2 = self.cars[car_index_2]

		# If they have rides
		if len(car1.rides) > 0 and len(car2.rides) > 0:
			# Get two random rides from them
			ride2_index = random.randint(0, len(car2.rides) - 1)
			ride1_index = random.randint(0, len(car1.rides) - 1)
			ride1 = car1.rides[ride1_index]
			ride2 = car2.rides[ride2_index]
			car1.rides.pop(ride1_index)
			car2.rides.pop(ride2_index)

			#swap them
			self.add_ride_into_car(car_index_1, ride2)
			self.add_ride_into_car(car_index_2, ride1)


			

	def from_car_to_unassigned(self):
		car = random.choice(self.cars)
		tries = len(self.cars)
		while len(car.rides) == 0 and tries >= 0:
			car = random.choice(self.cars)
			tries = tries - 1

		if len(car.rides) > 0: 
			ride_index = random.randint(0, len(car.rides) - 1)
			self.rides_no_assinged = self.rides_no_assinged + [car.rides[ride_index]]
			car.rides.pop(ride_index)



	def shift_rides(self):
		pass


	#Tarda como mucho 0.001 segundo
	def get_score(self):
		# return sum(c.score for c in self.cars)
		score_final = 0
		first=time.time()
		for car_next in self.cars:
			car_next.position=[0,0]
			car_next.step_available=0
			#simulate rides and calculate score
			for ride_next in car_next.rides:
				time_to_go = distance_to_from(car_next.position, ride_next.position_init) + car_next.step_available
				time_to_start_expected = ride_next.time_init 
				time_to_start_real = max(time_to_go, time_to_start_expected ) 
				distance = distance_to_from(ride_next.position_init, ride_next.position_final)

				# catch only if the car is able to make it in time steps
				if time_to_start_real + distance <= ride_next.time_final and time_to_start_real + distance <= self.steps  :

					car_next.position=ride_next.position_final
					car_next.step_available=time_to_start_real + distance

					# Calculate score
					score_final = score_final + distance
					if time_to_start_real == time_to_start_expected:
						score_final = score_final + self.bonus 


		# print('seconds to calculate score: ' + str(time.time()-first))
		return score_final


	def mutate(self):
		functions = [self.add_no_assigned_ride, self.swap_rides, self.from_car_to_unassigned, self.reorder]

		func = random.choice(functions)
		func()


def next_generation(solutions, max_size_gen=1000, size_final_gen=100, mutations_per_solution_max=50):

	#Solutions must be a list
	#solutions.sort(key=lambda x:  x.get_score(), reverse=True) # Mas altas primero
	new_gen_solutions = copy.deepcopy(solutions)

	# quedarte solo la mitad de los mejores de la antrior gneracion
	new_gen_solutions = new_gen_solutions[:int(size_final_gen/4)+1]

	#llenar scores
	scores_solutions = []
	for solution in new_gen_solutions:
		scores_solutions = scores_solutions + [solution.get_score()]

	for step in xrange(max_size_gen):

		# get a random index. But the first elemetns will have more probabilities
		index_solution = min(random.randint(0, len(solutions)-1), random.randint(0, len(solutions)-1))
		solution_to_mutate = copy.deepcopy(solutions[index_solution])

		# la mitad de veces, lo que se hara ser mutaciones aleatorias sin mirar hasta lelgar al final pero la otra mitad, 
		# si una mutacion empeora, vuelves atras
		# Mute N times

		for times in xrange(random.randint(1, mutations_per_solution_max)):
			solution_to_mutate.mutate()
		
			
		#no repetir soluciones 
		if solution_to_mutate.get_score()  not in scores_solutions:
			new_gen_solutions = new_gen_solutions + [solution_to_mutate]

	new_gen_solutions.sort(key=lambda x:  x.get_score(), reverse=True) # Mas altas primero
	new_gen_solutions = new_gen_solutions[0:size_final_gen]

	return new_gen_solutions[0:size_final_gen]



def genetic_alg(next_gen, num_generations=200, max_size_gen=1000, size_final_gen=100, mutations_per_solution_max=50, name=""):
	print('start solution:' + str(next_gen[0].get_score()))
	for times in xrange(num_generations):
		next_gen = next_generation(next_gen, max_size_gen, size_final_gen, mutations_per_solution_max)
		print('iter :' + str(times) + ', name: ' +name)
		print('best solution:' + str(next_gen[0].get_score()))
		print('worst solution:' + str(next_gen[size_final_gen-1].get_score()))
		print('start solution:' + str(next_gen[0].get_score()))
		file_write = open(name + '.obj', 'w') 
		pickle.dump(next_gen[0], file_write)
		ex = Extractor.Extractor(next_gen[0].cars, name)
		ex.write()

	return next_gen[0]