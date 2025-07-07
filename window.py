from imagesclass import *
from databases import *


# abstract window class, holds all the attributes and method shared by all the different windows.
class AbstractWindow:
	def __init__(self):
		self.width = 600
		self.height = 750
		self.clicking = False
		self.display = pygame.display.set_mode((self.width,self.height))
		self.caption = pygame.display.set_caption("Invader Evader")
		self.images = Images()
		self.text_colour = self.images.colours["white"]
		self.background_image = self.images.start_background
		self.background_image = pygame.transform.scale(self.background_image, (self.width,self.height))
		self.font_size = 42
		self.font = pygame.font.Font("newfont2.ttf", self.font_size)
		self.smaller_font = pygame.font.Font("newfont2.ttf", int(self.font_size/1.5))
		self.button_list = []
		self.button_sound = pygame.mixer.Sound("buttonsound.wav")

		self.Leaderboard_database = LeaderboardDatabase()
		self.login_database = LoginDatabase()

	# checks whether the player is quitting or clicking.
	def check_events(self):
		self.clicking = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.clicking = True

	# displays background
	def background(self):
		self.display.blit(self.background_image,(0,0))

	# displays text on the screen, given a center position.
	def create_text(self, text, colour, center):
		self.line = self.font.render(text, 1, colour)
		self.rect = self.line.get_rect(center = center)
		self.display.blit(self.line,self.rect)

	# displays text on the screen, given a top left position.
	def create_text_top_left(self, text, colour, position):
		self.line = self.font.render(text, 1, colour)
		self.rect = self.line.get_rect()
		self.display.blit(self.line,position)

	# draws a rect on the screen
	def draw_rect(self, rect_tuple):
		self.rect = pygame.draw.rect(self.display, self.text_colour, rect_tuple, 1)
		return self.rect

	# gets mouse position
	def get_mouse_position(self):
		self.x_mouse_position, self.y_mouse_position = pygame.mouse.get_pos()

	# used to find if a button was pressed, and decides what to do.
	def button_pressed(self):
		if self.clicking:
			for i in range(0, len(self.button_list)):
				if self.button_list[i][0].collidepoint((self.x_mouse_position, self.y_mouse_position)):
					self.button_sound.play()
					if self.button_list[i][1] == "settings":
						self.settings_button_pressed(self.button_list[i][2])
					elif self.button_list[i][1] == "login":
						self.login_button_pressed(self.button_list[i][2])
					elif self.button_list[i][1] == "game options":
						self.reset_player_inputs()
						self.menu_stack.push_menu_stack(self.menu_stack.options)
					elif self.button_list[i][1] == "logout":
						self.menu_stack.pop_menu_stack()
					else:
						self.menu_stack.evaluate_button(self.button_list[i][1])

	# sets delta time
	def set_delta_time(self,delta_time):
		self.delta_time = delta_time

	# sets menu stack
	def set_menu_stack(self,menu_stack):
		self.menu_stack = menu_stack


