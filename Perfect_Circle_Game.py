import pygame, sys, time, math
from pygame.locals import *

# Initializing
pygame.init()

# Display
HEIGHT, WIDTH = 800, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Perfect Circle')
screen.fill('white')

# Font
myFont = pygame.font.SysFont('times new roman', 40)
fail_txt = myFont.render('Draw a full circle', False, (0, 0, 0))
time_out = myFont.render('Too slow', False, (0, 0, 0))
close_txt = myFont.render('Too close to dot', False, (0, 0, 0))

# Variables
circle_r = 10
center_x = WIDTH // 2
center_y = HEIGHT // 2
mouse_pos = (0, 0)
start_time = time.time()
draw = False
last_pos = None  
f = c = percent = 0
x1=y1=i=k=angle=0

# Draw the center point
pygame.draw.circle(screen, (0,255,0), (center_x, center_y), circle_r)
pygame.display.update()

# Game loop
while True:
    for event in pygame.event.get():
        past = time.time() - start_time
        sec = int(past % 60)

        if k!=0:
            start_time = time.time()

        # Too slow
        if 6 < sec:
            mouse_pos = (0, 0)
            draw = False
            last_pos = None
            screen.fill(pygame.Color('white'), (center_x/1.25, 0, WIDTH, 40))
            screen.blit(time_out, (center_x/1.25, 0))
            pygame.mixer.Sound("Wrong-answer-sound-effect.mp3").play()
            f=1
            start_time=time.time()
        
        # Event -> QUIT
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Implement the ability to draw with the mouse
        elif event.type == MOUSEMOTION:
            if draw:
                mouse_pos = pygame.mouse.get_pos()
                th_x, th_y = mouse_pos
                if c == 0:
                    x, y=mouse_pos
                    l = math.sqrt(pow(x-center_x,2)+pow(y-center_y,2))
                    c += 1
        
                if c == 2:
                    x1, y1 = mouse_pos
        
                if f != 0:
                    screen.fill('white')
                    pygame.draw.circle(screen, (0,255,0), (center_x, center_y), circle_r)
                    pygame.display.update()
                    draw = True
                    f = 0

                # As the quality of the circle deteriorates, change the color to more red
                if last_pos is not None:
                    i = 100 - percent
                    pygame.draw.line(screen, (2*abs(int(i)), 255-2*abs(int(i)), 0), last_pos, mouse_pos, 5)
                    
                    # Coordinates of an ideal circle / Starting position: left corner 
                    if x < center_x:
                        if x1 != 0 and y1 != 0:   
                            # If line goes down   
                            if y1 < y:
                                angle = math.atan(-1*(y-center_y)/(x-center_x))+math.pi-0.7*c*math.pi/180
                                th_y = l*math.sin(angle) 
                                th_x = l*math.cos(angle)
                            
                            # If line goes up
                            if y1>y:
                                angle = math.atan(-1*(y-center_y)/(x-center_x))+math.pi+0.7*c*math.pi/180
                                th_y = l*math.sin(angle) 
                                th_x = l*math.cos(angle)
                    
                    # Starting position: right corner
                    if x>center_x:
                        if x1 != 0 and y1 != 0:      
                            # If line goes down
                            if y1>y :
                                angle = math.atan(-1*(y-center_y)/(x-center_x))+math.pi-0.7*c*math.pi/180
                                th_y = l*math.sin(angle) 
                                th_x = l*math.cos(angle)
                            
                            # If line goes up
                            if y1<y:
                                angle = math.atan(-1*(y-center_y)/(x-center_x))+math.pi+0.7*c*math.pi/180
                                th_y = l*math.sin(angle)
                                th_x = l*math.cos(angle)
                    c += 1
                last_pos = mouse_pos
                x, y = last_pos 

                # Demonstrate as a percentage how perfect the circle is
                percent = 100-100*(abs(((center_x+th_x)-x)/x)+abs(((center_y-th_y)-y)/y))/2 
                if percent < 0:
                    percent = 0
                screen.fill(pygame.Color("white"), (center_x/1.25, 0, HEIGHT, 40))
                percentage = myFont.render(f'{round(percent,1)}%', False, (0, 0, 0))
                screen.blit(percentage, (center_x/1.25,0))
        
                # Failure if the mouse is out of range of the screen
                if x > WIDTH or y > HEIGHT or x < 0 or y < 0:
                    draw = False
                    last_pos = None
                    mouse_pos = (0, 0)
                    screen.fill(pygame.Color("white"), (center_x/1.25, 0, HEIGHT, 40))
                    screen.blit(fail_txt, (center_x/1.25,0))
                    f=1
                
                # Too close to dot
                elif(pow((x-center_x),2) + pow((y-center_y),2) < pow(4*circle_r,2)):
                    draw = False
                    last_pos = None
                    mouse_pos = (0, 0)
                    screen.fill(pygame.Color("white"), (center_x/1.25, 0, HEIGHT, 40))
                    screen.blit(close_txt, (center_x/1.25,0))
                    f = 1
                    c = 0 
        
        # Releasing the button
        elif event.type == MOUSEBUTTONUP:
            mouse_pos = (0, 0)
            draw = False
            last_pos = None
            k = f = 1
            c = 0
        
        # Moving the mouse
        elif event.type == MOUSEBUTTONDOWN:
            draw = True
            if k == 1:
                screen.fill('white')
                pygame.draw.circle(screen, (0,255,0), (center_x, center_y), circle_r)
                pygame.display.update()
                k = 0
    pygame.display.update()
