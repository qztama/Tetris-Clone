import pygame, random, time
import piece
from copy import deepcopy

BLACK = (0,0,0)
WHITE = (255,255,255)

COLOR_CHOICES = [
                 (0,0,0),     #White
                 (175,20,20), #Light REd
                 (20,175,20), #Light Green
                 (20,20,175), #Light Blue
                 (175,175,20) #Light Yellow
                ]

DISP_TEMP_S = ((1.5,3),(2.5,2),(3.5,2),(2.5,3))
DISP_TEMP_Z = ((1.5,2),(2.5,2),(2.5,3),(3.5,3))
DISP_TEMP_I = ((2.5,1),(2.5,2),(2.5,3),(2.5,4))
DISP_TEMP_O = ((2,2),(3,2),(2,3),(3,3))
DISP_TEMP_J = ((2,3.5),(3,3.5),(3,1.5),(3,2.5))
DISP_TEMP_L = ((2,3.5),(3,3.5),(2,1.5),(2,2.5))
DISP_TEMP_T = ((1.5,3),(2.5,3),(3.5,3),(2.5,2))

DISP_SHAPES = [DISP_TEMP_S, DISP_TEMP_Z,DISP_TEMP_I,DISP_TEMP_O,
               DISP_TEMP_J, DISP_TEMP_L,DISP_TEMP_T]

DISP_TEMP_SIZE = 6

FPS = 25
BASE_FALL_TIME = 1000

