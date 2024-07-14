import pygame
import sys
import csv
import os
import time
from datetime import datetime

#전역변수로 각 Response의 할당량 설정
FR_A = 5
FR_B = 10
FR_C = 10

#로그 파일 설정
try:
    os.mkdir("LogFile")
except:
    pass
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log_file_name = "./LogFile/PSAP_Logfile_" + str(timestamp)
with open(log_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Response A", "Response B", "Response C", "Current Response"
                     ,"FR", "Total Point", "Timestamp"])


# 초기 설정
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PSAP Game')
font = pygame.font.Font(None, 36)



# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)

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
        self.active = True
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

    def set_active(self, active):
        self.active = active


# 게임 클래스
class PSAPGame:
    def __init__(self, log_file):
        self.points = 0
        self.FR = 0
        self.response_a = 0
        self.response_b = 0
        self.response_c = 0
        self.currentButton = 'None'
        self.log_file_name = log_file
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
            # if self.currentButton == 'A' and self.FR > 5:
            #     self.add_point()
            # elif self.currentButton == 'B' and self.FR > 10:
            #     self.subtract_point()
            # elif self.currentButton == 'C' and self.FR > 10:
            #     self.start_pfi()
            points_text = font.render(f"Points: {self.points}", True, WHITE)
            screen.blit(points_text, (350, 50))
            FR_ratio = f"FR: {self.FR}"
            if self.currentButton == 'A':
                FR_ratio = f"FR: {self.FR}/5"
            elif self.currentButton == 'B' or self.currentButton == 'C':
                FR_ratio = f"FR: {self.FR}/10"
            FR_text = font.render(FR_ratio, True, WHITE)
            screen.blit(FR_text, (350, 200))
            print("now: ", self.currentButton)
            if self.currentButton == "None":
                for button in self.buttons:
                    button.draw(screen)
                print("None")
            elif self.currentButton == "A":
                ResponseButton("A", (200, 350), self.press_button_a).draw(screen)
                print("A")
            elif self.currentButton == "B":
                ResponseButton("B", (340, 350), self.press_button_b).draw(screen)
                print("B")
            elif self.currentButton == "C":
                ResponseButton("C", (480, 350), self.press_button_c).draw(screen)
                print("C")

        pygame.display.flip()

    def log_event(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # 밀리세컨드까지 포함
        elapsed_time = int(time.perf_counter() * 1000)  # 밀리세컨드 단위 시간
        current_button = self.currentButton
        if self.FR == 0:
            current_button = "X"
        with open(log_file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.response_a, self.response_b, self.response_c, current_button, 
                             self.FR, self.points, timestamp])

    def press_button_a(self):
        if self.FR == 0:
            self.currentButton = 'A'
        if self.FR == FR_A:
            self.add_point()
            self.response_a += 1
        elif self.currentButton == 'A':
            self.FR += 1
            self.response_a += 1
        self.log_event()
        print("current button: ", self.currentButton)
        self.update_screen()

    def press_button_b(self):
        if self.FR == 0:
            self.currentButton = 'B'
        if self.FR == FR_B:
            self.subtract_point()
            self.response_b += 1
        elif self.currentButton == 'B':
            self.FR += 1
            self.response_b += 1
        self.log_event()
        self.update_screen()
        
    def press_button_c(self):
        if self.FR == 0:
            self.currentButton = 'C'
        if self.FR == FR_C:
            self.start_pfi()
            self.response_c += 1    
        elif self.currentButton == 'C':
            self.FR += 1
            self.response_c += 1    
        self.log_event()
        self.update_screen()
        # if self.score_subtracted:
        #     self.start_pfi()
        # else:
        #     print("Cannot start PFI. No point has been subtracted yet.")

    def add_point(self):
        self.points += 1
        self.FR = 0
        self.currentButton = "None"
        
    def subtract_point(self):
        self.score_subtracted = True
        self.FR = 0
        self.currentButton = "None"
        
    def start_pfi(self):
        self.pfi_active = True
        self.score_subtracted = False
        self.FR = 0
        self.currentButton = "None"

    def enable_button(self):
        for button in self.buttons:
            button.set_active(True)


# 게임 루프
game = PSAPGame(log_file_name)
running = True
cnt = 0;
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
    if cnt == 0:
        game.update_screen()
    cnt += 1
    

pygame.quit()
sys.exit()
