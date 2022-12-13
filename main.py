import random
import time

import pygame as pg
import pygame.mouse
import json
# crearea de display

def game(jsonFile):
    
    with open(jsonFile, 'r') as fcc_file:
        data = json.load(fcc_file)
    
    print(data)

    WIDTH = int(data['WIDTH']) #latime 
    HEIGTH = int(data['HEIGTH']) #lungime
    
    SIZE = 20 #casuta

    FILL_COLOR = (1, 0, 35) 
    SNAKE_COLOR = (255, 255, 255) #alb
    FOOD_COLOR = (255, 0, 0) #rosie
    OBSTACLE_COLOR = (255,165,0) #portocaliu
    screen = pg.display.set_mode((WIDTH, HEIGTH))

    pg.display.set_caption("Snake")

    START_IMAGE = pg.image.load('start_button_low_di.png').convert_alpha()
    STOP_IMAGE = pg.image.load('stop_button.png').convert_alpha()

    pg.display.update()


    # creem o clasa oentru butoanele disponibile

    class Buttons:
        def __init__(self, x, y, image):
            self.image = pg.transform.scale(image, (100, 40))
            self.x = x
            self.y = y
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self):
            action = False

            position = pygame.mouse.get_pos()

            if self.rect.collidepoint(position):
                if pygame.mouse.get_pressed()[0] == 1:
                    action = True

            screen.blit(self.image, (self.x, self.y))

            return action

    
    start_button = Buttons(WIDTH / 2 + 40, 150, START_IMAGE)
    stop_button = Buttons(WIDTH / 4, 150, STOP_IMAGE)

    x = 0
    y = 0
    new_x = 0
    new_y = 0

    play = True
    clock = pygame.time.Clock()


    def displayGame(score):
        min_score = 0
        score_array = []
        highscore_dict ={'highscore': score}
        
        file1 = open("highscore.txt", "a")  # append mode
        file1.write(score)
        file1.write("\n")

        f = open("highscore.txt", "r")
        for line in f.readlines():
            if int(min_score) < int(line):
                min_score = line
        
        print(min_score)
        
        SCORE = (0, 255, 0) #verde

        screen.fill(FILL_COLOR)
        GAMEOVER = pg.image.load('gameover.jpg').convert_alpha()
        image = pg.transform.scale(GAMEOVER, (240, 80))
        # screen.blit(image, (WIDTH/4, 150))
        screen.blit(image, image.get_rect(center = (WIDTH/2, HEIGTH/2)))
        
        font = pygame.font.Font(None, 24)

        text1 = font.render("YOUR SCORE: " + score, 1, SCORE)
        
        if int(min_score) < int(score):
            text = font.render("HIGHSCORE: " + score, 1, SCORE)
        else:
            text = font.render("HIGHSCORE: " + min_score, 1, SCORE)

        screen.blit(text1, text.get_rect(center = (WIDTH/2, 20)))
        screen.blit(text, text.get_rect(center = (WIDTH/2, 60)))

        # screen.blit(text1, (140, 10))
        # screen.blit(text, (140, 30))

        

        pg.display.update()
        time.sleep(3)



    # functionalitate joc
    class RunGame():
        def __init__(self, x, y, new_x, new_y):
            self.x = x
            self.y = y
            self.new_x = new_x
            self.new_y = new_y

        def gamePlay(self, run):
            heigth = 20
            length = 20
            TIMER = 5
            x_width = 200
            y_heigth = 200
            length_of_snake = 1
            increase = 0
            snake_list = [(self.x, self.y)] 
            obstacle_list = []
            prevKey = "name"
            SCORE = (0, 255, 0) #verde
            number_prevKey = 1
            with open('size.json', 'r') as fcc_file:
                data = json.load(fcc_file)
    
            OBSTACLE_1 = data['FIRST_OBSTACLE'] 
            OBSTACLE_2 = data['SECOND_OBSTACLE'] 
            
            OBSTACLE_1[0] = OBSTACLE_1[0] * 20 
            OBSTACLE_1[1] = OBSTACLE_1[1] * 20 
            OBSTACLE_2[0] = OBSTACLE_2[0] * 20
            OBSTACLE_2[1] = OBSTACLE_2[1] * 20

            obstacle_list.append((OBSTACLE_1[0], OBSTACLE_1[1]))
            obstacle_list.append((OBSTACLE_2[0], OBSTACLE_2[1]))

            while run:
                pg.font.init()
                
                font = pygame.font.Font(None, 24)
                text = font.render("SCORE: " + str(length_of_snake), 1, SCORE)
                screen.blit(text, text.get_rect(center = (WIDTH/2, 10)) )
                
                pg.display.update()

                for decision in pg.event.get():
                    if decision.type == pg.QUIT:
                        print("GoodBye")
                        exitButton = False
                        quit()

                    if decision.type == pg.KEYDOWN:
                        if decision.key == pg.K_LEFT:
                            if prevKey != "right":
                                self.new_x -= 20
                                self.new_y = 0
                                prevKey = "left"
                                
                        elif decision.key == pg.K_RIGHT:
                            if prevKey != "left":
                                self.new_x += 20
                                self.new_y = 0
                                prevKey = "right"
                                
                        elif decision.key == pg.K_UP:
                            if prevKey != "down":
                                self.new_x = 0
                                self.new_y -= 20
                                prevKey = "up"
                                
                        elif decision.key == pg.K_DOWN:
                            if prevKey != "up":
                                self.new_x = 0
                                self.new_y += 20
                                prevKey = "down"

                self.x += self.new_x
                self.y += self.new_y
                
                print(snake_list, (x_width, y_heigth))
                
                if (self.x, self.y) in snake_list and length_of_snake >= 2 or (self.x, self.y) in obstacle_list:
                    time.sleep(1)
                    displayGame(str(length_of_snake))

                    run = False
                    return run

                snake_list.append((self.x, self.y))
                
                if self.x == x_width and self.y == y_heigth:
                    ok = 0
                    while ok == 0:
                        x_width = random.randrange(0, WIDTH, +20)
                        y_heigth = random.randrange(0, HEIGTH, +20)
                        if (x_width, y_heigth) not in snake_list:
                            ok = 1
                    
                    length_of_snake += 1
                    increase += 1
                else:
                    del snake_list[0]
                
                screen.fill(FILL_COLOR)
                
                for (i, j) in snake_list:
                    pg.draw.rect(screen, SNAKE_COLOR, [i, j, heigth, length])

                pg.draw.rect(screen, FOOD_COLOR, [x_width, y_heigth, 20, 20])

                obs_1 = pg.draw.rect(screen, OBSTACLE_COLOR, [OBSTACLE_1[0], OBSTACLE_1[1], 20, 20])
                obs_2 = pg.draw.rect(screen, OBSTACLE_COLOR, [OBSTACLE_2[0], OBSTACLE_2[1], 20, 20])

                if length_of_snake % 5 == 0 and increase % 2 != 0: 
                    TIMER += 1
                    increase += 1 

                clock.tick(TIMER)

                pg.display.update()

                if self.x > WIDTH or self.x < 0 or self.y > HEIGTH or self.y < 0:
                    if self.x > WIDTH:
                        self.x = 0
                    if self.x < 0:
                        self.x += WIDTH + SIZE
                    if self.y > HEIGTH:
                        self.y = 0
                    if self.y < 0:
                        self.y += HEIGTH + SIZE   
                    # displayGame()

                    # run = False
                    # return run


    run = True

    while play:
        screen.fill(FILL_COLOR)
        initializeGame = RunGame(x, y, new_x, new_y)

        if start_button.draw() and initializeGame.gamePlay(run):
            initializeGame.gamePlay(run)

        elif start_button.draw() and not initializeGame.gamePlay(run):
            run = True
            initializeGame.gamePlay(run)

        if stop_button.draw():
            print("GoodBye!")
            play = False

        pg.display.update()

        for decisions in pg.event.get():
            if decisions.type == pg.QUIT:
                play = False

    # class Options:

game("size.json")