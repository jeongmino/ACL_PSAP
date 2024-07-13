import pygame
import sys

# 초기 설정
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PSAP Game')
font = pygame.font.Font(None, 36)

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 버튼 클래스
class StartButton:
    def __init__(self, text, pos, action):
        self.text = text
        self.pos = pos
        self.action = action
        self.rect = pygame.Rect(pos[0], pos[1], 150, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        # screen.blit(text_surf, (self.pos[0] + 10, self.pos[1] + 10))

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)


class ResponseButton:
    def __init__(self, text, pos, action):
        self.text = text
        self.pos = pos
        self.action = action
        self.rect = pygame.Rect(pos[0], pos[1], 150, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        ResponseFont = pygame.font.Font(None, 64)
        text_surf = ResponseFont.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        # screen.blit(text_surf, (self.pos[0] + 10, self.pos[1] + 10))

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)



# 게임 클래스
class PSAPGame:
    def __init__(self):
        self.points = 0
        self.FR = 0
        self.currentButton = ''
        self.pfi_active = False
        self.score_subtracted = False
        self.start_screen = True
        self.start_button = StartButton("Start", (325, 250), self.start_game)
        self.buttons = [
            ResponseButton("A", (200, 350), self.press_button_a),
            ResponseButton("B", (340, 350), self.press_button_b),
            ResponseButton("C", (480, 350), self.press_button_c)
        ]
        

    def start_game(self):
        self.start_screen = False
        self.update_screen()

    def update_screen(self):
        screen.fill(BLACK)
        if self.start_screen:
            # print("before")
            self.start_button.draw(screen)
            
        else:
            # print("after")
            if self.currentButton == 'A' and self.FR > 100:
                self.add_point()
            elif self.currentButton == 'B' and self.FR > 10:
                self.subtract_point()
            elif self.currentButton == 'C' and self.FR > 10:
                self.start_pfi()
                
            points_text = font.render(f"Points: {self.points}", True, WHITE)
            screen.blit(points_text, (350, 50))
            FR_ratio = f"FR: {self.FR}"
            if self.currentButton == 'A':
                FR_ratio = f"FR: {self.FR}/100"
            elif self.currentButton == 'B' or self.currentButton == 'C':
                FR_ratio = f"FR: {self.FR}/10"
            FR_text = font.render(FR_ratio, True, WHITE)
            screen.blit(FR_text, (350, 200))
            for button in self.buttons:
                button.draw(screen)

        pygame.display.flip()

    def press_button_a(self):
        if self.FR == 0:
            self.currentButton = 'A'
        self.FR += 1
        self.update_screen()

    def press_button_b(self):
        if self.FR == 0:
            self.currentButton = 'B'
        self.FR += 1
        self.update_screen()
        
    def press_button_c(self):
        if self.FR == 0:
            self.currentButton = 'C'
        self.FR += 1 
        self.update_screen()
        # if self.score_subtracted:
        #     self.start_pfi()
        # else:
        #     print("Cannot start PFI. No point has been subtracted yet.")

    def add_point(self):
        self.points += 1
        self.FR = 0
        
    def subtract_point(self):
        self.score_subtracted = True
        self.FR = 0

    def start_pfi(self):
        self.pfi_active = True
        self.score_subtracted = False
        self.FR = 0
        self.update_screen()

# 게임 루프
game = PSAPGame()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.start_screen:
                if game.start_button.is_clicked(event):
                    game.start_button.action()
            else:
                for button in game.buttons:
                    if button.is_clicked(event):
                        button.action()

    game.update_screen()

pygame.quit()
sys.exit()
