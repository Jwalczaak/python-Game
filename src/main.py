import pygame
import math

pygame.init()
fps = 60
timer = pygame.time.Clock()
fontFamily = pygame.font.Font('assets/fonts/customizedFont.ttf',32)
width = 900
height = 800
screenSize = pygame.display.set_mode([width, height])
mapsArray = []
gunsArray = []
targetArray = [[],[],[]]
targets = {1: [10, 5, 3],
           2: [12, 8, 5],
           3: [16, 12, 8, 3]}
level = 1
userPoints = 0
allShots = 0
ammo = 0
time_passed = 0
time_remaining = 0
counter = 1
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
smallfont = pygame.font.SysFont('Corbel',35)
quitButton = smallfont.render('Quit' , True , color)
startButton = smallfont.render('Start' , True , color)
isShoted = False

for i in range(1,4):
    mapsArray.append(pygame.image.load(f'assets/maps/{i}.png'))
    gunsArray.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{i}.png'),(100,100)))
    if i < 3:
        for j in range(1,4):
            targetArray[i - 1].append(pygame.transform.scale(pygame.image.load(f'assets/targets/{i}/{j}.png'),(120 - (j*18), 80 - (j*12) )))
    else:
        for j in range(1,5):
            targetArray[i - 1].append(pygame.transform.scale(pygame.image.load(f'assets/targets/{i}/{j}.png'),(120 - (j*18), 80 - (j*12) )))

# drawing user point, time, number of shots
def createUserScore():
    global time_text
    points_text = fontFamily.render(f'Points: {userPoints}', True, 'White')
    screenSize.blit(points_text,(320, 660))
    shots_text = fontFamily.render(f'Total Shots: {allShots}', True, 'White')
    screenSize.blit(shots_text, (320,687))
    time_text = fontFamily.render(f'Total Elapsed: {time_passed}', True, 'White')
    screenSize.blit(time_text, (320,714))    

# drawing gun on the bottom of screen
def draw_gun():
    mouse_pos = pygame.mouse.get_pos()
    gun_point = (width/2, height - 200)
    lasers = ['red', 'purple', 'green']
    clicks = pygame.mouse.get_pressed()
    
    # rotating gun up and donw it depends from mouse coursor
    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1] - gun_point[1])/(mouse_pos[0] - gun_point[0])
    #if mouse is equal gun ox then gun looks on the sky 
    else:
        slope = -100000
    angle = math.atan(slope)
    rotation = math.degrees(angle)
   
      # rotating gun left and right it depends from mouse coursor
    if mouse_pos[0] < width / 2:
        gun = pygame.transform.flip(gunsArray[level-1],True,False)
        if mouse_pos[1] < 600:
            screenSize.blit(pygame.transform.rotate(gun,90 - rotation),(width/2 - 90, height -250))
            if clicks[0]:
                # after click is drawing dot(bullet)
                pygame.draw.circle(screenSize, lasers[level - 1], mouse_pos , 5)
    else:
        gun = gunsArray[level - 1]
        if mouse_pos[1] < 600:
            screenSize.blit(pygame.transform.rotate(gun,270 - rotation),(width/2 - 30, height - 250))
            if clicks[0]:
                pygame.draw.circle(screenSize, lasers[level - 1], mouse_pos , 5)


def  targetsMoving(coords):
    if level == 1 or level == 2:
        max_val = 3
    else:
        max_val = 4
    for i in range(max_val):
        for j in range(len(coords[i])):
            my_coords = coords[i][j]
            if my_coords[0] < -150:
                coords[i][j] = (width, my_coords[1])
            
            else:
                coords[i][j] = (my_coords[0] - 2**i, my_coords[1])

    return coords

# rendering next levels
def renderLevel(coords):
    if level == 1 or level == 2:
        target_rects = [[],[],[]]
    else:
         target_rects = [[],[],[],[]]
    
    for  i in range(len(coords)):
        for j in range(len(coords[i])):
            # rendering position enemies
            target_rects[i].append(pygame.rect.Rect((coords[i][j][0] + 20,coords[i][j][1]), (60 - i*12, 60 - i*12)))
            screenSize.blit(targetArray[level-1][i],coords[i][j])

    return target_rects

def shotService(targets,coords):
    global userPoints
    mouse_pos = pygame.mouse.get_pos()
    for i in range(len(targets)):
        for j in range(len(targets[i])):
            if targets[i][j].collidepoint(mouse_pos):
                coords[i].pop(j)
    # number of point is depends from kind of "monsters"
                userPoints += 10 + 10 * (i**2)
    return coords


    # creating menu
def printMenu():
    mouse = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
     
    if level == 3:
        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
         pygame.draw.rect(screenSize,color_light,[width/2,height/2,140,40])

        else:
         pygame.draw.rect(screenSize,color_dark,[width/2, height/2,140,40])
        screenSize.blit(quitButton , (width/2+50,height/2))

#initialize enemy coordinates
coords1 = [[],[],[]]
coords2 = [[],[],[]]
coords3 = [[],[],[],[]]

for i in range(3):
    my_list = targets[1]
    for j in range(my_list[i]):
        coords1[i].append((width//(my_list[i]) * j, 300 - (i * 150) + 30 * (j%2)))

for i in range(3):
    my_list = targets[2]
    for j in range(my_list[i]):
         coords2[i].append((width//(my_list[i]) * j, 300 - (i * 150) + 30 * (j%2)))
        
for i in range(4):
    my_list = targets[3]
    for j in range(my_list[i]):
         coords3[i].append((width//(my_list[i]) * j, 300 - (i * 100) + 30 * (j%2)))

    # game has been started
run = True

while run:
    timer.tick(fps)
    # counting time
    if level != 0 and level != 4:
     if counter < 60 : 
        counter +=1
   
#    setting game's bg
    screenSize.fill('black')
    screenSize.blit(mapsArray[level - 1],(0,0))
 
    # Checking current level and calling functions for them
    if level == 1:
        target_boxes = renderLevel(coords1)
        coords1 = targetsMoving(coords1)
        if isShoted:    
            coords1 = shotService(target_boxes,coords1)
            isShoted = False
  
    elif level == 2:
        target_boxes = renderLevel(coords2)
        coords2 = targetsMoving(coords2)
        if isShoted:    
            coords2 = shotService(target_boxes,coords2)    
            isShoted = False
    elif level == 3:
         target_boxes = renderLevel(coords3)
         coords3 =  targetsMoving(coords3)
         if isShoted:    
            tree_coords = shotService(target_boxes,coords3)
            isShoted = False
    if level > 0:  
        draw_gun()
        createUserScore()
    else: 
        printMenu()
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            if (0 < mouse_position[0] < width) and (0 < mouse_position[1] < height - 200):
                isShoted  = True
                allShots  += 1
        if event.type == pygame.MOUSEBUTTONDOWN:       
            if width/2 <= mouse_position[0] <= width/2+140 and height/2 <= mouse_position[1] <= height/2+40:
                run = False
          
                 
                
    
    if level > 0:
        if target_boxes == [[],[],[]] and level <3 :
            level += 1
        elif target_boxes == [[],[],[],[]] and level  == 3:
           
            printMenu()
        print(level)   
    pygame.display.flip()
pygame.quit()
