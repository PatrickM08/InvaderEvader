from imagesclass import *
import math

# ENTITY CLASSES


class EntitiesAbstract(pygame.sprite.Sprite):
	def __init__(self, image):
		super().__init__()
		self.image = image
		self.image_copy = self.image
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.display = pygame.display.get_surface().get_rect()
		self.width = self.display.width
		self.height = self.display.height
		self.mouse_x_position, self.mouse_y_position = pygame.mouse.get_pos()

	# used to update entities position
	def update(self):
		self.rect.center = (self.x_position, self.y_position)

	# finds mouse position
	def find_mouse_position(self):
		self.mouse_x_position, self.mouse_y_position = pygame.mouse.get_pos()

	# finds a rotation angle of entity in relation to the players mouse position
	def find_rotation_angle(self):
		self.angle = math.atan2(self.mouse_y_position - self.y_position, self.mouse_x_position - self.x_position)
		self.x_distance = math.cos(self.angle)
		self.y_distance = math.sin(self.angle)
		self.angle = (180 / math.pi) * -self.angle - 90

	# rotates an image
	def rotate(self):
		self.image = pygame.transform.rotozoom(self.image_copy, int(self.angle),1).convert_alpha()
		self.rect = self.image.get_rect(center= (self.x_position, self.y_position))

	# reduces the health of the entity by a given amount of damage.
	def hit(self,damage):
		self.health -= damage
		if self.health <= 0:
			self.kill()

	# finds a vector based off the direction the player is moving.
	def find_movement_direction(self):
		self.movement_vector = pygame.math.Vector2((self.future_x - self.x_position, self.future_y - self.y_position))
		try:
			self.movement_vector = self.movement_vector.normalize()  # cannot normalize vector of zero (ValueError)
		except ValueError:
			self.movement_vector.x = 0
			self.movement_vector.y = 0
	

