import pygame
import sys
import random
import time

def game_floor():
    screen.blit(floor_base, (floor_x_pos, 900))
    screen.blit(floor_base, (floor_x_pos + 576, 900))

    #collisions check function
def check_collision(pipes):
    #collisions with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False

    #Checking if the bird is under the ground's level or over the top edge of screen
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        die_sound.play()
        return False
    return True

    #creating the pipes
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos-300))
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    return bottom_pipe, top_pipe

    #moving the pipes
def move_pipies(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

pygame.init()
clock = pygame.time.Clock()

#varbiables - can be changed by the user. (Default: gravity: 0.35, bird_movement: 0)
gravity = 0.35
bird_movement = 0

#Set the window size
screen = pygame.display.set_mode((576, 1024))

#Loading all the PNG files and scale them to the window size.
#convert alpha - for transparent background images.
#convert - for regular images, without transparent background.
background = pygame.image.load("assets/sprites/background-day.png").convert()
background = pygame.transform.scale2x(background)

bird = pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)

floor_base = pygame.image.load("assets/sprites/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0

message = pygame.image.load("assets/sprites/message.png").convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center = (288, 512))

pipe_surface = pygame.image.load("assets/sprites/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400, 600, 800]

#Respawning the pipes
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

#Adding rectangle over the bird to detect collisions
bird_rect = bird.get_rect(center=(100, 512))

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
die_sound = pygame.mixer.Sound('assets/audio/die.wav')

#Active game Flag
game_active = True

while True:

    #Enable to close the game using navigation bar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Keys event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100, 512)
                bird_movement = 0
                pipe_list.clear()
                game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.blit(background, (0, 0))
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)

        #Drawing the pipes
        pipe_list = move_pipies(pipe_list)
        draw_pipes(pipe_list)

        #checking collisions
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)

    #Creating ground
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -576: #Repeting ground image
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)