# login menu class
class Login(AbstractWindow):
	def __init__(self):
		super().__init__()
		self.username_input = ''
		self.inputting_username = False
		self.password_input = ''
		self.inputting_password = False
		self.rect = (0,0,0,0)
		self.character_limit = 10
		self.register_or_login_text = "register page"
		self.menu_title = "login"
		self.login_incorrect = False
		self.username_taken = False
		self.username_allowed = True
		self.password_allowed = True

	# checks whether the player is clicking and or quitting
	# and checks if the player is typing into each of the input fields
	def check_events(self):
		self.clicking = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.clicking = True

			if event.type == KEYDOWN:                      
				if self.inputting_username:
					self.username_input = self.add_characters(event,self.username_input)
				
				elif self.inputting_password:
					self.password_input = self.add_characters(event,self.password_input)

	# adds characters to the input fields based off of the unicode off the key pressed.
	def add_characters(self,event,input_field):
		if event.key == K_BACKSPACE:
			return input_field[:-1]
		elif event.key != K_RETURN and len(input_field) < self.character_limit:   
			return input_field + event.unicode
		else:
			return input_field

	# creates the buttons and text of the menu
	def create_buttons(self):
		self.create_text(self.menu_title,self.text_colour,(self.width/2,40))
		self.username_rect = pygame.Rect(self.width / 2 - 250, 200, 500, 40)
		if self.inputting_username:
			self.username_button = self.draw_rect(self.username_rect)
		self.username_button_text = self.create_text_top_left("username: " + self.username_input, self.text_colour, (self.width/2-245,200))

		self.password_rect = pygame.Rect(self.width / 2 - 250, 300, 500, 40)
		if self.inputting_password:
			self.password_button = self.draw_rect(self.password_rect)
		self.password_button_text = self.create_text_top_left("Password: " + self.password_input, self.text_colour, (self.width/2-245,300))

		self.enter_button = self.draw_rect((self.width / 2 - 100, 400, 200, 40))
		self.enter_button_text = self.create_text("Enter", self.text_colour, self.enter_button.center)

		self.change_button = self.draw_rect((self.width / 2 - 100, 450, 200, 40))
		self.change_button_text = self.create_text(self.register_or_login_text, self.text_colour, self.change_button.center)

		self.exit_button = self.draw_rect((self.width / 2 - 100, 550, 200, 40))
		self.exit_button_text = self.create_text("Exit", self.text_colour, self.exit_button.center)

		# a list of all the buttons on the menu and what they do.
		self.button_list = [[self.username_rect,"login","username"],[self.password_rect,"login","password"],
							[self.enter_button,"login","enter"],[self.change_button,"login",self.register_or_login_text],[self.exit_button,"exit"]]

		# messages only displayed if the user inputs a an invalid input.
		if self.login_incorrect:
			self.create_text("incorrect. try again.",self.text_colour,(self.width/2,100))
		if self.username_taken:
			self.create_text("username taken. try again.",self.text_colour,(self.width/2,100))
		if not(self.username_allowed):
			self.create_text("username, 3 characters minimum.",self.text_colour,(self.width/2,100))
		if not(self.password_allowed):
			self.create_text("password:",self.text_colour,(self.width/2,70))
			if len(self.password_input) < 5:
				self.create_text("5 characters minimum.",self.text_colour,(self.width/2,100))
			if self.password_input.islower() or len(self.password_input) == 0:
				self.create_text("at least 1 capital letter.",self.text_colour,(self.width/2,130))
			if self.password_input.isalpha() or len(self.password_input) == 0:
				self.create_text("at least 1 special character.", self.text_colour, (self.width / 2, 160))

	# used to find what to do is a button on the login menu is pressed.
	def login_button_pressed(self,button):
		self.login_incorrect = False
		self.username_taken = False
		self.username_allowed = True
		self.password_allowed = True
		self.button = button
		if self.button == "username":
			self.inputting_username = True
			self.inputting_password = False
		elif self.button == "password":
			self.inputting_password = True
			self.inputting_username = False
		elif self.button == "enter":
			if self.register_or_login_text == "register page":
				self.check_login()
			else:
				self.check_inputs()
		elif self.button == "register page":
			self.register_or_login_text = "login page"
			self.menu_title = "register"
		elif self.button == "login page":
			self.register_or_login_text = "register page"
			self.menu_title = "login"

	# checks whether the strings in stored in the input fields provide a valid login.
	def check_login(self):
		if self.login_database.login(self.username_input,self.password_input) == "correct":
			self.menu_stack.evaluate_button("main menu")
			self.menu_stack.game_over.find_username(self.username_input)
		else:
			self.login_incorrect = True

	# INPUT VALIDATION, used when the player tries to register.
	def check_inputs(self):
		if len(self.username_input) < 3:
			self.username_allowed = False
		elif len(self.password_input) < 5 or self.password_input.islower() or self.password_input.isalpha():
			self.password_allowed = False
		else:
			self.check_registration()

	# checks whether the username is taken, if not the player is registered.
	def check_registration(self):
		if self.login_database.username_available(self.username_input):
			self.login_database.register(self.username_input,self.password_input)
			self.menu_stack.evaluate_button("main menu")
			self.menu_stack.game_over.find_username(self.username_input)
		else:
			self.username_taken = True


