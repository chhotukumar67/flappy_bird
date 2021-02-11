import pygame
import sys
import random

def draw_floor():
	screen.blit(floor_surface, (floor_x,screen_height-125))
	screen.blit(floor_surface, (floor_x+screen_width,screen_height-125))
def create_pip():
	random_pip_pos = random.choice(pipe_height)
	rand_dist = random.randrange(200,300,20)
	top_pipe = pipe_surface.get_rect(midbottom = (screen_width+200, random_pip_pos-rand_dist))
	bottom_pipe = pipe_surface.get_rect(midtop = (screen_width+200, random_pip_pos))
	return top_pipe, bottom_pipe
def move_pipes(pipes):
	for pipe in pipes:
		pipe[0].centerx -=speed
		pipe[1].centerx -=speed
	visible_pipe = [pipe for pipe in pipes if pipe[0].right > -50]
	return visible_pipe
def draw_pipes(pipes):
	for pipe in pipes:
		flip_surface = pygame.transform.flip(pipe_surface,False, True)
		screen.blit(flip_surface, pipe[0])
		screen.blit(pipe_surface,pipe[1])
def check_collision(pipes):
	global can_score
	if bird_rect.top <= -10 or bird_rect.bottom >= screen_height-125:
		death_sound.play()
		can_score = True
		return False
	for pipe in pipes:
		if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
			can_score = True
			death_sound.play()
			return False
	return True # if no collision happen
def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement*3,1)
	return new_bird
def bird_animation():
	new_bird_surf = bird_frames[bird_index]
	new_rect_surf = new_bird_surf.get_rect(center = (100, bird_rect.centery))
	return new_bird_surf, new_rect_surf
def score_display(game_state):
	if game_state == "main_game":
		score_surface = score_font.render("Score : "+str(int(score)),True, (255,255,255))
		# high_score_surface = game_font.render('High Score', True, (255,255,255))
		score_rect = score_surface.get_rect(center = (screen_width/2,80))
		screen.blit(score_surface, score_rect)
	if game_state == "game_over":
		score_surface = score_font.render("Score : "+str(int(score)),True, (255,255,255))
		# high_score_surface = game_font.render('High Score', True, (255,255,255))
		score_rect = score_surface.get_rect(center = (screen_width/2,80))
		screen.blit(score_surface, score_rect)

		# score_surface = game_font.render(str(score),True, (255,255,255))
		high_score_surface = high_score_font.render("High Score : "+str(int(high_score)), True, (255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (screen_width/2,640))
		screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score
def pipe_score_check():
	global score, can_score
	if pipe_list:
		for pipe in pipe_list:
			if 95 <pipe[0].centerx <=105 and can_score :
				score +=1
				score_sound.play()
				can_score = False
			if pipe[0].centerx < 95:
				can_score = True

# Initialize pygame
pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)
pygame.init()
clock = pygame.time.Clock()
fps = 120 # Frames per second
score_font = pygame.font.Font("04B_19.TTF", 32)
high_score_font = pygame.font.Font("04B_19.TTF",26)


#Game variables
gravity = 0.25
bird_movement = 0
speed = 4
go_up = 10
game_active = True
score = 0
high_score = 0
score_sound_countdown = 100
can_score = True

#color
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

# Screen and surfaces
screen_width = 50*9
screen_height = 50*16
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load("sprites/redbird-midflap.png")
pygame.display.set_icon(icon)
bg_surface = pygame.image.load("sprites/background-day.png").convert() 
# add covert() method to work faster
bg_surface =pygame.transform.scale(bg_surface,(screen_width, screen_height))

# floor running surface
floor_surface = pygame.image.load("sprites/base.png").convert()
floor_surface =pygame.transform.scale(floor_surface,(screen_width, 125))
floor_x = 0

# Bird surface
bird_downflap = pygame.transform.scale(pygame.image.load("sprites/bluebird-downflap.png").convert_alpha(), (51,36))
bird_midflap = pygame.transform.scale(pygame.image.load("sprites/bluebird-midflap.png").convert_alpha(), (51,36))
bird_upflap = pygame.transform.scale(pygame.image.load("sprites/bluebird-upflap.png").convert_alpha(), (51,36))
bird_frames = [bird_downflap,bird_midflap, bird_upflap]
bird_index = 0

bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect()
bird_rect.center = (100,250)
BIRDFLAP = pygame.USEREVENT + 1 # Plus 1, because we have already have a user_event 
pygame.time.set_timer(BIRDFLAP, 200)


# bird_surface = pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface,(51,36))
# bird_rect = bird_surface.get_rect()
# bird_rect.center = (100,250)


# Pipe surface
pipe_surface = pygame.image.load("sprites/pipe-green.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface,(65,600))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT # The variable need not to be capital
pygame.time.set_timer(SPAWNPIPE, 1200) # 1200 mili seconds = 1.2 second
pipe_height = [400,450,500,550,600]


game_over_surface = pygame.image.load("sprites/message.png").convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (screen_width-250, screen_height-370))
game_over_rect = game_over_surface.get_rect(center = (screen_width/2,screen_height/2))



game_over_text_surface = pygame.image.load("sprites/gameover.png").convert_alpha()
game_over_text_surface = pygame.transform.scale(game_over_text_surface, (288, 63))
game_over_tect_rect = game_over_text_surface.get_rect(center = (screen_width/2,screen_height/2-12))
# Music and Sound 
flap_sound = pygame.mixer.Sound("audio/wing.wav")
death_sound = pygame.mixer.Sound("audio/hit.wav")
score_sound = pygame.mixer.Sound("audio/point.wav")

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active == True:
				flap_sound.play()
				bird_movement = 0
				bird_movement -= go_up
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				bird_rect.center = (100,250)
				pipe_list.clear()
				bird_movement = 0
				bird_movement -= 4 
				score = 0

		if event.type == SPAWNPIPE:
			if game_active:
				pipe_list.append(create_pip())
		if event.type == BIRDFLAP:
			bird_index = (bird_index + 1 )%3
			bird_surface, bird_rect = bird_animation()


	screen.fill(blue)
	screen.blit(bg_surface, (0,0))

	if game_active:
		# Bird
		bird_movement += gravity
		bird_rect.centery += bird_movement
		rotated_bird = rotate_bird(bird_surface)
		screen.blit(rotated_bird,bird_rect)
		game_active = check_collision(pipe_list)

		# pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

		# Score system
		pipe_score_check()
		score_display("main_game")
	else:
		screen.blit(game_over_surface, game_over_rect)
		pygame.draw.rect(screen, (90,198,219), pygame.Rect(screen_width/2-288/2, screen_height/2-30-25, 288,85)) 
		screen.blit(game_over_text_surface, game_over_tect_rect)
		high_score = update_score(score, high_score)
		score_display("game_over")

	# floor
	floor_x -= speed
	draw_floor()
	if floor_x <= -1*screen_width:
		floor_x = 0



	pygame.display.update()
	clock.tick(fps)

