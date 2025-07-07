import pygame, sys, time
from pygame.locals import *
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512) 	# Pre-initializes the mixer so that sound effects are not delayed
											# (frequency, size, channel- 2 for stereo, buffer)
											# low buffer results in low delay


class Images:
	# loads all images
	def __init__(self):
		self.colours = {"white":(255,255,255), "black":(0,0,0), "red":(255,0,0), "green":(0,255,0), "blue":(0,0,255)}
		self.background = pygame.image.load("back2.png").convert()
		self.crosshair_image = pygame.image.load("crosshair.png").convert_alpha()
		self.crosshair_image = pygame.transform.scale(self.crosshair_image, (22,22)).convert_alpha()

		self.player_image = pygame.image.load("defender.png").convert_alpha()
		self.player_image = pygame.transform.scale(self.player_image,(84,94)).convert_alpha()

		self.blue_enemy = pygame.image.load("attacker.png").convert_alpha()
		self.blue_enemy = pygame.transform.flip(self.blue_enemy, False, True).convert_alpha()
		self.blue_enemy = pygame.transform.scale(self.blue_enemy,(84,94)).convert_alpha()
		self.green_enemy = pygame.image.load("1b.png").convert_alpha()
		self.green_enemy = pygame.transform.flip(self.green_enemy, False, True).convert_alpha()
		self.green_enemy = pygame.transform.scale(self.green_enemy,(84,94)).convert_alpha()
		self.yellow_enemy = pygame.image.load("5b.png").convert_alpha()
		self.yellow_enemy = pygame.transform.flip(self.yellow_enemy, False, True).convert_alpha()
		self.yellow_enemy = pygame.transform.scale(self.yellow_enemy,(100,130)).convert_alpha()

		self.player_laser = pygame.image.load("laser2.png").convert_alpha()
		self.player_laser = pygame.transform.scale(self.player_laser, (10,50)).convert_alpha()
		self.player_missile = pygame.image.load("newmissile.png").convert_alpha()
		self.player_missile = pygame.transform.scale(self.player_missile, (20,60)).convert_alpha()
		self.blue_laser = pygame.image.load("elaser.png").convert_alpha()
		self.blue_laser = pygame.transform.scale(self.blue_laser,(10,50)).convert_alpha()
		self.green_laser = pygame.image.load("greenlaser.png").convert_alpha()
		self.green_laser = pygame.transform.scale(self.green_laser, (10,50)).convert_alpha()
		self.yellow_orb = pygame.image.load("yelloworb.png").convert_alpha()
		self.yellow_orb = pygame.transform.scale(self.yellow_orb, (25,25)).convert_alpha()
		self.red_orb = pygame.image.load("redorb.png").convert_alpha()
		self.red_orb = pygame.transform.scale(self.red_orb, (25,25)).convert_alpha()

		self.laser_frame = pygame.image.load("frame1.png").convert_alpha()
		self.laser_frame = pygame.transform.scale(self.laser_frame, (50,50)).convert_alpha()
		self.missile_frame = pygame.image.load("frame2.png").convert_alpha()
		self.missile_frame = pygame.transform.scale(self.missile_frame, (50,50)).convert_alpha()

		self.dash_image = pygame.image.load("dash_available.png").convert_alpha()
		self.dash_image = pygame.transform.scale(self.dash_image, (40,40)).convert_alpha()

		self.no_dash_image = pygame.image.load("dash_not_available.png").convert_alpha()
		self.no_dash_image = pygame.transform.scale(self.no_dash_image, (40,40)).convert_alpha()

		self.settings_image = pygame.image.load("settingsimage.png").convert_alpha()
		self.settings_image = pygame.transform.scale(self.settings_image, (50,50)).convert_alpha()

		self.flashing_png = pygame.image.load("png.png").convert_alpha()

		self.shop_image = pygame.image.load("4b.png").convert_alpha()
		self.shop_image = pygame.transform.flip(self.shop_image, False, True).convert_alpha()
		self.shop_image = pygame.transform.scale(self.shop_image,(84,94)).convert_alpha()

		# Used for the explosion animations
		self.exp1 = pygame.image.load("exp1.png").convert_alpha()
		self.exp1 = pygame.transform.scale(self.exp1, (50,50))
		self.exp2 = pygame.image.load("exp2.png").convert_alpha()
		self.exp2 = pygame.transform.scale(self.exp2, (50,50))
		self.exp3 = pygame.image.load("exp3.png").convert_alpha()
		self.exp3 = pygame.transform.scale(self.exp3, (50,50))
		self.exp4 = pygame.image.load("exp4.png").convert_alpha()
		self.exp4 = pygame.transform.scale(self.exp4, (50,50))
		self.exp5 = pygame.image.load("exp5.png").convert_alpha()
		self.exp5 = pygame.transform.scale(self.exp5, (50,50))
		self.explosion_list = [self.exp1,self.exp2,self.exp3,self.exp4,self.exp5]
		# creates new list with larger explosions
		self.player_explosion_list = []
		for i in range(len(self.explosion_list)):
			self.explosion = pygame.transform.scale(self.explosion_list[i], (120,120)).convert_alpha()
			self.player_explosion_list.append(self.explosion)

		# Used for start menu
		self.start_background = pygame.image.load("newbg.gif").convert()

		

class Music:

	@staticmethod
	def set_music(music):
		pygame.mixer.music.load(music)
	
	@staticmethod
	def play_music():	
		pygame.mixer.music.play(-1)

	@staticmethod
	def stop_music():
		pygame.mixer.music.stop()

	@staticmethod
	def set_music_volume(volume):
		pygame.mixer.music.set_volume(volume / 100)

	@staticmethod
	def set_sound_volume(sound,volume):
		sound.set_volume(volume / 100)