# player entity
class PlayerShip(EntitiesAbstract):
	def __init__(self, image, flashing_image):
		super().__init__(image)
		self.player_image = image
		self.x_position = self.width / 2
		self.y_position = self.height - 100
		self.velocity = 500
		self.scale = 1
		self.moving_down = False
		self.moving_up = False
		self.moving_right = False
		self.moving_left = False
		self.future_x = self.x_position
		self.future_y = self.y_position
		self.dashing = False
		self.health = 3
		self.flashing_countdown = 0
		self.flashing = False
		self.flashing_image = flashing_image
		
	# reduces the health of the player and starts the flashing countdown (invulnerability)
	def hit(self,damage):
		if self.health - damage < 0:
			self.health = 0
		else:
			self.health -= damage
		self.flashing_countdown = 60

	# checks whether the player is invulnerable and does the flashing animation.
	def vulnerable(self):
		if self.flashing_countdown > 0:
			self.flashing = True
		else:
			self.flashing = False

		# flashing animation
		if self.flashing and (self.flashing_countdown > 40 or self.flashing_countdown < 20):
			self.image = self.flashing_image
			self.image_copy = self.image
		else:
			self.image = self.player_image
			self.image_copy = self.image

		self.flashing_countdown -= 1

	# if the player is moving (pressing WASD) the respective functions are called.
	def move(self,delta_time):
		self.check_if_moving()
		self.get_velocity_scale()
		if self.moving_up:
			self.move_up(delta_time)

		if self.moving_down:
			self.move_down(delta_time)

		if self.moving_right:
			self.move_right(delta_time)

		if self.moving_left:
			self.move_left(delta_time)

	# checks if player is moving, if not the future position (used for dash) is changed
	def check_if_moving(self):
		if not(self.moving_up or self.moving_down):
			self.future_y = self.y_position
		if not(self.moving_right or self.moving_left):
			self.future_x = self.x_position
		if not(self.moving_up or self.moving_down or self.moving_left or self.moving_right):
			self.future_y = self.height
			# when the player is not moving the dash takes them backwards,
			# therefore we set the future_y to the bottom of the screen.

	# This scale is required because the velocity would increase when going diagonally.
	def get_velocity_scale(self):
		if (self.moving_up or self.moving_down) and (self.moving_right or self.moving_left):
			self.scale = 0.7071
		else:
			self.scale = 1

	# moves player up
	def move_up(self,delta_time):
		self.y_velocity = self.velocity*self.scale*delta_time
		if self.rect.top >= self.y_velocity:
			self.y_position -= self.y_velocity
			self.future_y = 0
		else:
			self.y_position = self.rect.height / 2

	# moves player down
	def move_down(self,delta_time):
		self.y_velocity = self.velocity*self.scale*delta_time
		if self.height - self.rect.bottom >= self.y_velocity:
			self.y_position += self.y_velocity
			self.future_y = self.height
		else:
			self.y_position = self.height - self.rect.height / 2

	# moves player right
	def move_right(self,delta_time):
		self.x_velocity = self.velocity*self.scale*delta_time
		if self.width - self.rect.right >= self.x_velocity:
			self.x_position += self.x_velocity
			self.future_x = self.width
		else:
			self.x_position = self.width - self.rect.width / 2

	# moves player left
	def move_left(self,delta_time):
		self.x_velocity = self.velocity*self.scale*delta_time
		if self.rect.left >= self.x_velocity:
			self.x_position -= self.x_velocity
			self.future_x = 0
		else:
			self.x_position = self.rect.width / 2

	# called when the player uses the dash ability.
	def dash(self):
		self.find_movement_direction()
		self.x_dash_distance = self.movement_vector.x * 150
		self.y_dash_distance = self.movement_vector.y * 150
		
		
		if self.x_dash_distance < 0:
			if self.width - self.rect.right >= self.x_dash_distance:
				self.x_position += self.x_dash_distance
			else:
				self.x_position = self.width - self.rect.width / 2

		elif self.x_dash_distance > 0:
			if self.rect.left >= self.x_velocity:
				self.x_position += self.x_dash_distance
			else:
				self.x_position = self.rect.width / 2

		if self.y_dash_distance > 0:
			if self.height - self.rect.bottom >= self.y_dash_distance:
				self.y_position += self.y_dash_distance
			else:
				self.y_position = self.height - self.rect.height / 2

		if self.y_dash_distance < 0:
			if self.rect.top >= self.y_dash_distance:
				self.y_position += self.y_dash_distance
			else:
				self.y_position = self.rect.height / 2


# projectile entities abstract class.
class PlayerProjectiles(EntitiesAbstract):
	def __init__(self,image):
		super().__init__(image)
		self.display_rect = pygame.Rect(-100,-100,self.width+100,self.height+100)

	# Factory used for projectiles
	@staticmethod
	def factory(type_of_projectile, images):
		if type_of_projectile == "laser":
			return PlayerLaser(images.player_laser)
		elif type_of_projectile == "missile":
			return PlayerMissile(images.player_missile)
		elif type_of_projectile == "homing_laser":
			return PlayerHomingLaser(images.red_orb)

	# sets the projectiles initial position using the players position.
	def get_initial_position(self, player_x_position, player_y_position):
		self.x_position = player_x_position
		self.y_position = player_y_position

	# moves the projectile and kills the object if it is outside the screen.
	def move(self):
		self.x_position += self.x_distance * self.velocity
		self.y_position += self.y_distance * self.velocity
		if not self.display_rect.contains(self.rect):
			self.kill()


# player laser entity
class PlayerLaser(PlayerProjectiles):
	def __init__(self,image):
		super().__init__(image)
		self.velocity = 7
		self.damage = 1

# player missile entity
class PlayerMissile(PlayerProjectiles):
	def __init__(self,image):
		super().__init__(image)
		self.velocity = 4
		self.damage = 3

