import time
import random
# Manhatan distance
def distance_to_from(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1])



class Solution:
	"""A simple example class"""
	def __init__(self, cars, rides_no_assinged, bonus):
		self.cars=cars
		self.rides_no_assinged=rides_no_assinged
		self.bonus = bonus

	def add_ride_into_car(self, index_car, ride):
		i = 0
		# Get the position the first it can fit (el time_init del ride es menor que el time_final del siguiente en la lista)
		# get the last position to fit: ride.time_final es mayor que el start de la siguiente en la lista
		index_min = 0
		index_max = 0
		while i < len(self.cars[index_car].rides):

			if ride.time_init >= self.cars[index_car].rides[i].time_final:
				index_min = i + 1

			if ride.time_final <= self.cars[index_car].rides[i].time_init:
				index_max = i + 1

			i = i + 1


		index = random.randint(index_min, index_max)
		self.cars[index_car].rides.insert(index, ride)




	def add_no_assigned_ride(self):
		if len(self.rides_no_assinged) > 0:
			# If there is a no assigned ride

			car_index = random.randint(0, len(self.cars) - 1)
			ride = random.choice(self.rides_no_assinged)
			# Add it into a fittable position
			self.add_ride_into_car(index_car, ride)

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

				# catch only if the car is able to make it in time
				if time_to_start_real + distance <= ride_next.time_final:

					car_next.position=ride_next.position_final
					car_next.step_available=time_to_start_real + distance

					# Calculate score
					score_final = score_final + distance
					if time_to_start_real == time_to_start_expected:
						score_final = score_final + self.bonus 


		# print('seconds to calculate score: ' + str(time.time()-first))
		return score_final


	def mutate(self):
		functions = [self.add_no_assigned_ride, self.swap_rides, self.from_car_to_unassigned]

		func = random.choice(functions)
		func()


def next_generation(solutions, size_next_gen=100, mutations_per_solution_max=50)
# Tienes de 1 a N soluciones
# ordenar por score
# mutar a todas las soluciones: gaurdandote la antigua generacion, generando mas de las que hay y ademas, mutando mas veces a las mejores que a las peores
# ordenar por score y devovler las M mejores
# hacer de 0 a X mutaciones por solucion

