import pygame
import random
import sys

pygame.init()  #allows us acces to pygame functions

# Color + font library
colors = {0: (132,132,132),
          2: (227, 238, 189),
          4: (143, 188, 143),
          8: (173, 200, 47),
          16: (46, 139, 87),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (255, 215, 0),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),  #will be used for higher numbered tiles
          'dark text': (119, 110, 101),     #will be used for lower numbered tiles
          'other': (0, 0, 0),       # will be used for tile numbers > 2048
          'bg': (132,132,132)}    #bg color

BLACK = (100,0,0)
WHITE = (255, 255, 255)
HOVER = (163,85,73)
CLICK = (119, 16, 0)
TRANSPARENT_BLACK =(0,0,0,130)  #black color with half transparency
scores_font = pygame.font.SysFont('Papyrus', 25)
button_font = pygame.font.SysFont('Papyrus', 25)
game_over_font = pygame.font.SysFont('BloodOmen', 90)
# message_font = pygame.font.SysFont('')


# Initial setup :
WIDTH = 500
HEIGHT = 500
fps = 60
screen = pygame.display.set_mode([WIDTH, HEIGHT])  #500 x 600 screen
pygame.display.set_caption('2048')  #set caption
timer = pygame.time.Clock()  #speed of game
run = True

# game vars initialized:
board_values  = [[0 for x in range(4)] for x in range(4)]  #creates a 4x4 board, where all tiles have value 0 (empty)
game_over = False
spawn_new = True  #spawn new board when game starts
initial_count = 0 #initial number of tiles
direction = ''  #initially direction = 0
score = 0 #initial score
scores_file = open('high_score', 'r') #open file and read highscore
initial_highscore = int(scores_file.readline()) #read first highscore
scores_file.close()
high_score = initial_highscore
game_over_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
game_over_surface.fill(TRANSPARENT_BLACK)
game_over_text = game_over_font.render('GAME OVER', True, (162,0,0))
game_over_text_rect = game_over_text.get_rect(center=screen.get_rect().center)





# Spawnning new tiles randomly when turns start
def new_tiles(board):
    empty_count =0 #counts empty tiles
    board_full = False # initially board is empty
    while any(0 in row for row in board) and empty_count <1: #if theres 1 empty space on board (0 = empty tile)
        row = random.randint(0,3)  #generate random position for row
        column = random.randint(0,3)  #generate random position for column
        if board[row][column] == 0:  #if the random generated tile position is empty,
            empty_count +=1  #increase the number of empty tiles found
            if random.randint(1,10) == 10: #then theres a 1/10 chance to spawn value 4
                board[row][column] = 4
            else:
                board[row][column] =2       #else, spawn value 2

    if empty_count <1:     # if theres less than 1 empty tiles, then board is full
        board_full = True
    return board, board_full  #returns the board values, and wether the board is full or not

# draw game background
def draw_board():
    # draw game background
    # pygame.draw.rect(screen, colors['bg'], [0,100,500,500], 0,10) #select 'bg' color from color lib
    score_text  = scores_font.render(f'Score: {score}', True, BLACK) #
    high_score_text = scores_font.render(f'High Score: {high_score}', True, BLACK)
    screen.blit(score_text,(10, 0))#score position on screen
    screen.blit(high_score_text,(10, 40))
# draw tiles for game
def draw_tiles(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]  #value of tile = value of board at i,j
            if value> 8:
                value_color = colors['light text']  #higher numbered tiles will have lighter text, cz tiles are dark
            else:
                value_color = colors['dark text']  #lower numbered tiles will hv darker text, cz tiles are light
            if value <=2048 :
                tile_color = colors[value]  #then the tile color will depend on its value in dictionary
            else:
                tile_color = colors['other']  #other numbers will have tile bg as black
            #draw tile:
            pygame.draw.rect(screen, tile_color,
                             [j * 110 + 50,         i * 100 + 100,  # top left/top right corners. position + distance
                              80, 80], 0, 5)  # tile dimensions=80x80, roundness=5

            pygame.draw.rect(screen, 'white',                             [j * 110 + 50, i * 100 + 100,                                80,80], 2, 5)

            # pygame.draw.rect(screen, tile_color,
            #                  [j*110+50, i*100+160,#top left/top right corners. position + distance
            #                   80, 80]                              , 0, 5) #tile dimensions=80x80, roundness=5
            #tile border:
            # pygame.draw.rect(screen, 'white',                             [j * 110 + 50, i * 100 + 160,                                80,80], 2, 5)

            if value > 0:
                value_len = len(str(value))
                font =pygame.font.Font('freesansbold.ttf', 48-(5*value_len))  #decrease font size by 5 by every increase in value_len. so that big no's fit on tile
                value_text = font.render(str(value), True, value_color)  #convert value -> str as value's Text
                text_bounds = value_text.get_rect(center= (j*110 +90, i*100+140))  #set text in center of tile
                screen.blit(value_text, text_bounds)
    pass
