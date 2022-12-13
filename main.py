import random
import time

import pygame as pg
import pygame.mouse
import json
# crearea de display

def game(jsonFile):
    '''
    Folosind comanda with open(jsonFile, 'r') as fcc_file:
                            data = json.load(fcc_file)

    Initializam valorile oferite in fisierul size.json
    In acesta se vor gasi : lungimea panoului, inaltimea si pozitiile pe care dorim sa gasim obstacole
    
    Acestea vor fi extrase luand din variabila data valori de pe pozitia "WIDTH", "HEIGTH", "OBSTACLE_1", "OBSTACLE_2"
    '''
    with open(jsonFile, 'r') as fcc_file:
        data = json.load(fcc_file)
    
    print(data)
    WIDTH = int(data['WIDTH']) #latime 
    HEIGTH = int(data['HEIGTH']) #lungime
    
    SIZE = 20 #casuta

    FILL_COLOR = (1, 0, 35) 
    '''
    Definim in functia mama si culorile pentru sarpe, mancare si obstacol
    '''
    SNAKE_COLOR = (255, 255, 255) #alb
    FOOD_COLOR = (255, 0, 0) #rosie
    OBSTACLE_COLOR = (255,165,0) #portocaliu
    '''
    Setam dimensiunile spatiului de joc, oferim un titlu paginii
    '''
    screen = pg.display.set_mode((WIDTH, HEIGTH))

    pg.display.set_caption("Snake")

    '''
    Pentru a putea sa ne ajutam de butoane pentru a putea incepe jocul propriu-zis le vom incarca
    folosind functia pygame.image.load la care mai apoi le vom apela intr-o clasa in care formam butoanele
    care apar pe jocul nostru
    '''
    START_IMAGE = pg.image.load('start_button_low_di.png').convert_alpha()
    STOP_IMAGE = pg.image.load('stop_button.png').convert_alpha()
    '''
    Dupa fiecare implementare, vom pune in practica lucrurile noi care apar folosind pygame.display.update()
    '''
    pg.display.update()


    # creem o clasa oentru butoanele disponibile
    '''
    Aceasta clasa are ca scop implementarea butoanelor pe tabla noastra de joc, butoane care pot fi si apelate
    dand click pe ele. Pentru a putea face asta, initializam dimensiunile imaginii, punctele de coordonate unde
    dorim sa vedem imaginea si luam totodata dimensiunea totala in care apare butonul nostru, astfel cand jucatorul va da click
    pe una din punctele din imaginea de buton, acesta sa fie redirectionat corect in tabla de joc
    '''
    class Buttons:
        def __init__(self, x, y, image):
            self.image = pg.transform.scale(image, (100, 40))
            self.x = x
            self.y = y
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
        '''
        Trebuie sa luam si pozitia mouse-ului in care s-a dat click pentru a face apelul corect
        '''
        def draw(self):
            action = False

            position = pygame.mouse.get_pos()

            if self.rect.collidepoint(position):
                if pygame.mouse.get_pressed()[0] == 1:
                    action = True

            screen.blit(self.image, (self.x, self.y))

            return action

    '''
    Odata ce clasa de butoane a fost implementata, va trebui sa apelam clasa noastra cu parametrii declarati
    anterior 
    '''
    start_button = Buttons(WIDTH / 2 + 40, 150, START_IMAGE)
    stop_button = Buttons(WIDTH / 4, 150, STOP_IMAGE)

    '''
    Setam cooronatele de inceput pentru sarpele nostru, acestea vor fi actualizate pe parcurs in functie
    de comenzile care vor fi apelate
    '''
    x = 0
    y = 0
    new_x = 0
    new_y = 0

    '''
    Setam un timp de executie in care codul nostru sa functioneze odata ce a inceput jocul
    '''
    play = True
    clock = pygame.time.Clock()

    '''
    Pentru a putea finaliza jocul si a fi redirectionat pe o pagina de final, ne vom ajuta de functia
    displayGame(score), care va fi apelata cu lungimea sarpelui pana in punctul in care acesta a murit.
    In aceasta functie am apelat un fisier "highscore.txt" in care mereu voi insera noile lungimi in functie
    de meci. Dupa ce lungimea a fost apelata, aceasta va urma sa fie afisata pe pagina de "GAMEOVER" si va
    fi comparata cu cel mai mare scor din fisierul "highscore.txt". Am declarat o variabila nula, cu parametru
    0 care va fi comparata cu toate scorurile pana la momentul actual. Aceasta variabila "min_score"
    va primi cel mai mare scor care a fost inregistrat si-l va apela sub scorul jucatorului curent. 
    '''

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
    
    '''
    Dupa ce butonul de start a fost apelat, acesta va intra in clasa in care este dezvoltata inteligenta
    jocului. Jocul propriu-zis se bazeaza pe coordonate, astfel desenam un patrat de dimensiune 20 cu 20
    pe coordonatele x si y declarate initial cu 0, iar odata ce unul dintre butoanele de "sus","jos","stanga","dreapta"
    va fi apasat, coordonatele sarpelui vor fi modificate constant.
    '''
    # functionalitate joc
    class RunGame():

        '''
        Initializam coordonatele de care ne vom ajuta
        '''
        def __init__(self, x, y, new_x, new_y):
            self.x = x
            self.y = y
            self.new_x = new_x
            self.new_y = new_y
        '''
        Cand clasa de joc a fost apelata, vom intra in functia gamePlay unde care loc jocul propriu-zis
        iar cat timp variabila "run" va fi True, jocul va continue sa ruleze. Aceasta se va schimba in false
        atunci cand : capul sarpelui isi va atinge coada sa, sarpele va atinge unul dintre obstacole. 
        '''
        def gamePlay(self, run):
            heigth = 20
            length = 20
            TIMER = 5
            x_width = 200
            y_heigth = 200
            length_of_snake = 1
            increase = 0
            '''
            Initializam un array cu coordonatele de pe care sesiunea de joc va incepe.
            '''
            snake_list = [(self.x, self.y)] 
            obstacle_list = []
            prevKey = "name"
            SCORE = (0, 255, 0) #verde
            number_prevKey = 1
            with open('size.json', 'r') as fcc_file:
                data = json.load(fcc_file)
    
            OBSTACLE_1 = data['FIRST_OBSTACLE'] 
            OBSTACLE_2 = data['SECOND_OBSTACLE'] 
            '''
            Tabla noasta fiind formata din casute de 20 pe 20, la coordonatele oferite in json care sunt
            valori numerice formate din una valori mai mici sau egale cu radicalul inaltimii sau lungimii, 
            le vom inmulti cu 20 pentru a putea oferi zone corecte.
            Aceste obstacole le vom baga intr-o lista care mai ne va ajuta in verificarea daca sarpele atinge
            sau nu acele puncte de pe mapa. 
            '''
            OBSTACLE_1[0] = OBSTACLE_1[0] * 20 
            OBSTACLE_1[1] = OBSTACLE_1[1] * 20 
            OBSTACLE_2[0] = OBSTACLE_2[0] * 20
            OBSTACLE_2[1] = OBSTACLE_2[1] * 20

            obstacle_list.append((OBSTACLE_1[0], OBSTACLE_1[1]))
            obstacle_list.append((OBSTACLE_2[0], OBSTACLE_2[1]))
            '''
            Cat timp run este True, jocul continua. Vom pregati pe tabla noastra: Scorul, obstacolele, 
            mancarea si sarpele.
            '''
            while run:
                pg.font.init()
                
                font = pygame.font.Font(None, 24)
                text = font.render("SCORE: " + str(length_of_snake), 1, SCORE)
                screen.blit(text, text.get_rect(center = (WIDTH/2, 10)) )
                
                pg.display.update()
                '''
                Daca incheiem partida de joc fortat, jocul se va opri, iar daca apasam una din taste, jocul
                va incepe sa ruleze. Tinand cont ca ne intereseaza doar tastele de decizie sus, jos,
                stanga, dreapta, doar pe baza lor vom face anumite decizii si actualizari.
                '''
                for decision in pg.event.get():
                    if decision.type == pg.QUIT:
                        print("GoodBye")
                        exitButton = False
                        quit()

                    if decision.type == pg.KEYDOWN:
                        if decision.key == pg.K_LEFT:
                            if prevKey != "right":
                                '''
                                Daca apelam tasta stanga, vom salva intr-un parametru ca aceasta tasta
                                a fost apasata, iar pe parcursul jocului, daca vom apasa tasta opusa, aceasta
                                nu va functiona. Cand tasta a fost apasata, noi coordonate vor fi modificare 
                                care mai apoi li se vor transmite coordonatelor principale.
                                '''
                                self.new_x -= 20
                                self.new_y = 0
                                prevKey = "left"
                                
                        elif decision.key == pg.K_RIGHT:
                            if prevKey != "left":
                                '''
                                Daca apelam tasta dreapta, vom salva intr-un parametru ca aceasta tasta
                                a fost apasata, iar pe parcursul jocului, daca vom apasa tasta opusa, aceasta
                                nu va functiona. Cand tasta a fost apasata, noi coordonate vor fi modificare 
                                care mai apoi li se vor transmite coordonatelor principale.
                                '''
                                self.new_x += 20
                                self.new_y = 0
                                prevKey = "right"
                                
                        elif decision.key == pg.K_UP:
                            if prevKey != "down":
                                '''
                                Daca apelam tasta sus, vom salva intr-un parametru ca aceasta tasta
                                a fost apasata, iar pe parcursul jocului, daca vom apasa tasta opusa, aceasta
                                nu va functiona. Cand tasta a fost apasata, noi coordonate vor fi modificare 
                                care mai apoi li se vor transmite coordonatelor principale.
                                '''
                                self.new_x = 0
                                self.new_y -= 20
                                prevKey = "up"
                                
                        elif decision.key == pg.K_DOWN:
                            if prevKey != "up":
                                '''
                                Daca apelam tasta jos, vom salva intr-un parametru ca aceasta tasta
                                a fost apasata, iar pe parcursul jocului, daca vom apasa tasta opusa, aceasta
                                nu va functiona. Cand tasta a fost apasata, noi coordonate vor fi modificare 
                                care mai apoi li se vor transmite coordonatelor principale.
                                '''
                                self.new_x = 0
                                self.new_y += 20
                                prevKey = "down"
                
                '''
                In coordonatele mele principale vom adauga noile coordonate in functie de decizia care s-a
                luat. Daca tasta sus s-a apelat, atunci de pe modificam coordonatele decrementand coordonata de pe lungime, etc.
                '''
                self.x += self.new_x
                self.y += self.new_y
                '''
                Daca una din coordonatele in care sarpele meu se afla pe mapa(de la coada pana la cap) va 
                include inca odata o coordonata deja salvata, atunci inseamna ca sarpele s-a atins pe el
                insusi iar sesiunea de joc s-a incheiat. Sau, daca sarpele atinge coordonatele pe care sunt
                declarate obstacolele, sesiunea se va incheia. Pentru a putea vedea si actiunea care l-a facut
                pe jucator sa piarda, am apelat si un sleep de o secunda, ca mai apoi sa intre pe ecranul de finalizare.
                ''' 
                if (self.x, self.y) in snake_list and length_of_snake >= 2 or (self.x, self.y) in obstacle_list:
                    time.sleep(1)
                    displayGame(str(length_of_snake))

                    run = False
                    return run
                '''
                In lista mea de sarpe, voi face append cu noile coordonate ale sarpelui, iar pe vechile le voi sterge.
                '''
                snake_list.append((self.x, self.y))
                '''
                In caz ca acesta mananca, nu se vor sterge coordonate vechi, astfel incrementand lungimea
                sarpelui. Daca acesta nu mananca, nu are ce incrementa, astfel pozitia noua in care 
                se va deplasa se va salva, iar pozitia veche pe care a fost se va sterge.
                '''
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
                '''
                Pentru a putea crea sarpele, vom apela elementele de pe pozitia (i, j) din lista mea intreaga si
                vom crea patratele noi de fiecare data.
                '''
                for (i, j) in snake_list:
                    pg.draw.rect(screen, SNAKE_COLOR, [i, j, heigth, length])
                '''
                Creem si mancarea pe tabla noastra pe pozitiile x_width, y_heigth de marime 20 pe 20.
                '''
                pg.draw.rect(screen, FOOD_COLOR, [x_width, y_heigth, 20, 20])
                '''
                La fel ca mancarea, vom crea si obstacole
                '''
                obs_1 = pg.draw.rect(screen, OBSTACLE_COLOR, [OBSTACLE_1[0], OBSTACLE_1[1], 20, 20])
                obs_2 = pg.draw.rect(screen, OBSTACLE_COLOR, [OBSTACLE_2[0], OBSTACLE_2[1], 20, 20])
                '''
                Aceasta functie am facut-o pentru a face mai dificil jocul, astfel incat:
                daca sarpele o lungime din 10 in 10, timpul de executie va creste cu o unitate. Cu cat
                sarpele incrementeaza mai mult din 10 in 10 cu atat viteza jocului va fi mai mare. Increase
                va creste cu o unitate odata ce mananca de pe tabla, si va ramane par pana la urmatorul moment 
                in care sarpele mai atinge o lungime divizibila cu 10.
                '''
                if length_of_snake % 5 == 0 and increase % 2 != 0: 
                    TIMER += 1
                    increase += 1 

                clock.tick(TIMER)

                pg.display.update()
                '''
                Daca sarpele atinge maximul de pe tabla de joc, sau minimul, atunci acesta va ajunge la
                o valoare initiala sau finala. Mai exact, aceasta conditie este facuta pentru ca sarpele
                sa poata trece prin pereti. Daca sarpele merge pe latime, iar coordonatele sale trec sub valoare
                0, atunci vom restarta coordonatele pentru latime cu latimea declarata a table. Analog si pentru lungime
                '''
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
    '''
    Pentru a putea incepe jocul, am creat o conditie odata ce programul este rulat, facand un while pe play
    care este setat initial ca True. Vom face fill la tabla cu culoarea dorita, vom itializa parametrii 
    pentru joc si ii vom apela atunci cand butonul de start va fi executat. Am pus 2 conditii si pentru
    momentul in care jucatorul termina sesiunea de joc si vrea sa reia jocul de la inceput.
    '''
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
