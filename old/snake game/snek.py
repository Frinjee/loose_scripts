import pygame as pg
import random, os
from pygame.math import Vector2
from sys import exit

class SNAKE:
	def __init__(self):
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] # all the blocks that constitute our snake
		self.direction = Vector2(0, 0)
		self.new_part = False
		
		self.head_up = pg.image.load('gfx/head_up.png').convert_alpha()
		self.head_down = pg.image.load('gfx/head_down.png').convert_alpha()
		self.head_right = pg.image.load('gfx/head_right.png').convert_alpha()
		self.head_left = pg.image.load('gfx/head_left.png').convert_alpha()
		
		self.tail_up = pg.image.load('gfx/tail_up.png').convert_alpha()
		self.tail_down = pg.image.load('gfx/tail_down.png').convert_alpha()
		self.tail_right = pg.image.load('gfx/tail_right.png').convert_alpha()
		self.tail_left = pg.image.load('gfx/tail_left.png').convert_alpha()

		self.body_vertical = pg.image.load('gfx/body_vertical.png').convert_alpha()
		self.body_horizontal = pg.image.load('gfx/body_horizontal.png').convert_alpha()

		self.body_tr = pg.image.load('gfx/body_tr.png').convert_alpha()
		self.body_tl = pg.image.load('gfx/body_tl.png').convert_alpha()
		self.body_br = pg.image.load('gfx/body_br.png').convert_alpha()
		self.body_bl = pg.image.load('gfx/body_bl.png').convert_alpha()

		self.munch_sfx = pg.mixer.Sound('sfx/munch.mp3')

	def draw_snake(self):
		self.update_head_gfx()
		self.update_tail_gfx()

		for index, part in enumerate(self.body):
			snake_x_pos = int(part.x * cell_size)
			snake_y_pos = int(part.y * cell_size)
			snake_rect = pg.Rect(snake_x_pos, snake_y_pos, cell_size, cell_size)

			if index == 0: screen.blit(self.head, snake_rect)
			elif index == len(self.body) - 1: screen.blit(self.tail, snake_rect)
			else:
				prev_part = self.body[index + 1] - part
				next_part = self.body[index - 1] - part

				if prev_part.x == next_part.x: screen.blit(self.body_vertical, snake_rect)
				elif prev_part.y == next_part.y : screen.blit(self.body_horizontal, snake_rect)
				else: 
					if prev_part.x == -1 and next_part.y == -1 or prev_part.y == -1 and next_part.x == -1:
						screen.blit(self.body_tl, snake_rect)
					elif prev_part.x == -1 and next_part.y == 1 or prev_part.y == 1 and next_part.x == -1:
						screen.blit(self.body_bl, snake_rect)
					elif prev_part.x == 1 and next_part.y == -1 or prev_part.y == -1 and next_part.x == 1:
						screen.blit(self.body_tr, snake_rect)
					elif prev_part.x == 1 and next_part.y == 1 or prev_part.y == 1 and next_part.x == 1:
						screen.blit(self.body_br, snake_rect)
		
	def update_head_gfx(self):
		head_pos_relation = self.body[1] - self.body[0]

		if head_pos_relation == Vector2(1,0): self.head = self.head_left
		elif head_pos_relation == Vector2(-1,0): self.head = self.head_right
		elif head_pos_relation == Vector2(0,1): self.head = self.head_up
		elif head_pos_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_gfx(self):
		tail_pos_relation = self.body[-2] - self.body[-1]

		if tail_pos_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_pos_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_pos_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_pos_relation == Vector2(0,-1): self.tail = self.tail_down

	def snake_movement(self):
		if self.new_part == True:
			body_cp = self.body[:]
			body_cp.insert(0, body_cp[0] + self.direction)
			self.body = body_cp
			self.new_part = False
		else:
			body_cp = self.body[:-1]
			body_cp.insert(0, body_cp[0] + self.direction)
			self.body = body_cp

	def add_body_part(self):
		self.new_part = True

	def play_sfx(self):
		self.munch_sfx.play()
	def reset(self):
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] 
		self.direction = Vector2(0, 0)

class FRUIT:
	def __init__(self):
		self.randomize()

	def draw_fruit(self):
		# create a rectangle + draw the rectangle
		fruit_x_pos = int(self.fruit_pos.x * cell_size)
		fruit_y_pos = int(self.fruit_pos.y * cell_size)
		fruit_rect = pg.Rect(fruit_x_pos, fruit_y_pos, cell_size, cell_size)
		screen.blit(fruit_gfx, fruit_rect)
		#pg.draw.rect(screen, (126, 166, 113), fruit_rect)

	def randomize(self):
		self.x = random.randint(0, cell_num - 1)
		self.y = random.randint(0, cell_num - 1)
		self.fruit_pos = Vector2(self.x, self.y)