# main menu class
class MainMenu(AbstractWindow):
	def __init__(self):
		super().__init__()

	# creates the buttons and text of the menu
	def create_buttons(self):	
		self.create_text("Invader Evader", self.text_colour, (self.width/2,20))
		
		self.start_button = self.draw_rect((self.width / 2 - 150, 100, 300, 40))
		self.start_button_text = self.create_text("Start Playing", self.text_colour, self.start_button.center)

		self.leaderboard_button = self.draw_rect((self.width / 2 - 150, 200, 300, 40))
		self.leaderboard_button_text = self.create_text("Leaderboard", self.text_colour, self.leaderboard_button.center)

		self.controls_button = self.draw_rect((self.width / 2 - 150, 300, 300, 40))
		self.controls_button_text = self.create_text("Controls", self.text_colour, self.controls_button.center)

		self.options_button = self.draw_rect((self.width / 2 - 150, 400, 300, 40))
		self.options_button_text = self.create_text("Options", self.text_colour, self.options_button.center)

		self.logout_button = self.draw_rect((self.width / 2 - 150, 500, 300, 40))
		self.logout_button_text = self.create_text("Log Out", self.text_colour, self.logout_button.center)

		self.exit_button = self.draw_rect((self.width / 2 - 150, 600, 300, 40))
		self.exit_button_text = self.create_text("Exit", self.text_colour, self.exit_button.center)

		# a list of all the buttons on the menu and what they do.
		self.button_list = [[self.start_button, "game"], [self.leaderboard_button, "leaderboard"], 
							[self.controls_button, "controls"], [self.options_button, "options"], [self.exit_button,"exit"],[self.logout_button,"logout"]]
		

# leaderboard menu class
class Leaderboard(AbstractWindow):
	def __init__(self):
		super().__init__()

	# creates the buttons and text of the menu.
	def create_buttons(self):
		self.create_text("leaderboard", self.text_colour, (self.width/2,20))

		self.back_button = self.draw_rect((self.width / 2 - 150, 600, 300, 40))
		self.back_button_text = self.create_text("Back", self.text_colour, self.back_button.center)

		# a list of all the buttons on the menu and what they do.
		self.button_list = [[self.back_button,"back"]]

		# retrieves the top 5 scores from the leaderboard and uses them to create the leaderboard text.
		self.Leaderboard_list = self.Leaderboard_database.retrieve_table()
		for i in range(len(self.Leaderboard_list)):
			rank = i + 1
			self.create_text_top_left(str(rank)+".  "+self.Leaderboard_list[i][0], self.text_colour, (100,rank*100))
			self.create_text_top_left(str(self.Leaderboard_list[i][1]), self.text_colour, (400,rank*100))


# controls class.
class Controls(AbstractWindow):
	def __init__(self):
		super().__init__()

	# creates the buttons and text of the menu.
	def create_buttons(self):
		self.create_text("Controls", self.text_colour, (self.width/2,20))

		# controls information text
		self.create_text("Press Q to Change Weapon", self.text_colour, (self.width/2,150))
		self.create_text("WASD to Move", self.text_colour, (self.width/2,225))
		self.create_text("Use the Mouse to Aim", self.text_colour, (self.width/2,300))
		self.create_text("Space to Shoot", self.text_colour, (self.width/2,375))
		
		self.back_button = self.draw_rect((self.width / 2 - 150, 500, 300, 40))
		self.back_button_text = self.create_text("Back", self.text_colour, self.back_button.center)

		# a list of all the buttons on the menu and what they do
		self.button_list = [[self.back_button,"back"]]


