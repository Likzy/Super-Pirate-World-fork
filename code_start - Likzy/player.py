from settings import * 

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, collision_sprites):
		super().__init__(groups)
		self.image = pygame.Surface((48,56))
		self.image.fill('red')

		#rects
		self.rect = self.image.get_frect(topleft = pos)
		self.oldrect = self.rect.copy()
		# movement 
		self.direction = vector()
		self.speed = 200
		self.gravity = 1300
		#collision
		self.collision_sprites = collision_sprites

	def input(self):
		keys = pygame.key.get_pressed()
		input_vector = vector(0,0)
		if keys[pygame.K_RIGHT]:
			
			input_vector.x += 1
		if keys[pygame.K_LEFT]:
			
			input_vector.x -= 1
		self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

	def move(self, dt):
		self.rect.x += self.direction.x * self.speed * dt
		self.collision("horizontal")

		#vertical
		self.direction.y += self.gravity/2 * dt
		self.rect.y += self.direction.y * dt
		self.direction.y += self.gravity/2 * dt
		self.collision("vertical")
	def collision(self, axis):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.rect):
				if axis == "horizontal":
					#left
					if self.rect.left <= sprite.rect.right and self.oldrect.left >= sprite.oldrect.right:
						self.rect.left = sprite.rect.right
					#right
					if self.rect.right >= sprite.rect.left and self.oldrect.right <= sprite.oldrect.left:
						self.rect.right = sprite.rect.left
					
				else: #vertical
					#top
					if self.rect.top <= sprite.rect.bottom and self.oldrect.top >= sprite.oldrect.bottom:
						self.rect.top = sprite.rect.bottom
					#bottom
					if self.rect.bottom >= sprite.rect.top and self.oldrect.bottom <= sprite.oldrect.top:
						self.rect.bottom = sprite.rect.top
				self.direction.y = 0
					

	def update(self, dt):
		self.oldrect = self.rect.copy()
		self.input()
		self.move(dt)
