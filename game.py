import os
os.system('cls')

import pygame
import random
from pygame import mixer

mixer.init()
pygame.font.init()
pygame.init()  
base_path=os.path.dirname(__file__)
print(base_path)

screen=pygame.display.set_mode((1000,600))
pygame.display.set_caption('Z FIGHTERS')

g_font=pygame.font.SysFont("comicsans",30,bold=True)
bg_path=(base_path+"/game images/battlebg.png")
print(bg_path)
bg_image=pygame.image.load(bg_path)
scaled_bg=pygame.transform.scale(bg_image,(1000,600))

bg_entrypath=(base_path+"/game images/bgimag.webp")
bg_entry=pygame.image.load(bg_entrypath)
scaled_bg_entry=pygame.transform.scale(bg_entry,(1000,600))

def main():
    class Fighter():
        COOLDOWN=30
        def __init__(self,x,y,sound_fx,health=100):
            self.x=x
            self.y=y
            self.health=health
            self.max_health=100
            self.attacking=False
            self.attack_type=0
            self.cool_down_counter=0
            self.score=0
            self.sound=sound_fx

            goku_path=(base_path+"/game images/gifwarrior.png")
            self.goku=pygame.image.load(goku_path)
            self.gif=self.load_images()
            self.frameindex=0
            self.counter=0
            self.beams=[]
            beam_path=(base_path+"/game images/energyball2.png")
            self.beamimg=pygame.image.load(beam_path)
            self.beam=pygame.transform.scale(self.beamimg,(70,70))
            self.mask = pygame.mask.from_surface(self.beam)
            self.image=self.gif[self.frameindex]
            self.mask = pygame.mask.from_surface(self.image)
            self.update_time=pygame.time.get_ticks()

        def get_height(self):
            return self.goku.get_height()

        def get_width(self):
            return self.goku.get_width()

        def move(self):
            speed=8
            dy=0
            dx=0
            #key pressed
            key=pygame.key.get_pressed()
            if self.attacking==False:
                #movement
                if key[pygame.K_w]:
                    dy=-speed
                if key[pygame.K_s]:
                    dy=speed

            if self.y + dy < 0:
                dy=-self.y
            if self.y+self.get_height()+dy>600:
                dy=600-self.get_height()-self.y
            self.y+=dy
    
            if key[pygame.K_SPACE]:
                self.attacking=True

        def cooldown(self):
            if self.cool_down_counter >= self.COOLDOWN:
                self.cool_down_counter = 0
            elif self.cool_down_counter > 0:
                self.cool_down_counter += 1

        def shoot(self):
            if self.cool_down_counter == 0:
                beam = Beam(self.x, self.y)
                self.beams.append(beam)
                self.cool_down_counter = 1

        def healthbar(self,surface):
            pygame.draw.rect(surface, (255,0,0), (self.x+10, self.y+10,10 ,self.image.get_height()-50))
            pygame.draw.rect(surface, (255,255,0), (self.x+10, self.y+10 ,10, (self.image.get_height() -50)* (self.health/self.max_health)))


        def move_beam(self, vel, objs):
            if self.counter==1:
                self.cooldown()
                for beam in self.beams:
                    beam.move(vel)
                    if beam.off_screen(1000):
                        self.beams.remove(beam)
                    else:
                        for obj in objs:
                            if beam.collision(obj):
                                self.score+=1
                                self.sound.play()
                                objs.remove(obj)
                                if beam in self.beams:
                                    self.beams.remove(beam)


        def load_images(self):
            temp_img_list=[]
            for x in range(0,5):
                temp_img=self.goku.subsurface(x*115,0,115,142)
                temp_img_list.append(pygame.transform.scale(temp_img,(115,142)))
            return temp_img_list
            
        def draw(self,surface): 
            self.healthbar(surface)
            if self.attacking==False:
                surface.blit(self.gif[0],(self.x,self.y))
            else:
                animation_cooldown = 150
                self.image = self.gif[self.frameindex]
                surface.blit(self.image,(self.x,self.y))
                if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                    self.frameindex += 1
                    self.update_time = pygame.time.get_ticks()
                if self.frameindex > len(self.gif)-1:
                    self.frameindex=0            
                if self.frameindex==len(self.gif)-1:
                    self.counter=1
                    self.shoot()
                self.attacking=False    
                surface.blit(self.image,(self.x,self.y))
           
            for beam in self.beams:
                beam.draw(surface)

    class Enemy:
        def __init__(self, x, y):
            self.x=x
            self.y=y
            enemy_path=(base_path+"/game images/fire.png")
            self.enemyimg=pygame.image.load(enemy_path)
            self.enimg=pygame.transform.scale(self.enemyimg,(70,70))
            self.mask = pygame.mask.from_surface(self.enimg)
        def move(self,vel):
            self.x-=vel
        def get_height(self):
            return self.enimg.get_height()

        def draw(self,surface):
            surface.blit(self.enimg,(self.x,self.y))

    class Villain(Fighter):
        def __init__(self, x, y):
            self.rect=pygame.Rect((x,y,60,140))
            villain_path=(base_path+"/game images/frieza-removebg-preview.png")
            self.villain=pygame.image.load(villain_path)
            self.scaled_villain=pygame.transform.scale(self.villain,(280,200))

        def draw(self,surface):
            surface.blit(self.scaled_villain,(self.rect.x,self.rect.y))

    class Beam:
        def __init__(self, x, y):
            self.x=x
            self.y=y
            beam_path=(base_path+"/game images/energyball2.png")
            self.beamimg=pygame.image.load(beam_path)
            self.beam=pygame.transform.scale(self.beamimg,(70,70))
            self.mask = pygame.mask.from_surface(self.beam)

        def draw(self, surface):
            surface.blit(self.beam, (self.x+75, self.y+20))

        def move(self, vel):
            self.x += vel

        def off_screen(self, height):
            return not(self.x <= height-100 and self.x >= 0)

        def collision(self, obj):
            offset_x=obj.x - self.x -75
            offset_y=obj.y - self.y -20
            return self.mask.overlap(obj.mask, (offset_x, offset_y)) != None
        

    def collide(obj1,obj2):
        offset_x=obj2.x - obj1.x 
        offset_y=obj2.y - obj1.y 
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    mixer.music.load(base_path+"/game images/bg song.mp3")
    mixer.music.set_volume(0.4)
    mixer.music.play(-1)

    clock=pygame.time.Clock()
    collision_fx=pygame.mixer.Sound(base_path+"\game images\goku-ultra-instinct-ultra-instinct-autonomous-attack-sound-effect.mp3")
    wave=0
    FPS=60
    enemies=[]
    wave_length=2
    enemy_vel=1.5
    fighter_vel=2.0
    health=100
    fighter=Fighter(0,300,collision_fx)
    run = True
    lost=False
    villain=Villain(800,200)
   
    def draw_bg():

        screen.blit(scaled_bg,(0,0))
        wave_label=g_font.render(f"wave:{wave}",1,(0,0,0))
        score_label=g_font.render(f"score:{fighter.score}",1,(0,0,0))
        wave_label=g_font.render(f"wave:{wave}",1,(0,0,0))
        health_label=g_font.render(f"health:{health}",1,(0,0,0))
 
        screen.blit(wave_label,(450,10))
        screen.blit(score_label,(850,10))
        screen.blit(health_label,(10,10))

        lost_font = pygame.font.SysFont("comicsans", 50)
        score_font=pygame.font.SysFont("comicsans", 50)
        continue_font=pygame.font.SysFont("comicsans", 50)

        if lost:
            screen.blit(scaled_bg_entry,(0,0))
            lost_label = lost_font.render("You Lost!!", 1, (0,0,0),(255,255,255))
            screen.blit(lost_label, (500 - lost_label.get_width()/2, 170))

            score_label = score_font.render(f"score={fighter.score}", 1, (0,0,0),(255,255,255))
            screen.blit(score_label, (500 - score_label.get_width()/2, 270))

            continue_label = continue_font.render("....press mouse button to continue....", 1, (0,0,0),(255,255,255))
            screen.blit(continue_label, (500 - continue_label.get_width()/2,370))
            run = False

            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    main_menu()
                if event.type==pygame.QUIT:
                    run=False
                    quit()
            

        else:
            fighter.move()
            fighter.draw(screen)
            villain.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)

        pygame.display.update()
    while run:
        clock.tick(FPS)
        draw_bg()

        if fighter.health <= 0:
                lost = True

        if len(enemies)==0:
            wave+=1
            enemy_vel+=0.05
            fighter_vel+=0.08
            wave_length+=3
            for i in range(wave_length):
                enemy = Enemy(random.randrange(1100,2200,50), random.randrange(50,500,50))
                enemies.append(enemy)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if collide(enemy, fighter):
                fighter.health -= 10
                health-=10
                enemies.remove(enemy)
            elif enemy.x + enemy.get_height() < 0:
                fighter.health-=10
                health-=10
                enemies.remove(enemy)

        fighter.move_beam(fighter_vel,enemies)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                quit()

def main_menu():
    title_font=pygame.font.SysFont("comicscans",70)
    instruction_font=pygame.font.SysFont("comicscans",40)
    mixer.music.load(base_path+"\game images\game opening.mp3")
    mixer.music.set_volume(1.0)
    mixer.music.play(-1)
    run=True
    while run:
        screen.blit(scaled_bg_entry,(0,0))
        title_label=title_font.render("...press the mouse button to begin...",1,(0,0,0),(255,255,255))
        screen.blit(title_label, (500 - title_label.get_width()/2, 200))
        l=['Rules And Instructions---','1. W -> Move Up','2. S -> Move Down','3. HOLD SPACE BAR -> Fire','4. Miss or Hit by the Blast deals Damage']
        for i in range(len(l)):
            instruction_label=instruction_font.render(l[i],1,(0,0,0),(0,255,0))
            screen.blit(instruction_label, (500 - instruction_label.get_width()/2, 300 + 30*i))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mixer.music.stop()
                main()
    pygame.quit()
main_menu()        

