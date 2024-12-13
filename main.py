from asyncio import sleep
import pygame
import sys
import random
import math

class Game:
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

        # Var ZOMBIE 
        self.ZOMBIE_VELOCITY = 2
        self.ZOMBIE_SIZE_MULTIPLIER = 0.5
        self.ZOMBIE_ATTACK_DISTANCE = 75

        # Var BULLET
        self.BULLET_VELOCITY = 10
        self.BULLET_SIZE = 1
        self.BULLET_MAX_DISTANCE = 700

        #Var TIR
        self.shooting_cooldown = 1000
        self.last_shot_time = pygame.time.get_ticks()

        #Var XP
        self.XP_SIZE_MULTIPLIER = 4
        self.xp_orbs = []
        self.player_xp = 0



        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.run = True

        #Var scores etc
        self.start_time = pygame.time.get_ticks()
        self.kill_count = 0
        self.font = pygame.font.SysFont(None, 50)
        


        # Chargement du fond
        self.background_image = pygame.image.load('texture_map.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, self.BACKGROUND_TILESET_SIZE)

        # Chargement du joueur
        self.player_image = pygame.image.load('BiggerPlayerTest.png').convert()
        new_player_size = (self.player_image.get_width() * self.PLAYER_SIZE_MULTIPLIER, self.player_image.get_height() * self.PLAYER_SIZE_MULTIPLIER)
        self.player_image = pygame.transform.scale(self.player_image, new_player_size)
        self.player_image.set_colorkey((0, 0, 0))

        # Chargement du zombie
        self.zombie_image = pygame.image.load('zombieetsqueletton_01.png').convert()
        new_zombie_size = (self.zombie_image.get_width() * self.ZOMBIE_SIZE_MULTIPLIER, self.zombie_image.get_height() * self.ZOMBIE_SIZE_MULTIPLIER)
        self.zombie_image = pygame.transform.scale(self.zombie_image, new_zombie_size)
        self.zombie_image.set_colorkey((0, 0, 0))

        #Chargement de l'orbe XP
        self.xp_image = pygame.image.load('New Piskel (4).png').convert()
        new_xp_size = (self.xp_image.get_width() * self.XP_SIZE_MULTIPLIER, self.xp_image.get_height() * self.XP_SIZE_MULTIPLIER)
        self.xp_image = pygame.transform.scale(self.xp_image, new_xp_size)
        self.xp_image.set_colorkey((0, 0, 0))

        # Chargement des balles
        self.bullet_image = pygame.image.load('PlayerTest.bmp').convert()
        new_bullet_size = (self.bullet_image.get_width() * self.BULLET_SIZE, self.bullet_image.get_height() * self.BULLET_SIZE)
        self.bullet_image = pygame.transform.scale(self.bullet_image, new_bullet_size)
        self.bullet_image.set_colorkey((0, 0, 0))

        # Aplication du mouvement du joueur
        self.player = self.player_image.get_rect(topleft=(30, 30))  # Position initiale
        self.player_movement_x = [False, False]  # [Gauche, Droite]
        self.player_movement_y = [False, False]  # [Monter, Descendre]
        self.player_position = [0, 0]  # Position de départ

        # Variables pour la caméra
        self.camera_position = [0, 0]

        # Liste des zombies
        self.zombies = []

        # Liste des balles
        self.bullets = []

    def spawn_zombie(self):
        spawn_radius = 1000
        zombie_x = random.randint(self.player_position[0] - spawn_radius, self.player_position[0] + spawn_radius)
        zombie_y = random.randint(self.player_position[1] - spawn_radius, self.player_position[1] + spawn_radius)
        zombie_rect = self.zombie_image.get_rect(topleft=(zombie_x, zombie_y))
        self.zombies.append(zombie_rect)

    def move_zombies(self):
        # Déplace chaque zombie vers le joueur
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
                self.PLAYER_HP -= 1 
                break


    def shoot_bullet(self):
        # Trouve le zombie le plus proche
        if not self.zombies:
            return

        closest_zombie = min(self.zombies, key=lambda z: math.sqrt((z.x - self.player_position[0])**2 + (z.y - self.player_position[1])**2))
        dx = closest_zombie.x - self.player_position[0]
        dy = closest_zombie.y - self.player_position[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            dx /= distance  # Normalisation
            dy /= distance

        # Ajoute la balle
        bullet_rect = self.bullet_image.get_rect(center=(self.player_position[0], self.player_position[1]))
        self.bullets.append({'rect': bullet_rect, 'direction': (dx, dy)})

    def move_bullets(self):
        for bullet in self.bullets[:]:
            # Déplacement de la balle
            bullet['rect'].x += bullet['direction'][0] * self.BULLET_VELOCITY
            bullet['rect'].y += bullet['direction'][1] * self.BULLET_VELOCITY

            # Supprime les balles trop loin du joueur
            if math.sqrt((bullet['rect'].x - self.player_position[0])**2 + (bullet['rect'].y - self.player_position[1])**2) > self.BULLET_MAX_DISTANCE:
                #print("Balle supprimée car trop loin :", bullet['rect'])  # Debug optionnel
                self.bullets.remove(bullet)
                continue

        #A REPARER
            # Supprime les balles en dehors de l'écran
           # if bullet['rect'].x < -100 or bullet['rect'].x > self.BACKGROUND_MAP_SIZE + 100 or \
           # bullet['rect'].y < -100 or bullet['rect'].y > self.BACKGROUND_MAP_SIZE + 100:
            #    self.bullets.remove(bullet)
            #    continue

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

    # On affiche le HUD
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


    def END_GAME(self): # a refaire
        death_text = self.font.render(f"Tu es mort", True, (255, 255,255))
        self.screen.blit(death_text,(500,500))
        pygame.quit()
        sys.exit()
    
    def collect_xp_orbs(self):
        for orb in self.xp_orbs[:]:
            distance = math.sqrt(
                (orb['rect'].centerx - self.player_position[0]) ** 2 +
                (orb['rect'].centery - self.player_position[1]) ** 2
            )
            if distance < 50:
                self.player_xp += orb['value']
                self.xp_orbs.remove(orb) 

        
            


    def run_game(self):
        while self.run:
            self.screen.fill(self.BACKGROUND_COLOR)

            # Déplace le fond pour que le joueur soit toujours centré
            for y in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE):
                for x in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE):
                    self.screen.blit(self.background_image, (x - self.camera_position[0], y - self.camera_position[1]))

            # Mise à jour de la position du joueur
            self.player_position[0] += (self.player_movement_x[1] - self.player_movement_x[0]) * self.PLAYER_VELOCITY
            self.player_position[1] += (self.player_movement_y[1] - self.player_movement_y[0]) * self.PLAYER_VELOCITY

            # Déplace la caméra pour centrer le joueur
            self.camera_position[0] = self.player_position[0] + 250 - self.SCREEN_WIDTH // 2
            self.camera_position[1] = self.player_position[1] + 250 - self.SCREEN_HEIGHT // 2

            # Déplace les zombies et les balles
            self.move_zombies()
            self.move_bullets()
            self.collect_xp_orbs()


            # Dessine les zombies
            for zombie in self.zombies:
                self.screen.blit(self.zombie_image, (zombie.x - self.camera_position[0], zombie.y - self.camera_position[1]))

            # Dessine les balles
            for bullet in self.bullets:
                self.screen.blit(self.bullet_image, (bullet['rect'].x - self.camera_position[0], bullet['rect'].y - self.camera_position[1]))

            # Dessine le joueur en fonction de la caméra
            self.screen.blit(self.player_image, (self.player_position[0] - self.camera_position[0], self.player_position[1] - self.camera_position[1]))

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


            # Spawn de zombies à chaque itération
            if random.random() < 0.02:  # 2% de chance de spawn par frame
                self.spawn_zombie()
            
            # Dessine les orbes d'XP
            for orb in self.xp_orbs:
                self.screen.blit(self.xp_image, (orb['rect'].x - self.camera_position[0], orb['rect'].y - self.camera_position[1]))


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