class Options(AbstractWindow):
	def __init__(self):
		super().__init__()
		self.music_volume = 100
		self.sound_volume = 100

	# creates the buttons and text of the menu
	def create_buttons(self):
		self.create_text("Options", self.text_colour, (self.width/2,20))

		self.music_volume_button = self.draw_rect((self.width / 2 - 150, 200, 300, 45))
		self.music_volume_button_text = self.create_text("Music Volume: "+str(self.music_volume),
														self.text_colour,self.music_volume_button.center)

		self.music_up_button = self.draw_rect((450, 200, 100, 45))
		self.music_up_button_text = self.create_text("UP",self.text_colour,self.music_up_button.center)
		self.music_down_button = self.draw_rect((50, 200, 100, 45))
		self.music_down_button_text = self.create_text("DOWN",self.text_colour,self.music_down_button.center)

		self.sound_volume_button = self.draw_rect((self.width / 2 - 150, 300, 300, 45))
		self.sound_volume_button_text = self.create_text("Sound Volume: "+str(self.sound_volume),
														self.text_colour,self.sound_volume_button.center)
		
		self.sound_up_button = self.draw_rect((450, 300, 100, 45))
		self.sound_up_button_text = self.create_text("UP",self.text_colour,self.sound_up_button.center)
		self.sound_down_button = self.draw_rect((50, 300, 100, 45))
		self.sound_down_button_text = self.create_text("DOWN",self.text_colour,self.sound_down_button.center)


		self.back_button = self.draw_rect((self.width / 2 - 150, 500, 300, 40))
		self.back_button_text = self.create_text("Back", self.text_colour, self.back_button.center)

		# a list of all the buttons on the menu and what they do.
		self.button_list = [[self.sound_up_button,"settings","sound up"],[self.sound_down_button,"settings","sound down"],
		[self.music_up_button,"settings","music up"], [self.music_down_button,"settings","music down"],[self.back_button,"back"]]

		# if the menu is accessed in the main game there needs to be a quit button.
		if self.menu_stack.menu_stack[-2] == self.menu_stack.game:
			self.quit_button = self.draw_rect((self.width / 2 - 150, 550, 300, 40))
			self.quit_button_text = self.create_text("Quit", self.text_colour, self.quit_button.center)
			self.button_list.append([self.quit_button, "quit"])

	# used to decide what to do when a button that manipulates in-game settings is pressed.
	def settings_button_pressed(self, button):
		self.button = button
		if self.button == "sound up" and self.sound_volume != 100:
			self.sound_volume += 5
			self.button_sound.play()
			Music.set_sound_volume(self.button_sound, self.sound_volume)
		elif self.button == "sound down" and self.sound_volume != 0:
			self.sound_volume -= 5
			self.button_sound.play()
			Music.set_sound_volume(self.button_sound, self.sound_volume)
		elif self.button == "music up" and self.music_volume != 100:
			self.music_volume += 5
			self.button_sound.play()
			Music.set_music_volume(self.music_volume)
		elif self.button == "music down" and self.music_volume != 0:
			self.music_volume -= 5
			self.button_sound.play()
			Music.set_music_volume(self.music_volume)

	
