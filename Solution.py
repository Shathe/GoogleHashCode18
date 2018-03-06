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

	def add_no_assigned_ride(self):
		if len(self.rides_no_assinged) > 0:
			car = random.choice(self.cars)
			ride = random.choice(self.rides_no_assinged)
			car.rides = car.rides + [ride]

	def swap_rides(self):
		pass

	def from_car_to_unassigned():
		pass

	def shift_rides():
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




