import pygame
import sys
import random


pygame.init()
clock = pygame.time.Clock()

game_font=pygame.font.Font('FontsFree-Net-04B_19__.ttf',48)
pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512)


screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy bird ')




bg_surface=pygame.image.load("background-day.png")
bg_surface=pygame.transform.scale2x(bg_surface)

floor_surface=pygame.image.load('base.png').convert()
floor_surface= pygame.transform.scale2x(floor_surface)
floor_x_pos=0


bird_downflap = pygame.transform.scale2x(pygame.image.load('bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('bluebird-upflap.png').convert_alpha())

bird_frames=[bird_upflap,bird_downflap,bird_midflap]
bird_index=0
bird_surface=bird_frames[bird_index]
bird_rect=bird_surface.get_rect(center=(100,512))

BIRDFLAP=pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,100)


pipe_surface=pygame.image.load('pipe-green.png').convert()
pipe_surface= pygame.transform.scale2x(pipe_surface)
pipe_list=[]
spawn=pygame.USEREVENT
pygame.time.set_timer(spawn,1200)
pipe_height=[500,600,400]


game_over_surface=pygame.transform.scale2x(pygame.image.load('renamed.png').convert_alpha())
game_over_rect=game_over_surface.get_rect(center=(288,512))


flap_sound=pygame.mixer.Sound('sfx_wing.wav')
hit_sound=pygame.mixer.Sound('sfx_hit.wav')
score_sound=pygame.mixer.Sound('sfx_point.wav')
score_countdown=100


#floor anime
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 800))
    screen.blit(floor_surface, (floor_x_pos+576, 800))

#Pipe functions
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    top_pipe=pipe_surface.get_rect(midbottom=(700,random_pipe_pos-200))
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    return top_pipe,bottom_pipe

def move_pipe(load):
    for m in load:
        m.centerx-=7
    return load




def draw_pipe(load):
    for m in load:
        if m.bottom>=1024:
            screen.blit(pipe_surface,m)
        else:
            flip_surface=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_surface, m)


def check_collision(load):
    for m in load:
        if bird_rect.colliderect(m):
            hit_sound.play()
            return False


    if bird_rect.top <=-100 or bird_rect.bottom>=900:
        return False

    return True


def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird, -bird_move*3,1)
    return new_bird


def bird_animation():
    new_bird=bird_frames[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird,new_bird_rect



def score_display(game_state):

    if (game_state=='main_game'):
        score_surface=game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect= score_surface.get_rect(center=(288,150))
        screen.blit(score_surface,score_rect)
    if (game_state=='game_over'):
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center=(288, 150))
        screen.blit(score_surface, score_rect)

        high_score_surface=game_font.render(f'High Score: {int(score)}', True, (255,255,255))
        high_score_rect=high_score_surface.get_rect(center=(288, 250))
        screen.blit(high_score_surface,high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score

    return high_score



#bird move variables

gravity=0.25
bird_move=0
game_active=True
score=0
high_score=0



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                bird_move=0
                bird_move-=5
                flap_sound.play()

            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(100,512)
                bird_move=0
                score=0

        if event.type==spawn:
            pipe_list.extend(create_pipe())

        if event.type==BIRDFLAP:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0

        bird_surface,bird_rect=bird_animation()






    screen.blit(bg_surface,(0,0))


    if game_active:
        bird_move += gravity
        rotation=rotate_bird(bird_surface)
        bird_rect.centery += bird_move
        screen.blit(rotation, bird_rect)

        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)

        game_active=check_collision(pipe_list)

        score+=0.01
        score_countdown-=1

        if score_countdown<=0:
            score_sound.play()
            score_countdown=100

        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score=update_score(score, high_score)
        score_display('game_over')




    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos < -576:
        floor_x_pos = 0





    pygame.display.flip()
    clock.tick(50)