# Take turn based on direction
def take_turn(direction, board):
    global score
    merged = [[False for x in range(4)] for x in range(4)]  #false cz nothing is merged yet
    if direction =='UP':
        # go thru every tile on board :
        for i in range(4):  #every row
            for j in range(4):  #every column
                shift = 0  #initially each tile moves by 0
                if i > 0:  #if its not top row (for rows 1, 2, 3):
                    for q in range(i):  #go thru every tile in that row
                        if board[q][j] == 0: #if those tiles are empty
                            shift += 1  #then shift tile by 1
                    if shift > 0:  #meaning if there are empty tiles (0) above my current tile
                        board[i-shift][j] = board[i][j]#then move the tile UP (-shift)
                        board[i][j]=0  #now the current tiles place is empty (0)
                    if board[i - shift - 1][j] == board[i-shift][j] \
                            and not merged[i-shift][j] \
                            and not merged[i-shift -1][j]: #check if tile collides with a same value tile above it
                        board[i-shift-1][j] *=2 #then double our current tile value
                        board[i-shift][j] = 0 #clear the previous value
                        score+= board[i-shift-1][j] #update the score based on current value
                        merged[i-shift-1][j] = True #the new double value tile is merged
    elif direction == 'DOWN':
        # go thru every tile on board :
        for i in range(3):  #every row (from last 2nd row)
            for j in range(4): # every column
                shift = 0
                for q in range(i+1):  #go thru every tile in that row
                        if board[3-q][j] == 0:  #check if tiles, staring from last 2nd tile from bottom are empty
                            shift+=1    #then shift tile by 1
                if shift > 0 : #if there are empty tiles below my current tile:
                        board[2-i  + shift][j] = board[2-i][j]  #then move tile DOWN (+ shift)
                        board[2-i][j] = 0 #now the current tile value becomes 0 (empty tile)
                if 3 - i + shift <= 3: #check if tiles are on board (<=3)
                        # if the tile we just moved into = right below my current tile
                        if board[2-i+shift][j] == board[3-i+shift][j] \
                            and not merged[3-i+shift][j] \
                            and not merged[2-i+shift][j]: #check if the tile collides with a same value tile BELOW it
                            board[3-i+shift][j] *=2 #then double our current tiles value
                            board[2-i+shift][j] = 0  #clear previous tile value
                            score += board[3-i+shift][j]    #update score based on current tile value
                            merged[3-i+shift][j] = True #merged = true
    elif direction == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):  #check every tile in every column
                    if board[i][q] == 0:#if the tile at [i][q] is empty
                        shift+=1    #shift tile by 1
                if shift > 0:   #if theres available tiles on the right
                        board[i][j-shift] = board[i][j] #move tile to LEFT (- shift)
                        board[i][j] = 0 #current tile value = 0
                if board[i][j-shift] == board[i][j-shift- 1] \
                        and not merged[i][j-shift-1]\
                        and not merged[i][j-shift]:  #check if tile collides with same value tile on LEFT
                        board[i][j-shift -1] *=2    #double current tile value
                        score += board[i][j - shift - 1]  # update score based on current tile value
                        board[i][j-shift] = 0   #previous tile value will become empty
                        merged[i][j-shift] = True #merged = true
    elif    direction== 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3-q] == 0:  #checks if tiles (starting from R > L) are empty
                        shift +=1
                if shift > 0:
                    board[i][3-j+shift] = board[i][3-j] #move tile to RIGHT (+ shift)
                    board[i][3-j] = 0   #current tile value will become empty
                if 4 - j + shift <=3:  #make sure collision stays within board bounds (<=3)
                    if board[i][4-j+shift] == board[i][3-j+shift]\
                        and not merged[i][4-j+shift]\
                        and not merged[i][3-j+shift]:  #if two tiles with same values collided but havent merged yet then
                        board[i][4-j+shift] *=2 #double current tile value
                        score += board[i][4-j+shift]    #update scores based on current tile value
                        board[i][3-j+shift] = 0 #previous tile value = empty
                        merged[i][4-j+shift] = True     #now merge the tiles
    return board # return new board values after movement
# check if any possible move is left, else game_over = true
def any_possible_moves(board):
    # Iterate over all the tiles on the board
    for i in range(4):
        for j in range(4):
            # Check if the tile is not zero
            if board[i][j] != 0:
                # Check if the tile can be merged with its adjacent tile (up, down, left, or right)
                if i > 0 and board[i][j] == board[i-1][j]: # Check up
                    return True
                if i < 3 and board[i][j] == board[i+1][j]: # Check down
                    return True
                if j > 0 and board[i][j] == board[i][j-1]: # Check left
                    return True
                if j < 3 and board[i][j] == board[i][j+1]: # Check right
                    return True
    # If none of the tiles can be merged, return False
    return False