class DRIVER:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.snake_movement()
		self.element_collision_check()
		self.snake_check()

	def draw_elements(self):
		self.draw_grass()
		self.draw_score()
		self.fruit.draw_fruit()
		self.snake.draw_snake()

	def element_collision_check(self):
		if self.fruit.fruit_pos == self.snake.body[0]:
			# reposition fruit & add new part to snake
			self.fruit.randomize()
			self.snake.add_body_part()
			self.snake.play_sfx()
			
			for part in self.snake.body[1:]:
				if part == self.fruit.fruit_pos:
					self.fruit.randomize()

	def snake_check(self):
		# check if snake is outside of screen or collides with itself
		if not 0 <= self.snake.body[0].x < cell_num or not 0 <= self.snake.body[0].y < cell_num:
			self.game_over()

		for part in self.snake.body[1:]:
			if part == self.snake.body[0]:
				self.game_over()

	def draw_grass(self):
		grass_hue = (61, 165, 185)

		for row in range(cell_num):
			if row % 2 == 0:
				for col in range(cell_num):
					if col % 2 == 0:
						grass_rect = pg.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
						pg.draw.rect(screen, grass_hue, grass_rect)
			else:
				for col in range(cell_num):
					if col % 2 != 0:
						grass_rect = pg.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
						pg.draw.rect(screen, grass_hue, grass_rect)

	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text, True, (0, 0, 0))
		score_x_pos = int(cell_size * cell_num - 60)
		score_y_pos = int(cell_num * cell_num - 40)

		score_rect = score_surface.get_rect(center = (score_x_pos, score_y_pos))
		score_fruit = pg.image.load(fruit_selector)
		score_fruit_rect = score_fruit.get_rect(midright = (score_rect.left, score_rect.centery))

		#score_bg_rect = pg.Rect(score_fruit_rect.left, score_fruit_rect.top, score_fruit_rect.width + score_rect.width, score_fruit_rect.height)
		#pg.draw.rect(screen, (0, 0, 0, 0), score_bg_rect)
		screen.blit(score_surface, score_rect)
		screen.blit(score_fruit, score_fruit_rect)

	def game_over(self):
		self.snake.reset()


pg.init()
clock = pg.time.Clock()

cell_size = 40
cell_num = 20
screen = pg.display.set_mode((cell_num * cell_size, cell_num * cell_size))

game_font = pg.font.Font('gfx/fonts/franchise.ttf', 25)
fruits = ['gfx/fruit.png', 'gfx/y_fruit.png', 'gfx/o_fruit.png']
fruit_selector = random.choice(fruits)
fruit_gfx = pg.image.load(fruit_selector).convert_alpha()

SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)

game_driver = DRIVER()
while True:
	# draw all elements
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			exit()
		if event.type == SCREEN_UPDATE:
			game_driver.update()
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_UP:
				if game_driver.snake.direction.y != 1:
					game_driver.snake.direction = Vector2(0, -1)
			if event.key == pg.K_RIGHT:
				if game_driver.snake.direction.x != -1:
					game_driver.snake.direction = Vector2(1, 0)
			if event.key == pg.K_DOWN:
				if game_driver.snake.direction.y != -1:
					game_driver.snake.direction = Vector2(0, 1)
			if event.key == pg.K_LEFT:
				if game_driver.snake.direction.x != 1:
					game_driver.snake.direction = Vector2(-1, 0)


	screen.fill((0, 255, 255))
	game_driver.draw_elements()
	pg.display.update()
	clock.tick(144) # frame rate


'''
	# display surface | only one 'canvas', displayed by default
	# Surfaces | multiple allowed, not displayed by default
	background_surface = pg.image.load('gfx/bg.png').convert_alpha()
	screen.blit(background_surface,(0,0))
	# create new surface, draw a rectangle around the surface and place in center of the screen to anchor surface
	test_surface = pg.Surface((100, 200))
	test_surface.fill((255, 255, 255))
	test_rectangle = test_surface.get_rect(center = (200, 250))
	#test_rectangle = pg.Rect(100, 200, 100, 100) # w, h, x, y

	# display surface here with blit, block image transfer
	
	screen.blit(test_surface, test_rectangle)
	test_rectangle.right += 1
	#pg.draw.rect(background_surface, pg.Color('black'), test_rectangle) # surface, color, rectangle
	for part in self.body:
	snake_x_pos = int(part.x * cell_size)
			snake_y_pos = int(part.y * cell_size)
			snake_rect = pg.Rect(snake_x_pos, snake_y_pos, cell_size, cell_size)
			pg.draw.rect(screen, (183, 111, 122), snake_rect)

'''