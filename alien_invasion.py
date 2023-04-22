import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Ogólna klasa przeznaczona do zarządzania zasobami i sposobem 
	działania gry."""

	def __init__(self):
 		"""Inicjalizacja gry i utworzenie jej zasobów."""
 		pygame.init()
 		self.settings = Settings()

 		self.screen = pygame.display.set_mode((self.settings.screen_width, 
 			self.settings.screen_height))

 		pygame.display.set_caption("Inwazja obcych")

 		self.ship = Ship(self)
 		self.bullets = pygame.sprite.Group()
 		self.aliens = pygame.sprite.Group()

 		self._create_fleet()

	def run_game(self):
		"""Rozpoczęcie pętli głównej gry."""
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()

	def _check_events(self):
		"""Reakcja na zdarzenia generowane przez klawiaturę i mysz."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		"""Reakcja na naciśnięcie klawisza."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_ESCAPE:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Reakcja na zwolnienie klawisza"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Utworzenie nowego pocisku i dodanie go do grupy pocisków."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Uaktualnienie położenia pocisków i usunięcie tych niewidocznych
		na ekranie."""
		self.bullets.update()

		#Usuwanie pocisków, które znajdują się poza ekranem.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

	def _create_fleet(self):
		"""Utworzenie pełnej floty obcych."""
		#Utworzenie obcego i ustalenie liczby obcych, którzy zmieszą się w rzędzie.
		#Odległość między poszczególnymi obcymi jest równa szerokości obcego.
		alien = Alien(self)
		alien_width = alien.rect.width
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		#Utworzenie pierwszego rzędu obcych.
		for alien_number in range(number_aliens_x):
			#Utworzenie obcego i umieszczenie go w rzędzie.
			alien = Alien(self)
			alien.x = alien_width + 2 * alien_width * alien_number
			alien.rect.x = alien.x
			self.aliens.add(alien)


	def _update_screen(self):
		"""Uaktualnienie obrazów na ekranie i przejście do nowego ekranu."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		pygame.display.flip()

if __name__ == '__main__':
	#Utworzenie egzemplarza gry i jej uruchomienie
	ai = AlienInvasion()
	ai.run_game()