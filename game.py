import pygame, sys
import random

import math

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.slow = True
        self.Human_Playing = False
        self.point = False
        self.unpoint = False
        self.died = False
        self.save = False

        self.score1 = 0
        self.score2 = 0
        self.record = 0
        self.ball_x, self.ball_y = 300, 200
        self.ball_dx, self.ball_dy = random.choice([-4, 4]), random.choice([-4, 4])
        self.paddle1_y, self.paddle2_y = 150, 150
        # initialize Q table

    def run(self):
        while self.running:
            self.update_game_state(1)
            self.draw_game_objects()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
    def get_state(self):
        paddle_middle = self.paddle1_y + 50
        ball_middle = self.ball_y + 5
        y_diff = paddle_middle - ball_middle
        x_diff = round(self.ball_x+5 - 20,-2)//100
        sign = lambda x: (1, -1)[x<0]
        direction = sign(self.ball_dx)
        return [x_diff,y_diff,direction]
        
    def draw_game_objects(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, self.paddle1_y, 10, 100))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(590, self.paddle2_y, 10, 100))
        pygame.draw.circle(self.screen, (255, 255, 255), (int(self.ball_x), int(self.ball_y)), 10)
        pygame.draw.line(self.screen, (255, 255, 255), (300, 0), (300, 400))
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(str(self.score1) + " - " + str(self.score2), True, (255, 255, 255))
        self.screen.blit(score_text, (260, 10))
        pygame.display.flip()
        
    def add_score(self, team):
        if team == 1:
            self.score1 += 1
            if(self.score1 > self.record):
                self.record = self.score1
            self.point = True
        elif team == 2:
            self.score2 += 1
            self.unpoint = True
            
    def update_game_state(self, action):
        #actions
        if action == 0 and self.paddle1_y > 0: #move paddle up
            self.paddle1_y -= 2
        elif action == 2 and self.paddle1_y < 300:
            self.paddle1_y += 2

        #update ball position
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        #check for collisions
        if self.ball_y < 0 or self.ball_y > 390: # hit top or bottom
            self.ball_dy *= -1
        if self.ball_x < 20 and self.paddle1_y < self.ball_y < (self.paddle1_y + 100): # hit left paddle
            self.ball_dx *= -1
            self.ball_x = 21
            #self.add_score(1)
        elif self.ball_x > 580 and self.paddle2_y < self.ball_y < (self.paddle2_y + 100): # hit right paddle
            self.ball_dx *= -1
            self.ball_x = 580
            #self.add_score(2)
        elif self.ball_x < 0 or self.ball_x > 600: # hit right or left wall (reset game)
            if self.ball_x < 0:
                self.add_score(2)
            elif self.ball_x > 600:
                self.add_score(1)
            self.ball_x, self.ball_y = 300, 200
            self.ball_dx, self.ball_dy = random.choice([-4, 4]), random.choice([-4, 4])
            if self.score1 > 10 or self.score2 > 10:
                self.died = True
                self.score1, self.score2 = 0, 0

        #update super ai paddle positions
        if not self.Human_Playing and self.ball_y < self.paddle2_y + 50 and self.paddle2_y > 0:
            self.paddle2_y -= 3
        elif not self.Human_Playing and self.ball_y > self.paddle2_y + 50 and self.paddle2_y < 300:
            self.paddle2_y += 3
    
    def get_reward(self):
        if self.point:
            self.point = False
            return 1  # High positive reward for winning the game
        elif self.unpoint:
            self.unpoint = False
            return -1  # High negative reward for losing the game
        elif self.ball_x <= 20 and self.paddle1_y < self.ball_y < (self.paddle1_y + 100):
            return 0.5 # Positive reward for successfully hitting the ball with the paddle
        else:
            return 0
    
    def get_score(self):
        return self.score1 - self.score2
        
    def render(self):
        if not self.running: return
        if self.slow:
            self.clock.tick(60)
            self.draw_game_objects()
            pygame.display.update()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.slow = True
                    elif event.key == pygame.K_r:
                        self.slow = False
                    elif event.key == pygame.K_q:
                        self.Human_Playing = not self.Human_Playing
                    elif event.key == pygame.K_s:
                        if self.Human_Playing:
                            self.paddle2_y += 5
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        self.running = False
                    elif event.key == pygame.K_b:
                        self.save = True
        
        keys = pygame.key.get_pressed()
        if self.Human_Playing and keys[pygame.K_w]:
            self.paddle2_y -= 5
        elif self.Human_Playing and keys[pygame.K_s]:
            self.paddle2_y += 5