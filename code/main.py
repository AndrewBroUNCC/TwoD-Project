import sys
from settings import *
import pygame

class game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        #game state. example game over
        self.game_active = True

        #which way player is facing
        self.player_facing_right = True

        self.player_idle = True

        self.background_surface = pygame.image.load('graphics\cake.png').convert()
        
        # self.score_surf = self.test_font.render('Time Score: 0', False, (0,0,255)).convert()
        # #if you create rec here it will not grow bc it is outside of loop
        # self.score_rec = self.score_surf.get_rect(center = (640,50))

        self.bady_one_surface = pygame.image.load('graphics\Bady_01_flipped_resize.png').convert_alpha()
        self.bady_rec = self.bady_one_surface.get_rect(bottomleft = (1280,590))

        self.player_surface = pygame.image.load('graphics\Dude_Monster_Walk_100_107_01.png').convert_alpha()
        #590 is surface of ground
        self.player_rec = self.player_surface.get_rect(midbottom = (80,590))

        self.player_index = 0
        self.player_idle_index = 0
        self.time_index = 00.00

        self.player_gravity = 0
        self.start_time = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #another way to check for mouse collision using event.type
                # if event.type == pygame.MOUSEMOTION:
                #     if self.player_rec.collidepoint(event.pos):
                #         print('collision')

                if self.game_active:
                    #mousebutton jump while hovering player
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player_rec.collidepoint(event.pos) and self.player_rec.bottom == 590:
                                self.player_gravity = -25

                    #another way to check if space key is pressed
                    if event.type == pygame.KEYDOWN:
                        #print('key pressed down')
                        if event.key == pygame.K_SPACE and self.player_rec.bottom == 590:
                            self.player_gravity = -25             
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.player_idle = False
                            self.player_facing_right = True
                            #move player using rectangle
                        elif event.key == pygame.K_LEFT:
                            self.player_idle = False
                            self.player_facing_right = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:    
                            self.player_idle = True
                
                else:
                    #restart game
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_active = True
                            self.bady_rec.left = 1280
                            self.start_time = pygame.time.get_ticks()

                #check when that key is released
                # if event.type == pygame.KEYUP:
                #     print('key released')    

            # self.time_index += .025
            # self.time_index_adv = int(self.time_index)
            # self.score_surf = self.test_font.render('Time Score: '+str(self.time_index_adv), False, 'blue').convert()
            
            #create rectangle here and it grows
            #self.score_rec = self.score_surf.get_rect(center = (640,50))
            test_font = pygame.font.Font('googleFont\Silkscreen-Regular.ttf', 50)
    
            current_time = int((pygame.time.get_ticks() - self.start_time)/1000)
            self.score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
            self.score_rec = self.score_surf.get_rect(center = (640, 50))
            
            #has to be at bottom
            #self.screen.blit(self.score_surf, self.score_rec)

            #PLAYER
            #player gravity
            self.player_gravity += 1
            self.player_rec.y += self.player_gravity

            #setting the base or ground
            if self.player_rec.bottom >= 590:
                self.player_rec.bottom = 590

            if self.player_rec.left <= 0:
                self.player_rec.left = 0

            if self.player_rec.right >= 1280: self.player_rec.right = 1280    
            
            #moving through sprites
            self.player_index_adv = 0.0
            self.player_index_adv = self.player_index % 6
            self.player_index_adv = int(self.player_index_adv)
            self.player_index +=.15

            #moving through sprites
            self.player_idle_index_adv = 0.0
            self.player_idle_index_adv = self.player_idle_index % 4            
            self.player_idle_index_adv = int(self.player_idle_index_adv)
            self.player_idle_index +=.12

            if self.player_idle == False:
                if self.player_facing_right:
                    self.player_surface = pygame.image.load('graphics\Dude_Monster_Walk_100_107_0'+str(self.player_index_adv)+'.png').convert_alpha()
                    self.player_rec.left += 5
                else:
                    self.player_surface = pygame.image.load('graphics\Dude_Monster_Walk_100_107_0'+str(self.player_index_adv)+'.png').convert_alpha()
                    self.player_surface = pygame.transform.flip(self.player_surface, True, False)
                    self.player_rec.left -= 5
            else:
                if self.player_facing_right:
                    self.player_surface = pygame.image.load('graphics\Dude_Monster_Idle_0'+str(self.player_idle_index_adv)+'.png').convert_alpha()
                else:
                    self.player_surface = pygame.image.load('graphics\Dude_Monster_Idle_0'+str(self.player_idle_index_adv)+'.png').convert_alpha()
                    self.player_surface = pygame.transform.flip(self.player_surface, True, False)
            

            #can be done in event loop as well
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_SPACE]:
            #     print('jump')
            

            if self.game_active:
                #BACKGROUND
                self.screen.blit(self.background_surface,(0,0))

                # pygame.draw.rect(self.screen, 'pink', self.score_rec)
                # self.screen.blit(self.score_surf,self.score_rec)

                if self.bady_rec.right <= 0 :
                    self.bady_rec.left = 1280

                self.bady_rec.x -= 4
                self.screen.blit(self.bady_one_surface,self.bady_rec)
                self.screen.blit(self.player_surface,self.player_rec)
                self.screen.blit(self.score_surf, self.score_rec)

                #MONSTER COLLISION
                if self.bady_rec.colliderect(self.player_rec):
                    self.game_active = False

            else:
                self.screen.fill('yellow')    
                

            #check for collision
            # if self.player_rec.colliderect(self.bady_rec):
            #     print('Collision')

            #check for mouse collision
            # mouse_pos = pygame.mouse.get_pos()
            # if self.player_rec.collidepoint(mouse_pos):
            #     print('collision')

            #self.screen.fill('black')
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = game()
    game.run()