# main game class
class Game(AbstractWindow):
	def __init__(self):
		super().__init__()
		self.background_image = self.images.background
		self.background_image = pygame.transform.scale(self.background_image, (self.width,self.height))
		self.background_position = 0
		self.background_is_moving = True

		self.font_size = 35
		self.font = pygame.font.Font("newfont2.ttf", self.font_size)
		
		self.laser_image = self.images.laser_frame
		self.missile_image = self.images.missile_frame
		# a list which stores the players current weapons.
		self.weapons = [[self.laser_image, 700, "laser"], [self.missile_image, 645, "missile"]]
		self.weapon_count = 0
		self.current_weapon = self.weapons[0]
		self.dash_purchased = False
		
		# creates all the necessary sprite groups.
		self.create_sprite_groups()
		# creates the objects of entities there will only be one of.
		self.create_ship_objects()
		self.create_shop_object()
		
		self.score = 0
		self.shooting = False
		self.bullet_timer = 0
		self.dash_timer = 0
		self.game_over_timer = 150
		# a queue, responsible for what happens each wave.
		self.wave_queue = [[["blue",self.images.blue_enemy,self.width/2]],[["green",self.images.green_enemy,50]],[["blue",self.images.blue_enemy,50],
							["green",self.images.green_enemy,550]],[["yellow",self.images.yellow_enemy,self.width/2]],None,
							[["green",self.images.green_enemy,50],["green",self.images.green_enemy,550]],[["yellow",self.images.yellow_enemy,100],["yellow",self.images.yellow_enemy,500]],
							[["yellow",self.images.yellow_enemy,self.width/2],["blue",self.images.blue_enemy,50]],[["green",self.images.green_enemy,50],
							["green",self.images.green_enemy,550],["yellow",self.images.yellow_enemy,self.width/2]]]
		

		# the speed at which the background moves down the screen per frame.
		self.background_velocity = 1


	# displays and moves the backgrounds.
	def background(self):
		if self.background_position < 750:
			self.background_position += self.background_velocity
		else:
			self.background_position = 0
		self.display.blit(self.background_image, (0,self.background_position))
		self.display.blit(self.background_image, (0, (0 - self.height) + self.background_position))

	# displays text, given a top left position.
	# much like the method inherited from the abstract class however this method accepts a font parameter,
	# meaning we can pass in new fonts.
	def create_text_top_left(self, text, colour, position, font = None):
		if font == None:
			font = self.font
		self.line = font.render(text, 1, colour)
		self.display.blit(self.line,position)

	# creates the buttons and text of the menu.
	def create_buttons(self):
		self.settings_image = self.images.settings_image
		self.display.blit(self.settings_image,(self.width-50,self.height-50))
		self.settings_button = pygame.Rect(self.width-50,self.height-50,50,50)

		self.button_list = [[self.settings_button,"game options"]]

		# displays weapon slots.
		for weapon in range(len(self.weapons)):
			if self.weapons[weapon] == self.current_weapon:
				self.display.blit(self.weapons[weapon][0], (0,self.weapons[weapon][1]))
			else:
				self.display.blit(self.weapons[weapon][0], (-40,self.weapons[weapon][1]))

		# displays player's lives
		self.create_text_top_left("lives: " + str(self.player_ship.health), self.text_colour, (52,self.height-35))
		# displays player's score
		self.create_text_top_left("score: " + str(self.score), self.text_colour, (150,self.height-35))

		# if the current wave is equal to none it is a shop round.
		if self.current_wave == None:
			# displays text onto the screen telling the player it is a shop round.
			self.create_text_top_left("shop round", self.text_colour, (350,self.height-35))

		# displays an arrow, if dash ability is purchased from the shop.
		if self.dash_purchased:
			# if the dash is available (dash timer equals 0) a white arrow is displayed on the screen.
			if self.dash_timer == 0:
				self.display.blit(self.images.dash_image,(0,self.height-160))
			else:
				# if the dash is unavailable (it has been used in the last second) then a grey arrow is displayed.
				self.display.blit(self.images.no_dash_image,(0,self.height-160))

	# resets the player inputs.
	def reset_player_inputs(self):
		self.shooting = False
		self.player_ship.moving_up = False
		self.player_ship.moving_down = False
		self.player_ship.moving_left = False
		self.player_ship.moving_right = False

	# checks the players inputs
	def check_events(self):
		self.clicking = False
		self.player_ship.dashing = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.clicking = True

			# checks whether a key has been pressed down.
			if event.type == KEYDOWN:
				if event.key == K_q:
					self.change_weapon()
					self.button_sound.play()
				if event.key == K_SPACE:
					self.shooting = True
				if event.key == K_a:
					self.player_ship.moving_left = True
				if event.key == K_d:
					self.player_ship.moving_right = True
				if event.key == K_w:
					self.player_ship.moving_up = True
				if event.key == K_s:
					self.player_ship.moving_down = True
				if event.key == K_i:
					self.player_ship.health = 100
				if event.key == K_h:
					self.score += 1000
				# if e is pressed and the player can interact with the shop then the shop menu is pushed onto the stack.
				if event.key == K_e and self.shop.is_open:
					self.reset_player_inputs()
					self.menu_stack.push_menu_stack(self.menu_stack.shop_screen)
				# if shift is pressed and dash is purchased then dashing is set to true.
				if event.mod & KMOD_SHIFT and self.dash_purchased:
					self.player_ship.dashing = True

			# checks if a key has been released.
			if event.type == KEYUP:
				if event.key == K_SPACE:
					self.shooting = False
				if event.key == K_a:
					self.player_ship.moving_left = False
				if event.key == K_d:
					self.player_ship.moving_right = False
				if event.key == K_w:
					self.player_ship.moving_up = False
				if event.key == K_s:
					self.player_ship.moving_down = False

		# Player needs to be alive to shoot and dash.
		if self.player_ship.health > 0:
			self.player_ship.move(self.delta_time)

			# if the player is dashing (dashing is true) and the dash timer is 0 then the player dashes.
			if self.player_ship.dashing and self.dash_timer == 0:
				self.player_ship.dash()
				self.dash_timer += 1

			# if the player is shooting and the bullet timer is zero, then a projectile object is created.
			if self.shooting and self.bullet_timer == 0:
				self.create_projectile_object()
				self.bullet_timer += 1
				
				

		
		self.change_bullet_timer()
		self.change_dash_timer()

	# the player can only shoot when the bullet timer attribute is 0,
	# different weapons take different amounts of time to reach 0, this is how i adjust the players fire-rate.
	def change_bullet_timer(self):                      
		if self.bullet_timer > 0:
			self.bullet_timer += 1
		if self.current_weapon[2] == "laser": 
			if self.bullet_timer >= 24:
				self.bullet_timer = 0
		if self.current_weapon[2] == "missile" or "homing_laser":     
			if self.bullet_timer >= 60:
				self.bullet_timer = 0

	# player can dash when the timer equals 0, after dashing the dash timer attribute is incremented by 1.
	# the player has to wait 120 frames (1 second) after dashing to dash again.
	def change_dash_timer(self):
		if self.dash_timer > 0:
			self.dash_timer += 1
		if self.dash_timer >= 120:
			self.dash_timer = 0

	# current weapon is changed to the next weapon in the weapons list.
	# we try to find the next weapon in the list, if there are no more weapons in the list (index error)
	# then we go back to the first weapon.
	def change_weapon(self):
		try:
			self.weapon_count += 1
			self.current_weapon = self.weapons[self.weapon_count]
		except IndexError:
			self.weapon_count = 0
			self.current_weapon = self.weapons[self.weapon_count]

	# create all the sprite groups we are going use.
	def create_sprite_groups(self):
		self.spaceship_group = pygame.sprite.Group()
		self.crosshair_group = pygame.sprite.Group()
		self.projectile_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.enemy_projectile_group = pygame.sprite.Group()
		self.explosion_group = pygame.sprite.Group()
		self.shop_group = pygame.sprite.Group()

	# creates an object of the PlayerShip class and adds it to its respective sprite group.
	# creates an object of the Crosshair class and adds it to its respective sprite group.
	def create_ship_objects(self):
		self.player_ship = PlayerShip(self.images.player_image,self.images.flashing_png)
		self.spaceship_group.add(self.player_ship)

		self.crosshair = Crosshair(self.images.crosshair_image)
		self.crosshair_group.add(self.crosshair)

	# creates the projectile, passes the players initial position into the object,
	# finds the rotation angle, rotates the projectile, and adds it to the projectile sprite group.
	def create_projectile_object(self):
		self.player_projectile = PlayerProjectiles.factory(self.current_weapon[2], self.images)
		self.player_projectile.get_initial_position(self.player_ship.x_position,self.player_ship.y_position)
		self.player_projectile.find_rotation_angle()
		self.player_projectile.rotate()
		self.projectile_group.add(self.player_projectile)

	# responsible for turning the wave queue into in-game events.
	# if there are no entities on the screen, the item at the front of the queue is made into an enemy.
	# unless the item is a NoneType (meaning its a shop round), where we add the shop object to the shop sprite group.
	# we then remove the item at the front of the list
	def waves(self):
		if len(self.enemy_group) == 0 and len(self.shop_group) == 0:
			try:
				self.current_wave = self.wave_queue[0]
				for enemy in range(len(self.current_wave)):
					self.create_enemy_object(*self.current_wave[enemy])
				self.wave_queue.remove(self.current_wave)
			except TypeError:
				self.shop_group.add(self.shop)
				self.wave_queue.remove(self.current_wave)
			except IndexError:
				self.game_over_setup()

	# creates the enemy object using a factory in the EnemyAbstract class,
	# adds the object to the enemy sprite group.
	def create_enemy_object(self, enemy, image, x_position):
		self.enemy = EnemyAbstract.factory(enemy,image,x_position)         
		self.enemy_group.add(self.enemy)

	# creates the shop object
	def create_shop_object(self):
		self.shop = ShopEntity(self.images.shop_image)

	# check collisions of the entities
	def check_collisions(self):
		# checks for a direct collision between the player and the enemy.
		if not self.player_ship.flashing and len(self.enemy_group) > 0:
			for enemy in self.enemy_group:
				if pygame.sprite.collide_mask(self.player_ship,enemy):
				
					if self.player_ship.health > 0:
						if self.score - 100 < 0:
							self.score = 0
						else:
							self.score -= 100
					
					self.player_ship.hit(1)

		# check for a collision between the players projectiles and enemies.
		if len(self.projectile_group) > 0 and len(self.enemy_group) > 0:
			for enemy in self.enemy_group:
				for projectile in self.projectile_group:
					if pygame.sprite.collide_mask(projectile,enemy) and enemy.rect.bottom > 0:
						projectile.kill()
						enemy.hit(projectile.damage)
						self.score += 50
						self.explosion = Explosions(self.images.explosion_list)
						self.explosion.get_enemy_position(projectile,enemy)
						self.explosion_group.add(self.explosion)

		# checks for collision between the the player and the enemies projectiles.
		if len(self.enemy_projectile_group) > 0:
			for projectile in self.enemy_projectile_group:
				if pygame.sprite.collide_mask(self.player_ship,projectile):
					
					if self.player_ship.health > 0:
						if self.score - 100 < 0:
							self.score = 0
						else:
							self.score -= 100

					self.player_ship.hit(projectile.damage)
					projectile.kill()

	# checks if the player has lost all their lives.
	def check_lives(self):
		if self.player_ship.health == 0:
			self.player_explosion = Explosions(self.images.player_explosion_list)
			self.player_explosion.get_player_position(self.player_ship.x_position,self.player_ship.y_position)
			self.explosion_group.add(self.player_explosion)
			self.game_over_setup()

	# completes all the actions required to end the game, timer makes it so it is not instant.
	def game_over_setup(self):
		if self.game_over_timer == 0:
			Music.stop_music()
			self.delete_objects()
			self.menu_stack.pop_menu_stack()
			self.menu_stack.game_over.set_score(self.score)
			self.menu_stack.push_menu_stack(self.menu_stack.game_over)
			self.menu_stack.reset_game_object()
			self.menu_stack.reset_shop_screen_object()
		else:
			self.game_over_timer -= 1

	# deletes all the objects
	def delete_objects(self):
		for enemy in self.enemy_group:
			del enemy
		for ship in self.spaceship_group:
			del ship
		for projectile in self.projectile_group:
			del projectile
		for projectile in self.enemy_projectile_group:
			del projectile
		for explosion in self.explosion_group:
			del explosion
		for shop in self.shop_group:
			del shop

	# updates the entities
	def update_entities(self):

		# moves projectiles
		for projectile in self.projectile_group:
			projectile.move()

		# moves enemies and creates enemy projectile objects
		for enemy in self.enemy_group:
			enemy.move()
			if enemy.is_shooting():
				self.enemy_projectile = EnemyProjectiles.factory(self.images,enemy)
				self.enemy_projectile_group.add(self.enemy_projectile)

		# moves enemy projectiles, some weapons need the players position.
		for projectile in self.enemy_projectile_group:
			try:
				projectile.move()
			except TypeError:
				projectile.move(self.player_ship)

		# moves shop onto and off of screen.
		for shop in self.shop_group:
			shop.check_state(self.player_ship)
			shop.move_onto_screen()
			shop.move_off_screen()
			# if the shop is in the middle of the screen and interactable the background stops moving.
			if shop.interactable:
				self.background_velocity = 0
			else:
				self.background_velocity = 1
			# if the shop is open (player within a certain distance of shop)
			# then a message of how to interact is displayed.
			if shop.is_open:
				self.create_text_top_left("[Press E]",self.text_colour,(shop.x_position+50,shop.y_position-50),self.smaller_font)


		# projectiles updated and drawn
		self.projectile_group.update()
		self.projectile_group.draw(self.display)
		self.enemy_projectile_group.update()
		self.enemy_projectile_group.draw(self.display)

		# enemies updated and drawn.
		self.enemy_group.update()
		self.enemy_group.draw(self.display)

		# players ship is updated, rotated and drawn.
		self.spaceship_group.update()
		self.player_ship.vulnerable()
		self.player_ship.find_mouse_position()
		self.player_ship.find_rotation_angle()
		self.player_ship.rotate()
		self.spaceship_group.draw(self.display)

		# shop is updated and drawn.
		self.shop_group.update()
		self.shop_group.draw(self.display)

		# explosions objects are updated and drawn
		self.explosion_group.update()
		self.explosion_group.draw(self.display)

		# crosshair group is updated and drawn.
		self.crosshair_group.update()
		self.crosshair_group.draw(self.display)