# player homing laser entity
class PlayerHomingLaser(PlayerProjectiles):
	def __init__(self,image):
		super().__init__(image)
		self.velocity = 3
		self.damage = 2
		self.change = True

	# homing laser requires a different move method as it moves differently.
	# if the laser is over a certain distance away, then a new vector is found which moves the laser toward the mouse.
	# if it is below a certain distance away, then the vector stays the same and it travels
	# in the direction of its final vector.
	def move(self):
		self.find_mouse_position()
		if self.change:
			self.vector = pygame.math.Vector2((self.mouse_x_position - self.x_position,
												self.mouse_y_position - self.y_position))

			self.vector = self.vector.normalize()
		self.x_distance_from_mouse = self.mouse_x_position - self.x_position
		self.y_distance_from_mouse = self.mouse_y_position - self.y_position
		if abs(self.x_distance_from_mouse) <= 20 and abs(self.y_distance_from_mouse) <= 20:
			self.change = False

		self.y_position += self.vector.y * self.velocity
		self.x_position += self.vector.x * self.velocity


# crosshair entity
class Crosshair(EntitiesAbstract):
	def __init__(self, image):
		super().__init__(image)

	def update(self):
		self.rect.center = pygame.mouse.get_pos()


# enemy entities abstract class
class EnemyAbstract(EntitiesAbstract):
	def __init__(self, image, x_position):
		super().__init__(image)
		self.moving_down = True
		self.moving_up = False
		self.moving_right = True
		self.moving_left = False
		self.shooting_timer = 0
		self.x_position = x_position
		self.y_position = -100

	# factory used for enemies.
	@staticmethod
	def factory(enemy,image,x_position):
		if enemy == "blue":
			return BlueEnemy(image,x_position)
		if enemy == "green":
			return GreenEnemy(image,x_position)
		if enemy == "yellow":
			return YellowEnemy(image,x_position)

	# method used to move enemies.
	def move(self):
		if self.moving_down:
			if self.y_position < self.y_bound[1]:
				self.y_position += self.velocity
			else:
				self.y_position = self.y_bound[1]
				self.moving_down = False

		elif self.moving_right:
			if self.x_position < self.x_bound[1]:
				self.x_position += self.velocity
			else:
				self.x_position = self.x_bound[1]
				self.moving_right = False
				self.moving_left = True
		
		elif self.moving_left:
			if self.x_position > self.x_bound[0]:
				self.x_position -= self.velocity
			else:
				self.x_position = self.x_bound[0]
				self.moving_left = False
				self.moving_right = True

	# responsible for controlling enemies rate of fire.
	def is_shooting(self):
		self.shooting_timer += 1
		if self.shooting_timer % self.fire_rate == 0:
			self.shooting_timer = 0
			return True
		else:
			return False


# blue enemy class
class BlueEnemy(EnemyAbstract):
	def __init__(self,image,x_position):
		super().__init__(image,x_position)
		self.x_bound = [50,550]
		self.y_bound = [50,70]
		self.velocity = 1.2
		self.health = 5
		self.fire_rate = 80   # The higher the value, the lower the fire rate.
		

# green enemy class
class GreenEnemy(EnemyAbstract):
	def __init__(self,image,x_position):
		super().__init__(image,x_position)
		self.x_bound = [50,550]
		self.y_bound = [50,115]
		self.velocity = 2
		self.health = 3
		self.fire_rate = 65
		

# yellow enemy class
class YellowEnemy(EnemyAbstract):
	def __init__(self,image,x_position):
		super().__init__(image,x_position)
		self.x_bound = [50,550]
		self.y_bound = [50,50]
		self.velocity = 1
		self.health = 8
		self.fire_rate = 130

		self.moving_right = False

		
# enemy projectiles abstract class
class EnemyProjectiles(EntitiesAbstract):
	def __init__(self,image,enemy):
		super().__init__(image)
		self.enemy = enemy
		self.display_rect = pygame.Rect(-100,-100,self.width+100,self.height+100)
		self.x_position = self.enemy.x_position
		self.y_position = self.enemy.y_position
		
	# factory used for enemy projectiles
	@staticmethod
	def factory(images,enemy):
		if enemy.__class__.__name__ == "BlueEnemy":
			return BlueLaser(images.blue_laser,enemy)
		elif enemy.__class__.__name__ == "GreenEnemy":
			return GreenLaser(images.green_laser,enemy)
		elif enemy.__class__.__name__ == "YellowEnemy":
			return YellowOrb(images.yellow_orb,enemy)

	# method used to move the enemy projectiles.
	def move(self):
		self.y_position += self.velocity
		if not self.display_rect.contains(self.rect):
			self.kill()


