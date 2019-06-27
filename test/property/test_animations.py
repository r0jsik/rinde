import unittest

from rinde.property import NumberProperty
from rinde.property.animation import Animation
from rinde.property.animation import Animations


def animate():
	for i in range(1000):
		Animations.update_all()


class AnimationsTest(unittest.TestCase):
	def test_parallel(self):
		property_1 = NumberProperty(98)
		property_1.animate_to(615)
		
		property_2 = NumberProperty(91)
		property_2.animate_by(-881)
		
		property_3 = NumberProperty(127)
		property_3.animate_to(92)
		
		animate()
		
		assert property_1.get() == 615
		assert property_2.get() == -790
		assert property_3.get() == 92
	
	def test_abortion(self):
		property_1 = NumberProperty(-512)
		property_2 = NumberProperty(162)
		
		animation_1 = Animation(property_1, 919, lambda:(), 2)
		animation_1.start()
		
		animation_2 = Animation(property_2, -61, lambda: Animations.remove(animation_1), 3)
		animation_2.start()
		
		animate()
		
		assert property_1.get() != 919
	
	def test_queue(self):
		property_1 = NumberProperty(15)
		property_2 = NumberProperty(66)
		property_3 = NumberProperty(71)
		
		start_animation_3 = lambda: property_3.animate_to(52)
		start_animation_2 = lambda: property_2.animate_to(88, start_animation_3)
		
		property_1.animate_to(32, start_animation_2)
		
		animate()
		
		assert property_1.get() == 32
		assert property_2.get() == 88
		assert property_3.get() == 52


class AnimationTest(unittest.TestCase):
	def test_animate_to(self):
		property = NumberProperty(301)
		property.animate_to(28)
		
		animate()
		
		assert property.get() == 28
	
	def test_animate_by(self):
		property = NumberProperty(116)
		property.animate_by(1009)
		
		animate()
		
		assert property.get() == 1125
	
	def test_callback(self):
		property_1 = NumberProperty(918)
		property_2 = NumberProperty(13)
		
		property_1.animate_to(57, lambda: property_2.set(118))
		animate()
		
		assert property_2.get() == 118
	
	def test_high_speed(self):
		property = NumberProperty(415)
		property.animate_to(3042, speed=21)
		
		animate()
		
		assert property.get() == 3042
	
	def test_low_speed(self):
		property = NumberProperty(82)
		property.animate_by(712, speed=1)
		
		animate()
		
		assert property.get() == 794
	
	def test_zero_speed(self):
		property = NumberProperty(-18)
		property.animate_to(691, speed=0)
		
		animate()
		
		assert property.get() == -18