class Game:
    def __init__(self, block_size, screen_width, screen_height, win_width, win_height, window):
        self.window = window
        self.block_size = block_size
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen_coord = (win_width/8, win_height-screen_height*block_size)
        self.clock = pygame.time.Clock()

        #moving variables
        self.left_key_held = False
        self.right_key_held = False
        self.down_key_held = False

        #time constraints in milliseconds
        self.time_between_fall = BASE_FALL_TIME
        self.time_between_move = 150

        #time tabbing
        self.last_fall_time = 0
        self.last_move_time = 0

        self.cur_piece = piece.Piece(random.randrange(1,len(COLOR_CHOICES),1))
        self.next_piece = piece.Piece(random.randrange(1,len(COLOR_CHOICES),1))

        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

        self.score = 0

        self.game_over = False

        self.hold_piece = None
        self.hold_used = False

        self.board = []

        for i in range(0,screen_height):
            self.board.append([0]*screen_width)

    def combine_piece_board(self):
        cur_board = deepcopy(self.board)
        coords = self.cur_piece.get_board_coord()

        for tuple in coords:
            if tuple[1] >= 0:
                cur_board[tuple[1]][tuple[0]] = self.cur_piece.color

        return cur_board
    
    def display_board(self, window):
        screen = pygame.Surface((self.screen_width * self.block_size,self.screen_height * self.block_size))
        screen.fill(BLACK)

        cur_board = self.combine_piece_board()

        for i in range(0, self.screen_width):
            for j in range(0, self.screen_height):
                if(cur_board[j][i] != 0):
                    pygame.draw.rect(screen, COLOR_CHOICES[ cur_board[j][i] ], (i*self.block_size, j*self.block_size,self.block_size, self.block_size), 0)
                    pygame.draw.rect(screen, BLACK, (i*self.block_size, j*self.block_size,self.block_size, self.block_size), 1)

        window.blit(screen,self.screen_coord)

    def display_hold_piece(self):
        np_block_size = 20
        hold_piece_screen = pygame.Surface((DISP_TEMP_SIZE*np_block_size, DISP_TEMP_SIZE*np_block_size))
        hold_piece_screen.fill(COLOR_CHOICES[0])

        pygame.draw.rect(hold_piece_screen, (255,255,255), (0,0, DISP_TEMP_SIZE*np_block_size, DISP_TEMP_SIZE*np_block_size), 1)

        if self.hold_piece:
            for tuple in DISP_SHAPES[self.hold_piece.shape]:
                pygame.draw.rect(hold_piece_screen, COLOR_CHOICES[self.hold_piece.get_color()],(tuple[0] * np_block_size, tuple[1] * np_block_size, np_block_size, np_block_size), 0)
                pygame.draw.rect(hold_piece_screen, BLACK, (tuple[0] * np_block_size, tuple[1] * np_block_size, np_block_size, np_block_size), 1)

        text_Surf, text_Rect = self.create_text_obj('Hold piece:', self.BASICFONT, (0,0,0))
        self.window.blit(text_Surf, (3/4*20*self.block_size, 5/8*23*self.block_size))
        self.window.blit(hold_piece_screen, (3/4*20*self.block_size, 5/8*23*self.block_size + text_Rect.size[1]))

    def display_next_piece(self):
        np_block_size = 20
        next_piece_screen = pygame.Surface((DISP_TEMP_SIZE*np_block_size, DISP_TEMP_SIZE*np_block_size))
        next_piece_screen.fill(COLOR_CHOICES[0])

        pygame.draw.rect(next_piece_screen, (255,255,255), (0,0, DISP_TEMP_SIZE*np_block_size, DISP_TEMP_SIZE*np_block_size), 1)

        for tuple in DISP_SHAPES[self.next_piece.shape]:
            pygame.draw.rect(next_piece_screen, COLOR_CHOICES[self.next_piece.get_color()],(tuple[0] * np_block_size, tuple[1] * np_block_size, np_block_size, np_block_size), 0)
            pygame.draw.rect(next_piece_screen, BLACK, (tuple[0] * np_block_size, tuple[1] * np_block_size, np_block_size, np_block_size), 1)

        text_Surf, text_Rect = self.create_text_obj('Next piece:', self.BASICFONT, (0,0,0))
        self.window.blit(text_Surf, (3/4*20*self.block_size, 1/8*23*self.block_size))
        self.window.blit(next_piece_screen, (3/4*20*self.block_size, 1/8*23*self.block_size + text_Rect.size[1]))

    def display_score(self):
        text_Surf, text_Rect = self.create_text_obj('Score:', self.BASICFONT, (0,0,0))
        self.window.blit(text_Surf, (3/4*20*self.block_size, 3/8*23*self.block_size))
        score_Surf, score_Rect = self.create_text_obj(str(self.score), self.BASICFONT, (0,0,0))
        self.window.blit(score_Surf, (3/4*20*self.block_size, 3/8*23*self.block_size+text_Rect.size[1]))

    def display_game_over(self):
        screen = pygame.Surface((self.screen_width * self.block_size,self.screen_height * self.block_size))
        screen.fill(BLACK)
        text_Surf, text_Rect = self.create_text_obj('Game Over', self.BASICFONT, WHITE)
        score_Surf, score_Rect = self.create_text_obj('Final Score: ' + str(self.score), self.BASICFONT, WHITE)
        instruct_Surf, instruct_Rect = self.create_text_obj('Press \'r\' to restart', self.BASICFONT, WHITE)

        text_x = screen.get_rect().centerx - text_Rect.centerx
        text_y = screen.get_rect().centery - text_Rect.centery

        screen.blit(text_Surf,(text_x, text_y))
        screen.blit(score_Surf, (text_x, text_y + text_Rect.height))
        screen.blit(instruct_Surf, (text_x, text_y + 2*text_Rect.height))
        self.window.blit(screen,self.screen_coord)

    def fall(self):
        self.cur_piece.coord[1]+=1

        #current piece has landed
        if not self.isValidConfig():
            self.cur_piece.coord[1]-=1

            self.piece_landed()

    def completed_line(self):
        num_of_completed_lines = 0
        erase_lines = []

        for i in range(0, self.screen_height):
            line_complete = True

            for j in range(0, self.screen_width):
                if(self.board[i][j] == 0):
                    line_complete = False
                    break


            if line_complete:
                num_of_completed_lines+=1
                erase_lines.append(i)

        self.score += num_of_completed_lines*50

        new_board = []

        starting_index = len(erase_lines)

        for i in range(0, starting_index):
            new_board.append([0]*self.screen_width)

        for k in range(0, self.screen_height):
            if k not in erase_lines:
                new_board.append(self.board[k])

        self.board = new_board

    def change_hold_piece(self):
        if not self.hold_used:
            self.hold_used = True

            if not self.hold_piece:
                self.hold_piece = self.cur_piece
                self.cur_piece = self.next_piece
                self.next_piece = piece.Piece(random.randrange(1,len(COLOR_CHOICES),1))
            else:
                #switch cur piece and hold piece
                temp = self.hold_piece
                self.hold_piece = self.cur_piece
                self.cur_piece = temp

            #reset the coordinates of hold piece
            self.hold_piece.reset_coord()

    def drop_piece(self):
        while self.isValidConfig():
            self.cur_piece.coord[1]+=1

        self.cur_piece.coord[1]-=1

        self.piece_landed()

    def isValidConfig(self):
        board_piece_coord = self.cur_piece.get_board_coord()

        for coord in board_piece_coord:
            #off the screen
            if coord[0] < 0 or coord[0] >= self.screen_width or coord[1] >= self.screen_height:
                return False
            if(coord[1] >= 0):
                #piece collides with stuff on the board
                if self.board[coord[1]][coord[0]] != 0:
                    return False

        return True

    def launch_new_piece(self):
        del self.cur_piece
        self.cur_piece = self.next_piece
        self.next_piece = piece.Piece(random.randrange(1,len(COLOR_CHOICES),1))

    def create_text_obj(self,text,font,color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def piece_landed(self):
        #reset the hold used
        self.hold_used = False

        board_piece_coord = self.cur_piece.get_board_coord()

        for coord in board_piece_coord:
            #checking for game over
            if coord[1] < 0:
                self.game_over = True
                return

            #updating the board
            self.board[coord[1]][coord[0]] = self.cur_piece.get_color()

        #check for lines completion
        self.completed_line()
        self.launch_new_piece()

    def rotate_piece(self, dir):
        self.cur_piece.rotate(dir)

        if not self.isValidConfig():
            self.cur_piece.rotate(-dir)

    def shift_piece(self, dir):
        self.cur_piece.shift(dir)

        if not self.isValidConfig():
            self.cur_piece.shift(-dir)

    def run_game(self):
        running = True

        while not self.game_over:
            #managing the key inputs
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.left_key_held = True
                    if event.key == pygame.K_RIGHT:
                        self.right_key_held = True
                    if event.key == pygame.K_DOWN:
                        self.down_key_held = True
                    if event.key == pygame.K_z:
                        self.rotate_piece(-1)
                    if event.key == pygame.K_x:
                        self.rotate_piece(1)
                    if event.key == pygame.K_SPACE:
                        self.drop_piece()
                    if event.key == pygame.K_c:
                        self.change_hold_piece()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.left_key_held = False
                    if event.key == pygame.K_RIGHT:
                        self.right_key_held = False
                    if event.key == pygame.K_DOWN:
                        self.down_key_held = False
                #closing the game
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            #updating the game state
            cur_time = pygame.time.get_ticks()

            if self.left_key_held == True and cur_time - self.last_move_time > self.time_between_move:
                self.last_move_time = cur_time
                self.shift_piece(-1)
            if self.right_key_held == True and cur_time - self.last_move_time > self.time_between_move:
                self.last_move_time = cur_time
                self.shift_piece(1)
            #speed up the drop with down arrow key
            if self.down_key_held == True:
                self.time_between_fall = BASE_FALL_TIME/10
            else:
                self.time_between_fall = BASE_FALL_TIME

            if cur_time - self.last_fall_time > self.time_between_fall:
                self.last_fall_time = cur_time
                self.fall()

            self.window.fill((150,150,150)) #clear screen
            self.display_board(self.window)
            self.display_next_piece()
            self.display_hold_piece()
            self.display_score()
            pygame.display.update()

            self.clock.tick(FPS)

        #display game over screen
        self.display_game_over()
        pygame.display.update()

        return True