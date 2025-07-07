from window import *


class MenuStack:
	def __init__(self):
		self.login = Login()       # creates objects for all menus.
		self.main_menu = MainMenu()
		self.game = Game()
		self.shop_screen = Shop()
		self.leaderboard = Leaderboard()
		self.controls = Controls()
		self.options = Options()
		self.game_over = GameOver()
		self.menu_stack = [self.login]

	# used in the window class to determine what to do when button is pressed.
	def evaluate_button(self, menu):
		if menu == "main menu":
			self.push_menu_stack(self.main_menu)
		elif menu == "game":
			self.push_menu_stack(self.game)
		elif menu == "leaderboard":
			self.push_menu_stack(self.leaderboard)
		elif menu == "options":
			self.push_menu_stack(self.options)
		elif menu == "controls":
			self.push_menu_stack(self.controls)
		elif menu == "back":
			self.pop_menu_stack()
		elif menu == "quit":
			self.quit_to_main_menu()
		elif menu == "exit":
			pygame.quit()
			sys.exit()

	# pushes a menu on to the stack
	def push_menu_stack(self, menu):
		self.menu_stack.append(menu)
		self.mouse_visibility()
		if menu == self.game:
			Music.set_music("gameplaymusic.wav")
			Music.play_music()

	# pops a menu off of the stack
	def pop_menu_stack(self):
		self.menu_stack.pop(-1)
		self.mouse_visibility()

	# peaks at the top of the stack
	def peak_menu_stack(self):
		return self.menu_stack[-1]

	# removes everything in the stack apart from the first two items (login and main menu)
	# resets game menu and shop menu objects, so it doesn't continue from where they quit.
	def quit_to_main_menu(self):
		self.menu_stack = self.menu_stack[:2]
		self.reset_game_object()
		self.reset_shop_screen_object()
		Music.set_music("calmbackground.wav")
		Music.play_music()
		pygame.mouse.set_visible(True)

	# Used to reset game after quitting to menu
	def reset_game_object(self):
		del self.game
		self.game = Game()

	# if the player dies or starts a new game the shop menu object will have to be reset.
	def reset_shop_screen_object(self):
		del self.shop_screen
		self.shop_screen = Shop()

	# Used to determine whether the mouse should be visible or not
	def mouse_visibility(self):
		if self.peak_menu_stack() == self.game:
			pygame.mouse.set_visible(False)
		else:
			pygame.mouse.set_visible(True)




