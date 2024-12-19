from asyncio import sleep
import pygame # type: ignore
import sys
import random
import math

class Game:

    def load_and_resize_image(self, filepath, size_multiplier, colorkey=(0, 0, 0)):
            """
            Charge une image, redimensionne et applique un colorkey.
            :param filepath: Chemin vers l'image.
            :param size_multiplier: Multiplicateur pour redimensionner l'image.
            :param colorkey: Couleur à rendre transparente.
            :return:Image redim
            """
            image = pygame.image.load(filepath).convert()
            new_size = (int(image.get_width() * size_multiplier), int(image.get_height() * size_multiplier))
            image = pygame.transform.scale(image, new_size)
            image.set_colorkey(colorkey)
            return image
    
    def __init__(self):
        pygame.init()

        # Var ECRAN
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080

        # Var BACKGROUND
        self.BACKGROUND_SIZE = 1028
        self.BACKGROUND_TILESET_SIZE = (self.BACKGROUND_SIZE, self.BACKGROUND_SIZE)
        self.BACKGROUND_COLOR = (255, 0, 0)  # Rouge
        self.BACKGROUND_MAP_SIZE = self.BACKGROUND_SIZE * 10  # Taille de la map

        # Var PLAYER
        self.PLAYER_VELOCITY = 7
        self.PLAYER_SIZE_MULTIPLIER = 0.3
        self.PLAYER_HP = 10
        self.PLAYER_LVL = 0

        # Var ZOMBIE 
        self.ZOMBIE_VELOCITY = 2
        self.ZOMBIE_SIZE_MULTIPLIER = 0.5
        self.ZOMBIE_ATTACK_DISTANCE = 75
        self.ZOMBIE_SPAWNCHANCHE = 0.04

        # Var BULLET
        self.BULLET_VELOCITY = 10
        self.BULLET_SIZE = 1
        self.BULLET_MAX_DISTANCE = 500
        self.bullet_number = 1

        #Var TIR
        self.shooting_cooldown = 1000
        self.last_shot_time = pygame.time.get_ticks()

        #Var XP
        self.XP_SIZE_MULTIPLIER = 4
        self.xp_orbs = []
        self.player_xp = 0
        self.last_ten_lvl = 10

        #Var LEVEL_UP_SCREEN
        self.LEVEL_UP = False
        self.CHOOSE_SIZE_MULTIPLIER = 1


        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.run = True

        #Var scores etc
        self.start_time = pygame.time.get_ticks()
        self.kill_count = 0
        self.font = pygame.font.SysFont(None, 50)
        
        #Var Gun
        self.GUN_SIZE_MULTIPLIER = 4


        # Chargement du fond
        self.background_image = pygame.image.load('src/image/sprite/p').convert()
        self.background_image = pygame.transform.scale(self.background_image, self.BACKGROUND_TILESET_SIZE)
     
        # Chargement du joueur
        self.player_image = self.load_and_resize_image('src/images/sprite/player/BiggerPlayerTest.png', self.PLAYER_SIZE_MULTIPLIER)

        # Chargement du zombie
        self.zombie_image = self.load_and_resize_image('src/images/sprite/zombie/zombie1/zombie1.png', self.ZOMBIE_SIZE_MULTIPLIER)
        
        # Chargement xp_screen
        self.lvl_up_image = self.load_and_resize_image('choose_background.png', self.CHOOSE_SIZE_MULTIPLIER)

        # Chargement de XP
        self.xp_image = self.load_and_resize_image('src/images/sprite/missellaneous/xp.png', self.XP_SIZE_MULTIPLIER)

        # Chargement des balles
        self.bullet_image = self.load_and_resize_image('src/images/sprite/player/player', self.BULLET_SIZE)


        # Aplication du mouvement du joueur
        self.player = self.player_image.get_rect(center=(0, 0))  # Position initiale
        self.player_movement_x = [False, False]  # [Gauche, Droite]
        self.player_movement_y = [False, False]  # [Monter, Descendre]
        self.player_position = [0, 0]  # Position de départ
        self.gun_position = [0, 0]

        # Variables pour la caméra
        self.camera_position = [0, 0]

        # Liste des zombies
        self.zombies = []

        # Liste des balles
        self.bullets = []

        self.PLAYER_VELOCITY = 200
        self.smooth_time = 0.5
        self.player_velocity_x = 0  
        self.player_velocity_y = 0 
        self.delta_time = 1 / 60 

    def spawn_zombie(self):
        spawn_radius = 2000
        min_distance = 1000

        while True:
            zombie_x = random.randint(int(self.player_position[0] - spawn_radius), int(self.player_position[0] + spawn_radius))
            zombie_y = random.randint(int(self.player_position[1] - spawn_radius), int(self.player_position[1] + spawn_radius))

            distance_squared = (zombie_x - self.player_position[0])**2 + (zombie_y - self.player_position[1])**2

            if distance_squared >= min_distance**2:
                break

        zombie_rect = self.zombie_image.get_rect(center=(zombie_x, zombie_y))
        self.zombies.append(zombie_rect)

    def move_zombies(self):
        # Déplace chaque zombie vers le joueur"
        for zombie in self.zombies:
            zombie_dx = self.player_position[0] - zombie.x
            zombie_dy = self.player_position[1] - zombie.y
            distance = math.sqrt(zombie_dx**2 + zombie_dy**2)

            if distance != 0:
                zombie_dx /= distance  # Normalisation
                zombie_dy /= distance  # Normalisation

            zombie.x += zombie_dx * self.ZOMBIE_VELOCITY
            zombie.y += zombie_dy * self.ZOMBIE_VELOCITY

            # Collision avec le joueur -> Dégats
            if distance <= self.ZOMBIE_ATTACK_DISTANCE:
                self.zombies.remove(zombie)  
                self.screen.fill((255, 0, 0))
                self.PLAYER_HP -= 1 
                break

    def smooth_damp(self, current, target, current_velocity, smooth_time, delta_time):
        smooth_time = max(0.0001, smooth_time)  # Évite la division par zéro
        omega = 2.0 / smooth_time
        x = omega * delta_time
        exp = 1 / (1 + x + 0.48 * x**2 + 0.235 * x**3)

        change = current - target
        temp = (current_velocity + omega * change) * delta_time
        new_velocity = (current_velocity - omega * temp) * exp
        new_position = target + (change + temp) * exp

        return new_position, new_velocity

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def shoot_bullet(self):
        if not self.zombies:
            return

        closest_zombie = min(self.zombies, key=lambda z: (z.x - self.player_position[0])**2 + (z.y - self.player_position[1])**2)

        dx = closest_zombie.x - self.player_position[0]
        dy = closest_zombie.y - self.player_position[1]
        distance = math.sqrt(dx**2 + dy**2)

        #Angle du gun arcos(dy/dx)
        self.gun_image = rot_center(self.gun_image, math.degrees(round(math.atan(dy/dx),1)))

        if distance != 0:
            dx /= distance
            dy /= distance

        for i in range(self.bullet_number):
            offset_x = 30 + (10 * i)
            offset_y = 30 + (10 * i)
            bullet_rect = self.bullet_image.get_rect(
                center=(self.player_position[0] + offset_x, self.player_position[1] + offset_y)
            )
            self.bullets.append({'rect': bullet_rect, 'direction': (dx, dy)})

    def move_bullets(self):
        for bullet in self.bullets[:]:  # Création d'une copie de la liste
            # Déplacement de la balle
            bullet['rect'].x += bullet['direction'][0] * self.BULLET_VELOCITY
            bullet['rect'].y += bullet['direction'][1] * self.BULLET_VELOCITY

            # Supprime les balles trop loin du joueur
            distance_squared = (bullet['rect'].x - self.player_position[0])**2 + (bullet['rect'].y - self.player_position[1])**2
            if distance_squared > self.BULLET_MAX_DISTANCE**2:
                self.bullets.remove(bullet)
            
            # Vérifie si une balle touche un zombie
            for zombie in self.zombies:
                if bullet['rect'].colliderect(zombie):
                    self.zombies.remove(zombie)
                    self.bullets.remove(bullet)
                    self.kill_count += 1

                    # Spawn une orbe d'XP à la position du zombie
                    xp_orb_rect = self.xp_image.get_rect(center=zombie.center)
                    self.xp_orbs.append({'rect': xp_orb_rect, 'value': 10})  # Chaque orbe vaut 10 XP
                    break


    def display_hud(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
        self.screen.blit(timer_text, (20, 20))
        kill_text = self.font.render(f"Kills: {self.kill_count}", True, (255, 255, 255))
        self.screen.blit(kill_text, (20, 70))
        hp_text = self.font.render(f"HP: {self.PLAYER_HP}", True, (255, 255,255))
        self.screen.blit(hp_text,(20,120))
        xp_text = self.font.render(f"XP: {self.player_xp}", True, (255, 255, 255))
        self.screen.blit(xp_text, (20, 170))
        level_text = self.font.render(f"LVL: {self.PLAYER_LVL}", True, (255, 255, 255))
        self.screen.blit(level_text, (20, 220))

    def END_GAME(self): # a refaire
        self.screen.fill((0, 0, 0))
        text = self.font.render("Rip", True, (255, 0, 0))
        self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width(), self.SCREEN_HEIGHT // 2 - text.get_height()))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()
    
    def collect_xp_orbs(self):
            for orb in self.xp_orbs[:]:
                distance_squared = (orb['rect'].centerx - self.player_position[0])**2 + (orb['rect'].centery - self.player_position[1])**2
                
                if distance_squared < 100**2:  
                    self.player_xp += orb['value']
                    self.xp_orbs.remove(orb)

    def level_up(self, lvl):  
        self.PLAYER_LVL += 1
        self.shooting_cooldown = self.shooting_cooldown * 0.9 * lvl
        self.ZOMBIE_SPAWNCHANCHE = self.ZOMBIE_SPAWNCHANCHE * 1.2 * lvl
        if self.PLAYER_LVL >= self.last_ten_lvl:
            self.bullet_number += 1
            self.last_ten_lvl += 10
        self.LEVEL_UP = True    
        #print(self.shooting_cooldown)

    def display_lvl_up_screen(self, lvl):
        self.screen.blit(self.lvl_up_image,(50, 50)) 
        pygame.time.wait(3000)


    def run_game(self):
        while self.run:
            self.screen.fill(self.BACKGROUND_COLOR)

            # Déplace le fond pour que le joueur soit toujours centré
            for y in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE):
                for x in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE):
                    self.screen.blit(self.background_image, (x - self.camera_position[0], y - self.camera_position[1]))

            if self.LEVEL_UP == True:
                self.display_lvl_up_screen(self.PLAYER_LVL)
                self.LEVEL_UP = False
                pass

            # Mise à jour de la position du joueur
            target_x = (self.player_movement_x[1] - self.player_movement_x[0]) * self.PLAYER_VELOCITY
            target_y = (self.player_movement_y[1] - self.player_movement_y[0]) * self.PLAYER_VELOCITY

            self.player_position[0], self.player_velocity_x = self.smooth_damp(
            self.player_position[0],
            self.player_position[0] + target_x,
            self.player_velocity_x,
            self.smooth_time,
            self.delta_time
            )

            self.player_position[1], self.player_velocity_y = self.smooth_damp(
                self.player_position[1],
                self.player_position[1] + target_y,
                self.player_velocity_y,
                self.smooth_time,
                self.delta_time
            )

            self.gun_position[0] = self.player_position[0]
            self.gun_position[1] = self.player_position[1]
            
            # Déplace la caméra pour centrer le joueur
            self.camera_position[0] = self.player_position[0] +200 -self.SCREEN_WIDTH // 2
            #print(self.player_position[1] -self.SCREEN_WIDTH // 2)
            self.camera_position[1] = self.player_position[1] +200 -self.SCREEN_HEIGHT // 2


            # Spawn de zombies à chaque itération
            if random.random() < self.ZOMBIE_SPAWNCHANCHE:  # 2% de chance de spawn par frame
                self.spawn_zombie()

            # Déplace les zombies et les balles
            self.move_zombies()
            self.move_bullets()
            self.collect_xp_orbs()

            # Dessine les orbes d'XP
            for orb in self.xp_orbs:
                self.screen.blit(self.xp_image, (orb['rect'].x - self.camera_position[0], orb['rect'].y - self.camera_position[1]))

            if self.player_xp >= 100:
                self.level_up(1)
                self.player_xp -= 100


            # Dessine les zombies
            for zombie in self.zombies:
                self.screen.blit(self.zombie_image, (zombie.x - self.camera_position[0], zombie.y - self.camera_position[1]))

            # Dessine les balles
            for bullet in self.bullets:
                self.screen.blit(self.bullet_image, (bullet['rect'].x - self.camera_position[0], bullet['rect'].y - self.camera_position[1]))

            # Dessine le joueur en fonction de la caméra
            self.screen.blit(self.player_image, (self.player_position[0] - self.camera_position[0], self.player_position[1] - self.camera_position[1]))
            self.screen.blit(self.gun_image, (self.gun_position[0] - self.camera_position[0] -50, self.gun_position[1] - self.camera_position[1]))
            print()


            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player_movement_y[0] = True
                    if event.key == pygame.K_DOWN:
                        self.player_movement_y[1] = True
                    if event.key == pygame.K_LEFT:
                        self.player_movement_x[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.player_movement_x[1] = True
                    #if event.key == pygame.K_SPACE:
                    #    self.shoot_bullet()             # Tir manuel

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.player_movement_y[0] = False
                    if event.key == pygame.K_DOWN:
                        self.player_movement_y[1] = False  
                    if event.key == pygame.K_LEFT:
                        self.player_movement_x[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.player_movement_x[1] = False

            # Tir automatique
            current_time = pygame.time.get_ticks() 
            if current_time - self.last_shot_time > self.shooting_cooldown:
                self.shoot_bullet()  
                self.last_shot_time = current_time  



            
           
            #Le hud
            self.display_hud()

            #Mort
            if self.PLAYER_HP == 0:
                self.END_GAME()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

Game().run_game()