# blue laser entity class
class BlueLaser(EnemyProjectiles):
	def __init__(self,image,enemy):
		super().__init__(image,enemy)
		self.velocity = 4
		self.damage = 1


# green laser entity class
class GreenLaser(EnemyProjectiles):
	def __init__(self,image,enemy):
		super().__init__(image,enemy)
		self.velocity = 8
		self.damage = 1
		

# yellow orb entity class
class YellowOrb(EnemyProjectiles):
	def __init__(self,image,enemy):
		super().__init__(image,enemy)
		self.velocity = 4
		self.damage = 2
		self.vector = 1
		self.change = True

	# this projectile has to have a different move method as it moves differently.
	# if it's a certain distance away from player, a vector is calculated based off the players position.
	# once the projectile gets within a certain range, the vector is no longer calculated and the projectile
	# moves in the direction of its final vector.
	def move(self,player_ship):
		if self.change:
			self.vector = pygame.math.Vector2((player_ship.x_position - self.x_position, 
												player_ship.y_position - self.y_position))
			
			self.vector = self.vector.normalize()
		if player_ship.x_position - self.x_position <= 95 and player_ship.y_position - self.y_position <= 95:
			self.change = False
		self.y_position += self.vector.y * self.velocity
		self.x_position += self.vector.x * self.velocity
		

# explosion entity class
class Explosions(pygame.sprite.Sprite):
	def __init__(self,explosion_list):
		super().__init__()
		self.explosion_list = explosion_list
		self.image = self.explosion_list[0]
		self.rect = self.image.get_rect()
		self.counter = 0

	# method used to find the position of the explosion on the enemy
	def get_enemy_position(self,projectile,enemy):
		if projectile.x_position >= enemy.x_position:
			if projectile.y_position >= enemy.y_position:
				self.x_position = enemy.x_position + enemy.rect.width/4
				self.y_position = enemy.y_position + enemy.rect.height/4          
			else:
				self.x_position = enemy.x_position + enemy.rect.width/4
				self.y_position = enemy.y_position - enemy.rect.height/4
		else:
			if projectile.y_position >= enemy.y_position:
				self.x_position = enemy.x_position - enemy.rect.width/4
				self.y_position = enemy.y_position + enemy.rect.height/4
			else:
				self.x_position = enemy.x_position - enemy.rect.width/4
				self.y_position = enemy.y_position - enemy.rect.height/4

	# retrieves player's position, used for when the player explodes when they lose all their lives.
	def get_player_position(self,x_position,y_position):
		self.x_position = x_position
		self.y_position = y_position

	# updates the image of the explosion.
	def update(self):
		if self.counter <= 8:
			self.image = self.explosion_list[self.counter//2]
			self.rect = self.image.get_rect()
			self.counter += 1
		else:
			self.kill()
		self.rect.center = (self.x_position, self.y_position)


# shop entity class
class ShopEntity(EntitiesAbstract):
	def __init__(self, image):
		super().__init__(image)
		self.x_position = self.display.width / 2
		self.y_position = -100
		self.velocity = 1
		self.moving_on = True
		self.moving_off = False
		self.is_open = False

	# checks and manipulates the state of the shop.
	def check_state(self, player):
		if self.moving_on or self.moving_off:
			self.interactable = False
		else:
			self.interactable = True

		if player.y_position < 75 and self.interactable:
			self.moving_off = True

		if -100 < player.y_position - self.y_position < 100 and -100 < player.x_position - self.x_position < 100 and self.interactable:
			self.is_open = True
		else:
			self.is_open = False

	# moves shop entity onto the screen and stops when the shop is in the middle of the screen
	def move_onto_screen(self):
		if self.moving_on:
			if self.y_position < self.display.height / 2:
				self.y_position += self.velocity
			else:
				self.y_position = self.display.height / 2
				self.moving_on = False

	# moves shop entity off of the screen
	def move_off_screen(self):
		if self.moving_off:
			if self.y_position < self.display.height + 100:
				self.y_position += self.velocity
			else:
				self.y_position = self.display.height + 100
				self.kill()