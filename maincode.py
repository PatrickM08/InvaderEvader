from MenuStack import *

FPS = 120  # how many loops per second.
clock = pygame.time.Clock()
previous_time = time.time()

# menu stack object
menu_stack = MenuStack()

# starts the menu music.
Music.set_music("calmbackground.wav")
Music.play_music()

while True:
	clock.tick(FPS)
	current_time = time.time()
	delta_time = current_time - previous_time
	previous_time = current_time				# Used to find the time passed after each frame, so we can keep a constant speed
												# no matter what the fps is.

	menu = menu_stack.peak_menu_stack() # finds menu currently at the top of stack.
	menu.set_delta_time(delta_time)
	menu.set_menu_stack(menu_stack)

	menu.check_events()
	menu.background()
	
	if menu == menu_stack.game:  # these are methods specific to the main game.
		menu.waves()
		menu.update_entities()
		menu.check_collisions()
		menu.check_lives()
	
	menu.create_buttons()	
	menu.get_mouse_position()
	menu.button_pressed()
	pygame.display.update()