#define button class :
class Button():
        def __init__(self, x, y, width, height, text = "Button", onclick_function = None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.onclick_function = onclick_function
            self.fill_colors = {'normal' : WHITE, 'hover' : HOVER, 'pressed' : CLICK}
            self.button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.button_text = button_font.render(text, True, BLACK)
            self.button_text_rect = self.button_text.get_rect(center = self.button_rect.center)

        def process_event(self, event):
            #change the button fill color based on mosue event
            mouse_pos = pygame.mouse.get_pos()  #get mouse position
            if self.button_rect.collidepoint(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_surface.fill(self.fill_colors['pressed'])
                else:
                    self.button_surface.fill(self.fill_colors['hover'])
                if event.type == pygame.MOUSEBUTTONUP:  #if butotn is clicked
                    if self.onclick_function:   #get onclick function
                        self.onclick_function()
            else:
                self.button_surface.fill(self.fill_colors['normal'])

        def render(self, screen):
            screen.blit(self.button_surface, self.button_rect)#blit the button surface onto the screen
            screen.blit(self.button_text, self.button_text_rect)    #blit the button text onto screen
def restart_game():
    global board_values
    global spawn_new
    global initial_count
    global score
    global direction
    global game_over

    board_values = [[0 for _ in range(4)] for _ in range(4)]  # reset board values to 0
    spawn_new = True  # spawn new board
    initial_count = 0  # initial tile count
    score = 0
    direction = ''
    game_over = False
    pygame.display.flip() #update the display after restarting
def exit_game():
    # pygame.quit()
    sys.exit()
    run = False  # stop running game
#define buttons :
restart_button = Button(130, 300, 250, 30, 'TRY AGAIN ?', restart_game)
leave_button = Button(150, 350, 200, 30, 'Leave', exit_game)

new_game_button = Button(300, 10, 200, 30,'New Game', restart_game)
new_game_button.button_surface.set_colorkey(WHITE) #makes all whites transparent
# new_game_button.button_text = button_font.render("New Game", True, CLICK) #change color
exit_button = Button(300, 50, 200, 30, 'Exit', exit_game)
exit_button.button_surface.set_colorkey(WHITE)  #makes all whites transparent



# Game loop =================================================================================================:
# run = True
while run: #while game is running :
    timer.tick(fps)  #start timer
    screen.fill((186, 186, 186))  #fill bg color
    draw_board()
    draw_tiles(board_values)  #draw tiles on board with values
    new_game_button.render(screen)
    exit_button.render(screen)


    # SPAWN :
    if spawn_new or initial_count <2:  #if a new tile is spawning, but tile count is <2, then spawn 2 tiles (in the starting)
        board_values, board_full= new_tiles(board_values)  #board value will update with each new spawn
        spawn_new = False
        initial_count +=1

    # MOVEMENT :
    if direction != '': #if key pressed, and direction changed
        board_values= take_turn(direction, board_values) #then board value will move
        direction = '' #update the board values
        spawn_new    = True # spawn new tile after we take a turn

    # GAME OVER SCREEN :
    if board_full and not any_possible_moves(board_values): #if board is full, and theres nO possible moves left
        game_over = True

    if game_over:  # save highscore when game over
        screen.blit(game_over_surface, (0, 0))  #blit the Game_Over surface
        screen.blit(game_over_text, game_over_text_rect)
        restart_button.render(screen)
        leave_button.render(screen)

        if high_score > initial_highscore:  # if new highScore > old highscore
                file = open('high_score', 'w')  # then update high_scores in file
                file.write(str(high_score))  # write new high score in file
                file.close()  # save file data
                initial_highscore = high_score  # now save new highscore as initial highscore when game starts again

    # EVENT HANDLING :
    for event in pygame.event.get():  #get the event happening
        new_game_button.process_event(event)    #new game button can now be pressed
        exit_button.process_event(event)
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):  #if we press quit X
            exit_game()
            run = False  #then stop running game

        if event.type == pygame.KEYUP: #when theres a key event
            if event.key == pygame.K_UP:    #press UP key
                direction= 'UP'
            elif event.key == pygame.K_DOWN:  # press DOWN key
                    direction = 'DOWN'
            elif event.key == pygame.K_LEFT:  # press LEFT key
                        direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:  # press RIGHT key
                            direction = 'RIGHT'

    # GAME OVER :
    if game_over:   #if board is full
        restart_button.process_event(event)
        leave_button.process_event(event)
        # pygame.display.flip() # is this needed or not ?

    if score > high_score:
        high_score = score  #update highscore

    pygame.display.flip()  #makes screen visible
pygame.quit()
