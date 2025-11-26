# 1 - Import library
import pygame
from pygame.locals import *
import math
import random

# ---------------- RESET GAME FUNCTION ----------------
def reset_game():
    global keys, playerpos, acc, arrows, paused, badtimer, badtimer1
    global badguys, healthvalue, start_time, paused_time_total
    global running, exitcode, level

    keys = [False, False, False, False]
    playerpos=[100,100]
    acc=[0,0]
    arrows=[]
    paused = False
    badtimer=100
    badtimer1=0
    badguys=[[1280,100]]
    healthvalue=256

    start_time = pygame.time.get_ticks()
    paused_time_total = 0
    running = 1
    exitcode = 0


# ---------------- PAUSE FUNCTION ----------------
def pause():
    pygame.mixer.music.pause()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0,0,0,100))
    screen.blit(overlay, (0, 0))
    menu_width, menu_height = 400, 250
    menu_x = (width - menu_width) // 2
    menu_y = (height - menu_height) // 2
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    pygame.draw.rect(screen, (30, 30, 30), menu_rect, border_radius=12)
    pygame.draw.rect(screen, (255,255,255), menu_rect, 2, border_radius=12)

    pause_text = font.render("Paused", True, (255,255,255))
    resume_text = small_font.render("Press ESC to Resume", True, (255,255,255))
    quit_text = small_font.render("Press Q to Quit", True, (255,255,255))
    
    screen.blit(pause_text, (menu_x + (menu_width - pause_text.get_width()) // 2, menu_y + 30))
    screen.blit(resume_text, (menu_x + (menu_width - resume_text.get_width()) // 2, menu_y + 100))
    screen.blit(quit_text, (menu_x + (menu_width - quit_text.get_width()) // 2, menu_y + 140))
    
    pause_start = pygame.time.get_ticks()
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                exit(0)
            elif event.type==MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if (position[0] >= button[0]) and (position[0] <= button[0]+button[2]) and (position[1]>=button[1]) and (position[1]<=button[1]+button[3]):
                    paused = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                paused = False
        
        button = pygame.draw.circle(screen, (255, 255, 255), (width-30, 30), 20)
        pygame.draw.rect(screen, (0, 0, 0), (width-26, 18 ,7,25))
        pygame.draw.rect(screen, (0, 0, 0), (width-42, 18 ,7,25))
        pygame.display.flip()

    pause_duration = pygame.time.get_ticks() - pause_start
    pygame.mixer.music.unpause()
    return pause_duration


# 2 - Initialize the game
pygame.init()
clock = pygame.time.Clock()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
keys = [False, False, False, False]
playerpos=[100,100]
acc=[0,0]
arrows=[]
paused = False
badtimer=100
badtimer1=0
badguys=[[1280,100]]
healthvalue=256
start_time = pygame.time.get_ticks()
paused_time_total = 0
pygame.mixer.init()

# ----- LEVEL SELECTION SCREEN -----
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 32)

selecting = True
level = 1

while selecting:
    screen.fill((30, 30, 30))
    title = font.render("CHOOSE LEVEL", True, (255, 255, 255))
    screen.blit(title, (width // 2 - 200, height // 2 - 150))
    
    font_small = pygame.font.Font(None, 50)
    screen.blit(font_small.render("1 - Level 1 (Easy)", True, (144,238,144)), (width // 2 - 150, height // 2 - 50))
    screen.blit(font_small.render("2 - Level 2 (Normal)", True, (255,165,0)), (width // 2 - 150, height // 2))
    screen.blit(font_small.render("3 - Level 3 (Hard)", True, (255,0,0)), (width // 2 - 150, height // 2 + 50))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                level = 1
                selecting = False
            elif event.key == pygame.K_2:
                level = 2
                badtimer1 -= 10
                selecting = False
            elif event.key == pygame.K_3:
                level = 3
                badtimer1 += 5
                selecting = False


# 3 - Load images + sounds
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg=badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
healthbar = pygame.transform.scale(healthbar,(263,20)) 
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
gameover = pygame.transform.scale(gameover,(1280,720))
youwin = pygame.image.load("resources/images/youwin.png")
youwin = pygame.transform.scale(youwin,(1280,720))
# 3.1 - Load audio
death = pygame.mixer.Sound("resources/audio/explode.wav")
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.1)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - game loop
running = 1
exitcode = 0

while True:     # MASTER GAME LOOP WITH RESTART SUPPORT

# 5 - clear the screen before drawing it again
    running = 1
    while running:
        badtimer -= 1
        screen.fill(0)
# 6 - draw the player on the screen at X:100, Y:100 
        for x in range(int(width/grass.get_width())+1):
            for y in range(int(height/grass.get_height())+1):
                screen.blit(grass,(x*100,y*100))
        screen.blit(castle,(0,30))
        screen.blit(castle,(0,135))
        screen.blit(castle,(0,240))
        screen.blit(castle,(0,345 ))
        screen.blit(castle,(0,450))
        screen.blit(castle,(0,555))
# 6.1 - Set player position and rotation        
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(playerrot, playerpos1) 
# 6.2 - Draw arrows      
        for bullet in arrows[:]:
            velx=math.cos(bullet[0])*10
            vely=math.sin(bullet[0])*10
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>1280 or bullet[2]<-64 or bullet[2]>720:
                arrows.remove(bullet)
            else:
                arrow1 = pygame.transform.rotate(arrow, 360 - bullet[0] * 57.29)
                screen.blit(arrow1, (bullet[1], bullet[2]))
# 6.3 - Draw badgers     
        if badtimer<=0:
            badguys.append([1280, random.randint(30,600)])
            badtimer=100-(badtimer1*2)
            if badtimer1<35:
                badtimer1+=5
        
        for badguy in badguys[:]:
            badguy[0]-=2
            badrect=pygame.Rect(badguyimg.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if badguy[0] < -64:
                badguys.remove(badguy)
            elif badrect.left < 64:
                hit.play()
                healthvalue -= random.randint(5,20)
                badguys.remove(badguy)
            else:
                for bullet in arrows[:]:
                    bullrect=pygame.Rect(arrow.get_rect())
                    bullrect.left=bullet[1]
                    bullrect.top=bullet[2]
                    if badrect.colliderect(bullrect):
                        enemy.play()
                        acc[0]+=1
                        badguys.remove(badguy)
                        arrows.remove(bullet)
                        break
        
        for badguy in badguys:
            screen.blit(badguyimg, badguy)
# 6.4 - Draw clock      
        remaining_ms = 90000 - pygame.time.get_ticks() + paused_time_total
        minutes = remaining_ms // 60000
        seconds = (remaining_ms // 1000) % 60
        font = pygame.font.Font(None, 50)
        survivedtext = font.render(f"{minutes}:{str(seconds).zfill(2)} sec", True, (0, 0, 0))
        screen.blit(survivedtext, (600,5))
# 6.5 - Draw health bar      
        screen.blit(healthbar, (1000,690))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+1004,693))
        
        button = pygame.draw.circle(screen, (255, 255, 255), (width-30, 30), 20)
        pygame.draw.rect(screen, (0, 0, 0), (width-26, 18 ,7,25))
        pygame.draw.rect(screen, (0, 0, 0), (width-42, 18 ,7,25))
# 7 - update the screen
        pygame.display.flip()
# 8 - loop through the events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key==K_w: keys[0]=True
                if event.key==K_a: keys[1]=True
                if event.key==K_s: keys[2]=True
                if event.key==K_d: keys[3]=True
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w: keys[0]=False
                if event.key==pygame.K_a: keys[1]=False
                if event.key==pygame.K_s: keys[2]=False
                if event.key==pygame.K_d: keys[3]=False
                if event.key==pygame.K_ESCAPE:
                    paused_time_total += pause()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    paused_time_total += pause()
                shoot.play()
                acc[1]+=1
                arrows.append([angle,playerpos1[0]+32,playerpos1[1]+32])
# 9 - Move player      
        if keys[0] and playerpos[1]>23: playerpos[1]-=5
        if keys[2] and playerpos[1]<height-20: playerpos[1]+=5
        if keys[1] and playerpos[0]>23: playerpos[0]-=5
        if keys[3] and playerpos[0]<width-20: playerpos[0]+=5
#10 - Win/Lose check  
        if pygame.time.get_ticks()>=90000+paused_time_total:
            running=0
            exitcode=1
        if healthvalue<=0:
            death.play()
            running=0
            exitcode=0
    
    # ---------------- END OF ORIGINAL GAME LOOP ----------------
# 11 - Win/lose display
    if acc[1] != 0:
        accuracy = acc[0] / acc[1] * 100
    else:
        accuracy = 0

    if exitcode==0:
        pygame.mixer.music.stop()
        text = small_font.render("Accuracy: {:.1f}%".format(accuracy), True, (255,0,0))
        screen.blit(gameover,(0,0))
        screen.blit(text, (width//2 - text.get_width()//2, height//2 + 20))
    else:
        pygame.mixer.music.stop()
        text = small_font.render("Accuracy: {:.1f}%".format(accuracy), True, (255,255,255))
        screen.blit(youwin,(0,0))
        screen.blit(text, (width//2 - text.get_width()//2, height//2 + 20))

    # ----------- RESTART BUTTON (TEXT ONLY) ------------
    restart_font = pygame.font.SysFont(None, 60)
    restart_text = restart_font.render("RESTART", True, (255,255,255))
    restart_rect = restart_text.get_rect(center=(width//2, height//2 + 120))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    # -------- WAIT FOR RESTART CLICK --------
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    reset_game()
                    pygame.mixer.music.play(-1, 0.0)
                    waiting = False  # restart game

        clock.tick(30)