# the game over menu
class GameOver(AbstractWindow):
	def __init__(self):
		super().__init__()

	# retrieves the current player's username.
	def find_username(self,username):
		self.username = username

	# retrieves the score achieved by the player.
	def set_score(self,score):
		self.score = score
		self.update_table()

	# inserts the players username and final score into the leaderboard database.
	def update_table(self):
		self.Leaderboard_database.insert_scores(self.username,self.score)

	# displays the game over menu's text.
	def create_buttons(self):
		self.create_text("GAME OVER", self.text_colour, (self.width/2,50))
		self.create_text("Your Score: " + str(self.score), self.text_colour, (self.width/2,100)) # the player's score.
		self.create_text("Press RETURN To Play Again", self.text_colour, (self.width/2,200))
		self.create_text("Press ESCAPE To Exit To Main Menu", self.text_colour, (self.width/2,250))

	# checks for player inputs.
	def check_events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_RETURN:  # if return pressed the game is restarted
					self.menu_stack.pop_menu_stack()
					self.menu_stack.push_menu_stack(self.menu_stack.game)
				elif event.key == K_ESCAPE: # if escape pressed the player quits to main menu.
					self.menu_stack.quit_to_main_menu()


# shop menu
class Shop(AbstractWindow):
	def __init__(self):
		super().__init__()
		# booleans to keep track of whether each product is available to purchase.
		self.homing_in_stock = True
		self.dash_in_stock = True
		self.three_lives_in_stock = True

	# creates text given its top left position, a new font can be passed in.
	def create_text_top_left(self, text, colour, position, font = None):
		if font == None:
			font = self.font
		self.line = font.render(text, 1, colour)
		self.display.blit(self.line,position)

	# creates the buttons and text of the shop menu.
	def create_buttons(self):
		self.create_text("Shop", self.text_colour, (self.width/2,50))
		self.create_text_top_left("score: " + str(self.menu_stack.game.score), self.text_colour, (50, 80), self.smaller_font)

		# button used to purchase the homing laser.
		self.homing_button = self.draw_rect((50,150,100,100))
		# description and price of the homing laser.
		self.homing_text = self.create_text_top_left("homing laser: follows the crosshair", self.text_colour, (155,150), self.smaller_font)
		self.homing_price = self.create_text_top_left("price: 500 score", self.text_colour, (155,175), self.smaller_font)
		self.create_text_top_left("stored in the missile slot", self.text_colour, (155,200), self.smaller_font)
		# if the homing laser is not in stock, "purchased" is displayed next to the button.
		if not(self.homing_in_stock):
			self.create_text_top_left("purchased", self.text_colour, (155,225), self.smaller_font)

		# button used to purchase the dash ability.
		self.dash_button = self.draw_rect((50,350,100,100))
		# description and price of the dash ability.
		self.dash_text = self.create_text_top_left("dash: press shift to dash away from harm", self.text_colour, (155,350), self.smaller_font)
		self.dash_price = self.create_text_top_left("price: 300 score", self.text_colour, (155,375), self.smaller_font)
		# if the dash ability is not in stock, "purchased" will be displayed next to the button.
		if not(self.dash_in_stock):
			self.create_text_top_left("purchased", self.text_colour, (155,400), self.smaller_font)

		# button used to purchase three extra lives.
		self.three_lives_button = self.draw_rect((50,550,100,100))
		# description and price of the three extra lives.
		self.three_lives_text = self.create_text_top_left("extra lives: get three more lives", self.text_colour, (155,550), self.smaller_font)
		self.three_lives_price = self.create_text_top_left("price: 1000 score", self.text_colour, (155,575), self.smaller_font)
		# if the extra three lives are in stock, "purchased" will be displayed next to the button.
		if not(self.three_lives_in_stock):
			self.create_text_top_left("purchased", self.text_colour, (155,600), self.smaller_font)

		# back button
		self.back_button = self.draw_rect((self.width / 2 - 150, 700, 300, 40))
		self.back_button_text = self.create_text("Back", self.text_colour, self.back_button.center)

		# list of all the menu's buttons
		self.button_list = [[self.back_button,"back"]]
		# buttons are appended depending on whether they are in stock or not.
		if self.homing_in_stock:
			self.button_list.append([self.homing_button,"homing"])
		if self.dash_in_stock:
			self.button_list.append([self.dash_button,"dash"])
		if self.three_lives_in_stock:
			self.button_list.append([self.three_lives_button,"three_lives"])

	def button_pressed(self):
		if self.clicking:
			for i in range(0,len(self.button_list)):
				if self.button_list[i][0].collidepoint((self.x_mouse_position,self.y_mouse_position)):
					if self.button_list[i][1] == "back":
						self.menu_stack.pop_menu_stack()
					elif self.button_list[i][1] == "homing" and self.menu_stack.game.score >= 500:
						self.homing_in_stock = False
						self.menu_stack.game.score -= 500
						self.menu_stack.game.weapons[1][2] = "homing_laser"
					elif self.button_list[i][1] == "dash" and self.menu_stack.game.score >= 300:
						self.dash_in_stock = False
						self.menu_stack.game.score -= 300
						self.menu_stack.game.dash_purchased = True
					elif self.button_list[i][1] == "three_lives" and self.menu_stack.game.score >= 1000:
						self.three_lives_in_stock = False
						self.menu_stack.game.score -= 1000
						self.menu_stack.game.player_ship.health += 3

 


from game import *

