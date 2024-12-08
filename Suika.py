import pygame

# Utility vars
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
WIDTH, HEIGHT = 900, 600
FPS = 60

# Initialize the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

class Piece(pygame.sprite.Sprite):
	def __init__(self, pos, surf, group, movement_range, order= 1, rnm = 0):
		super().__init__(group)
		self.image = surf
		self.rect = self.image.get_rect(topleft=pos)
		self.vel_y = 0  # Vertical velocity
		self.falling = False
		self.direction = 1
		self.rnm = rnm
		self.order = order
		self.movement_range = movement_range
	def move(self, floors, other_pieces):
		if self.falling : 
			# Apply gravity
			self.vel_y += 1  # Gravity effect
			self.rect.y += self.vel_y

		# Check for collision with floors
		for floor in floors:
			if self.rect.colliderect(floor):
				self.rect.bottom = floor.top  # Place on top of the floor
				self.vel_y = 0  # Reset vertical velocity
	
		# Check for collision with other pieces
		for piece in other_pieces:
			if self.rect.colliderect(piece):
				if piece is not self:
					if self.order is not piece.order and self.rnm >= piece.rnm:
						self.rect.bottom = piece.rect.top  # Place on top of the floor
						self.vel_y = 0  # Reset vertical velocity
					if self.order == 3 and piece.order == 3 :
						self.rect.bottom = piece.rect.top  # Place on top of the floor
						self.vel_y = 0  # Reset vertical velocity

	def move_back_and_forth(self):
		# Move horizontally within the movement range
		self.rect.x += 5 * self.direction

		# Reverse direction if out of range
		if self.rect.x <= self.movement_range[0] or self.rect.x >= self.movement_range[1] - self.rect.width:
			self.direction *= -1  # Change direction

def main():
	# Initialize variables
	run = True
	clock = pygame.time.Clock()

	# Groups
	camera_group = pygame.sprite.Group()
	pieces_group = pygame.sprite.Group()

	# Floor setup
	floors = [
		pygame.Rect(0, HEIGHT - 20, WIDTH, 20),  # Main floor
	]

	# Piece setup
	red_square = pygame.Surface((50, 50))  # Size of the square (50x50)
	big_square = pygame.Surface((70, 70))  # Size of the square (50x50)
	red_square.fill(red)  # Fill the square with red color
	big_square.fill(red)  # Fill the square with red color
	
	piece = Piece(pos=(300, 100), surf=red_square, group=camera_group, movement_range=(100, 800))
	pieces_group.add(piece)
	pieces = []
	pieces.append(piece)
	i = 0 
	click_cooldown = 0  # Time remaining before another click is allowed
	cooldown_time = 500  # Cooldown time in milliseconds (0.5 seconds)
	# Game loop
	while run:
		dt = clock.tick(FPS)  # Control the frame rate
		if click_cooldown > 0:
			click_cooldown -= dt
  		
		screen.fill(white)
		# Draw floors
		for floor in floors:
			pygame.draw.rect(screen, black, floor)
		# Draw and update pieces
		camera_group.draw(screen)
		
		for piece in pieces:
			piece.move(floors, pieces)
			if not piece.falling:
				piece.move_back_and_forth()
			for other_piece in pieces:
				if piece != other_piece and piece.rect.colliderect(other_piece.rect):
					if piece.order == other_piece.order and piece.order !=3 :
						#remove one piece and increase the other's order
						piece.kill()
						pieces.remove(piece)
						i-=1
						#you should have a increase_order() fct here
						if other_piece.order == 1:
							other_piece.image.fill(green)
							other_piece.image = pygame.transform.scale(other_piece.image,(70,70))
							other_piece.rect = other_piece.image.get_rect(topleft=other_piece.rect.topleft)
							other_piece.order = 2
							break
						if other_piece.order == 2:
							other_piece.image.fill(blue)
							other_piece.image = pygame.transform.scale(other_piece.image,(100,100))
							other_piece.rect = other_piece.image.get_rect(topleft=other_piece.rect.topleft)
							other_piece.order = 3
							break
	

		for event in pygame.event.get():

			if event.type == pygame.MOUSEBUTTONDOWN :
				if event.button == 1:
					if click_cooldown <= 0:
						pieces[i].falling = True
						i += 1
						new_surface = pygame.Surface((50, 50))
						new_surface.fill(red)
						new_piece = Piece(pos=(300, 100), surf=new_surface, group=camera_group, movement_range=(100, 800), order = 1, rnm = i)
						pieces.append(new_piece)
						click_cooldown = cooldown_time

			if event.type == pygame.QUIT:
				run = False
				
		pygame.display.update()  # Update the screen

	pygame.quit()

if __name__ == "__main__":
	main()
