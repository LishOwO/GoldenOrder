import pygame  # type: ignore
import sys
import random
import math

sys.path.append('./bin')

from objects import Objects     # type: ignore
from zombie import Zombie       # type: ignore
from player import Player       # type: ignore
from weapons import Weapons     # type: ignore
import tools                    # type: ignore



class Game:


    # initialisation
    def __init__(self):
        pygame.init()

        #pygame.mixer.set_num_channels(20) #Utile ?

        # Var ECRAN
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h

        # Var BACKGROUND
        self.BACKGROUND_SIZE = 1024
        self.BACKGROUND_TILESET_SIZE = (self.BACKGROUND_SIZE, self.BACKGROUND_SIZE)
        self.BACKGROUND_COLOR = (255, 0, 0)  # Rouge
        self.BACKGROUND_MAP_SIZE = self.BACKGROUND_SIZE * 10  # Taille de la map

        # Var PLAYER
        self.PLAYER_VELOCITY = 7
        self.PLAYER_SIZE_MULTIPLIER = 4
        self.player_health = 10
        self.player_lvl = 0
        self.PLAYER_DAMAGE_SOUNDS = [pygame.mixer.Sound("src/son/PlayerDamage1.mp3"),
                                    pygame.mixer.Sound("src/son/PlayerDamage2.mp3"),
                                    pygame.mixer.Sound("src/son/PlayerDamage3.mp3"),
                                    pygame.mixer.Sound("src/son/PlayerDamage4.mp3"), ]


        # Var ZOMBIE
        self.ZOMBIE_VELOCITY = 2
        self.ZOMBIE_SIZE_MULTIPLIER = 0.5
        self.ZOMBIE_ATTACK_DISTANCE = 75
        self.ZOMBIE_SPAWNCHANCHE = 0.03
        self.ZOMBIE_DAMAGE_SOUNDS = [pygame.mixer.Sound("src/son/ZombieDamage1.mp3"),
                                     pygame.mixer.Sound("src/son/ZombieDamage2.mp3"),
                                     pygame.mixer.Sound("src/son/ZombieDamage3.mp3"),
                                     pygame.mixer.Sound("src/son/ZombieDamage4.mp3"), ]

        # Son Powerups
        self.son_bombe = pygame.mixer.Sound("src/son/BombSound.mp3")
        self.son_soin = pygame.mixer.Sound("src/son/HealthBoost.mp3")


        # Var BULLET
        self.BULLET_VELOCITY = 20
        self.BULLET_SIZE = 2
        self.BULLET_MAX_DISTANCE = self.SCREEN_HEIGHT // 2
        self.bullet_number = 1

      
        # Var XP
        self.XP_SIZE_MULTIPLIER = 4
        self.xp_orbs = []
        self.player_xp = 0
        self.last_ten_lvl = 10

        # Var Potion Heal
        self.POT_SIZE_MULTIPLIER = 4
        self.health_potions = []

        # Var Bombe
        self.bombs = []
        self.BOMB_SIZE_MULTIPLIER = 4


        # Var LEVEL_UP_SCREEN
        self.LEVEL_UP = False
        self.CHOOSE_SIZE_MULTIPLIER = self.SCREEN_WIDTH / 1980

        # Var SCREEN
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        # Var MENU
        self.run = True
        self.menu = True
        self.menu_skin = False
        self.menu_weapon = False

        # Var scores etc
        self.start_time = pygame.time.get_ticks()
        self.kill_count = 0
        self.font = pygame.font.SysFont(None, 50)

        # Var BOX
        self.BOX_SPAWN_CHANCE = 0.005  # 1% de chance de spawn par frame
        self.boxes = []
        self.LOCAL_BOX_DISTANCE = 50000
        self.MAX_LOCAL_BOX = 4
        self.local_boxes = 0

        # Chargement du fond
        self.background_image = pygame.image.load('src/images/sprite/texture_map.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, self.BACKGROUND_TILESET_SIZE)

        # Chargement des skins du joueur
        self.lebron_image = self.load_and_resize_image('src/images/sprite/player/LebronJames.png',self.PLAYER_SIZE_MULTIPLIER)
        self.white_james_image = self.load_and_resize_image('src/images/sprite/player/WhiteJames.png',self.PLAYER_SIZE_MULTIPLIER)
        self.red_james_image = self.load_and_resize_image('src/images/sprite/player/RedJames.png',self.PLAYER_SIZE_MULTIPLIER)
        self.player_image = self.lebron_image #Image de Base
        self.original_player_image = self.player_image #Image pour le Flip


        #self.mec_alakippa_image = self.load_and_resize_image('src/images/sprite/player/MecAlakippa.png',0.75)

        
        #listes des skins
        self.skins = [self.lebron_image,self.white_james_image,self.red_james_image,self.lebron_image,self.white_james_image,self.red_james_image]

        # Chargement xp_screen
        self.lvl_up_image = self.load_and_resize_image('src/images/ui/lvl_up/lvl_up.png', self.CHOOSE_SIZE_MULTIPLIER)

        # Chargement de XP
        self.xp_image = self.load_and_resize_image('src/images/sprite/miscellaneous/xp.png', self.XP_SIZE_MULTIPLIER)

        self.health_image = self.load_and_resize_image('src/images/sprite/miscellaneous/health_potion.png', self.POT_SIZE_MULTIPLIER)

        self.bombe_image = self.load_and_resize_image('src/images/sprite/miscellaneous/bombe.png',self.BOMB_SIZE_MULTIPLIER)


        # Chargement des balles
        self.bullet_image = self.load_and_resize_image('src/images/sprite/weapons/Bullet2.png', self.BULLET_SIZE)
        self.rotated_bullet_image = self.load_and_resize_image('src/images/sprite/weapons/Bullet2.png',self.BULLET_SIZE)

        # Chargement du gun
        self.weapon_image = self.load_and_resize_image('src/images/sprite/weapons/AK47.png', 0.8)
        self.rotated_weapon_image = self.load_and_resize_image('src/images/sprite/weapons/AK47.png', 0.8)

        # Chargement des box
        self.luckyblock_image = self.load_and_resize_image('src/images/sprite/miscellaneous/LuckyBlock.png', 1)

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
        # Check si boss est spawn
        self.boss_state = False
        self.bosses_spawned = 0
        # Liste des balles
        self.bullets = []

        # Variables de mouvement du joueur
        self.PLAYER_VELOCITY = 200
        self.smooth_time = 0.5
        self.player_velocity_x = 0
        self.player_velocity_y = 0
        self.delta_time = 1 / 60

        # Variables lucky blocks
        self.lucky_blocks = []  # Liste des lucky blocks

        #Var Weapon M4        
        self.GUN_SIZE_MULTIPLIER = 4
        self.son_tir = pygame.mixer.Sound("src/son/PistolSound.mp3")
        self.shooting_cooldown = 700
        self.last_shot_time = pygame.time.get_ticks()

        #Var Weapon Laser
        self.laser_image = self.load_and_resize_image("src/images/sprite/weapons/NetherStar.jpeg", 0.2, (255,255,255))
        self.laser_length = 200  
        self.laser_color = (255, 0, 0)  
        self.laser_speed = 1  
        self.laser_angle = 0  

        #Var Weapon Pistolet
        self.pistolet_image = self.load_and_resize_image("src/images/sprite/weapons/GunTest.png", 7)

        #Var Weapon 
        # Var Waepons

        self.weapons_data= {
            "M4": {
                "name": "M4",
                "image": self.weapon_image
            },
            "Laser": {
                "name": "Laser",
                "image": self.laser_image
            },
            "Pistolet" :{
                "name": "Pistolet",
                "image": self.pistolet_image
            }
        }
        self.weapons_list = [weapons for weapons in self.weapons_data.keys()]
        self.weapons = [self.weapons_data[weapon]["image"] for weapon in self.weapons_list]

        # Charger la musique
        pygame.mixer.music.load("src/son/pixelmusique2.mp3")
        pygame.mixer.music.play(-1)

        # Créer un dégradé radial
        self.generate_radial_gradient()



    def draw_radial_gradient(self):
        self.screen.blit(self.background_gradient, (0, 0))


    # load les images et les resize
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

    def generate_radial_gradient(self):
       # Créer une surface pour le dégradé radial
        gradient_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        
        # Obtenir le centre de l'écran
        center_x, center_y = self.screen.get_width() // 2, self.screen.get_height() // 2
        
        # Rayon maximum (distance du centre aux coins)
        max_radius = math.sqrt(center_x**2 + center_y**2)

        radius = max_radius
        compteur = max_radius
        
        # Dessiner le dégradé radial
        while compteur > 0:
            alpha = int(255 - (1 + radius / max_radius))
            color = (0, 0, 0, alpha)
            pygame.draw.circle(gradient_surface, color, (center_x, center_y), radius)
            compteur -= 10
            radius -= 10
        
        self.background_gradient = gradient_surface




    # spawne quelque chose autour du joueur
    def zombie_spawn(self, spawn_radius, min_distance, target_list):
        while True:
            target_x = random.randint(int(self.player_position[0] - spawn_radius),
                                      int(self.player_position[0] + spawn_radius))
            target_y = random.randint(int(self.player_position[1] - spawn_radius),
                                      int(self.player_position[1] + spawn_radius))
            target_pos = [target_x, target_y]
            distance_squared = tools.distance_squared(target_pos, self.player_position)

            if distance_squared >= min_distance ** 2:
                break
        type_ = random.randint(1,100)

        if self.boss_state:
            zombie_type = 'boss1' 
        else:    
            if type_ < 80:
                zombie_type = 'normal'
            elif type_ >= 80:
                zombie_type = 'deviant'

        newZ = Zombie(target_pos, zombie_type)
        target_list.append(newZ)

    def spawn_objects(self, spawn_radius, min_distance, target_image, target_list, type):
        while True:
            target_x = random.randint(int(self.player_position[0] - spawn_radius),
                                      int(self.player_position[0] + spawn_radius))
            target_y = random.randint(int(self.player_position[1] - spawn_radius),
                                      int(self.player_position[1] + spawn_radius))
            target_pos = [target_x, target_y]
            distance_squared = tools.distance_squared(target_pos, self.player_position)

            if distance_squared >= min_distance ** 2:
                break
        if type == "lucky_block":
            target_rect = target_image.get_rect(center=(target_x, target_y))
            target_list.append(target_rect)
    
    def spawn_around_player(self, spawn_radius, min_distance, target_image, targetlist):
        while True:
            target_x = random.randint(int(self.player_position[0] - spawn_radius),
                                      int(self.player_position[0] + spawn_radius))
            target_y = random.randint(int(self.player_position[1] - spawn_radius),
                                      int(self.player_position[1] + spawn_radius))
            target_pos = [target_x, target_y]
            distance_squared = tools.distance_squared(target_pos, self.player_position)

            if distance_squared >= min_distance ** 2:
                break

        target_rect = target_image.get_rect(center=(target_x, target_y))
        targetlist.append(target_rect)

    # check une limite de choses proches
    def check_number_of_close(self, targets, rayon, max_number):
        number = 0
        for target in targets:
            target_pos = [target.x, target.y]
            distance_squared = tools.distance_squared(target_pos, self.player_position)
            if distance_squared < rayon ** 2:
                number += 1
        return number < max_number

    # inertie
    def smooth_damp(self, current, target, current_velocity, smooth_time, delta_time):
        smooth_time = max(0.0001, smooth_time)  # Évite la division par zéro
        omega = 2.0 / smooth_time
        x = omega * delta_time
        exp = 1 / (1 + x + 0.48 * x ** 2 + 0.235 * x ** 3)

        change = current - target
        temp = (current_velocity + omega * change) * delta_time
        new_velocity = (current_velocity - omega * temp) * exp
        new_position = target + (change + temp) * exp

        return new_position, new_velocity

    # tir des balles
    def shoot_bullet(self):
        if not self.zombies:
            return

        # Trouver le zombie le plus proche
        closest_zombie = min(
            self.zombies, key=lambda zombie: (zombie.zombie_pos[0] - self.player_position[0]) ** 2 + (zombie.zombie_pos[1] - self.player_position[1]) ** 2
        )

        dx = closest_zombie.zombie_pos[0] - self.player_position[0]
        dy = closest_zombie.zombie_pos[1] - self.player_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx /= distance
            dy /= distance

        # Calculer angle balle (tigo toa (toi toiii))
        angle = math.degrees(math.atan2(-dy, dx))  # Angle en degrés

        # On tourne le gun
        self.rotated_weapon_image = pygame.transform.rotate(self.weapon_image, angle)

        for i in range(self.bullet_number):
            offset_x = 30 + (10 * i)
            offset_y = 30 + (10 * i)

            # Créer une copie individuelle pour chaque balle avec son angle propre
            rotated_bullet_image = pygame.transform.rotate(self.bullet_image, angle)
            bullet_rect = rotated_bullet_image.get_rect(
                center=(self.player_position[0] + offset_x, self.player_position[1] + offset_y)
            )
            self.son_tir.play()

            self.bullets.append({
                'rect': bullet_rect,
                'direction': (dx, dy),
                'image': rotated_bullet_image  # Image chaque balle
            })

    # deplace les balles
    def move_bullets(self):
        for bullet in self.bullets[:]:
            # Déplacement de la balle
            bullet['rect'].x += bullet['direction'][0] * self.BULLET_VELOCITY
            bullet['rect'].y += bullet['direction'][1] * self.BULLET_VELOCITY

            target_pos = [bullet['rect'].x, bullet['rect'].y]

            # Supprimer les balles trop loin du joueur
            distance_squared = tools.distance_squared(target_pos, self.player_position)
            if distance_squared > self.BULLET_MAX_DISTANCE ** 2:
                self.bullets.remove(bullet)
                continue

            #  collisions balle et zombie
            for zombie in self.zombies:

                if bullet['rect'].colliderect(zombie.zombie_hitbox):

                    self.bullets.remove(bullet)

                    zombie.zombie_hp -= 100
                    random.choice(self.ZOMBIE_DAMAGE_SOUNDS).play()


                    if zombie.zombie_hp <= 0:
                        self.kill_count += 1
                        random_ = random.randint(0,100)

                        if random_ <20:
                            # Spawn un orbe d'xp à la position du zombie
                            xp_orb_rect = self.xp_image.get_rect(center=zombie.zombie_hitbox.center)
                            self.zombies.remove(zombie)
                            self.xp_orbs.append({'rect': xp_orb_rect, 'value': 10})  # Chaque orbe vaut 10 XP
                        if random_ >= 95 and random_ < 100:
                            health_orb_rect = self.health_image.get_rect(center=zombie.zombie_hitbox.center)
                            self.zombies.remove(zombie)
                            self.health_potions.append({'rect': health_orb_rect, 'value': 1}) 
                        if random_ >= 20 and random_ < 95:
                            bombe_rect = self.bombe_image.get_rect(center=zombie.zombie_hitbox.center)
                            self.zombies.remove(zombie)
                            self.bombs.append({'rect': bombe_rect, 'value': 1}) 
                    break

    # affiche le hud
    def display_hud(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
        self.screen.blit(timer_text, (20, 20))
        kill_text = self.font.render(f"Kills: {self.kill_count}", True, (255, 255, 255))
        self.screen.blit(kill_text, (20, 70))
        hp_text = self.font.render(f"HP: {self.player_health}", True, (255, 255, 255))
        self.screen.blit(hp_text, (20, 120))
        xp_text = self.font.render(f"XP: {self.player_xp}", True, (255, 255, 255))
        self.screen.blit(xp_text, (20, 170))
        level_text = self.font.render(f"LVL: {self.player_lvl}", True, (255, 255, 255))
        self.screen.blit(level_text, (20, 220))

    # fin du jeu
    def end_game(self):  # a refaire
        self.screen.fill((0, 0, 0))
        text = self.font.render("Rip", True, (255, 0, 0))
        self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width()//2, self.SCREEN_HEIGHT // 2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # collecter l'xp
    def collect_xp_orbs(self):
        for orb in self.xp_orbs[:]:

            target_pos = [orb['rect'].centerx, orb['rect'].centery]

            distance_squared = tools.distance_squared(target_pos, self.player_position)

            if distance_squared < 100 ** 2:
                self.player_xp += orb['value']
                self.xp_orbs.remove(orb)

    def collect_health_potion(self):
        for pot in self.health_potions[:]:

            target_pos = [pot['rect'].centerx, pot['rect'].centery]

            distance_squared = tools.distance_squared(target_pos, self.player_position)

            if distance_squared < 100 ** 2:
                if self.player_health < 10:
                    self.player_health += pot['value']
                self.health_potions.remove(pot)

    def collect_bombe(self):
        for bombe in self.bombs[:]:

            target_pos = [bombe['rect'].centerx, bombe['rect'].centery]

            distance_squared = tools.distance_squared(target_pos, self.player_position)

            if distance_squared < 100 ** 2:
                self.player_effect_bomb()
                self.bombs.remove(bombe)

              

    # collecter les luckys blocks
    def collect_lucky_blocks(self):
        for box in self.boxes:
            box_dx = self.player_position[0] - box.x
            box_dy = self.player_position[1] - box.y
            distance = math.sqrt(box_dx ** 2 + box_dy ** 2)

            if distance <= 100:
                self.open_lucky_blocks()

                self.boxes.remove(box)
                break

    # ouvres les luckys blocks
    def open_lucky_blocks(self):
        options = ["bombe"]
      #  options = ["bombe", "soin", "invincibilite"]
        choice = random.choice(options)

        if choice == "bombe":
            print("Effet: Bombe")
            self.player_effect_bomb()

       # elif choice == "soin":
            print("Effet: Soin")
            self.player_effect_heal()
            self.son_soin = pygame.mixer.Sound("src/son/HealthBoost.mp3")
        #elif choice == "invincibilite":
            print("Effet: Invincibilité")
            self.player_effect_invincibility()

    # effet lucky : bombe
    def player_effect_bomb(self):
        self.son_bombe.play()
        for zombie in self.zombies:
            if zombie.zombie_type == 'boss1':
                continue
            self.zombies.remove(zombie)
            xp_orb_rect = self.xp_image.get_rect(center=zombie.zombie_hitbox.center)
            self.xp_orbs.append({'rect': xp_orb_rect, 'value': 10})
            self.screen.fill((255, 255, 255))
            self.kill_count += 1
                

    # effet lucky : soin
    def player_effect_heal(self):
        if self.player_health < 10:
            self.player_health += 1

    # effet lucky : bouclier
    def player_effect_invincibility(self):
        print("a")

    # augmentation du level
    def level_up(self, lvl):
        self.player_lvl += 1
        self.shooting_cooldown = self.shooting_cooldown * 0.9 * lvl
        self.ZOMBIE_SPAWNCHANCHE = self.ZOMBIE_SPAWNCHANCHE * 1.2 * lvl
        if self.player_lvl >= self.last_ten_lvl:
            self.bullet_number += 1
            self.last_ten_lvl += 10
        self.LEVEL_UP = True
        # print(self.shooting_cooldown)

    # affichace du screen de level up
    def display_lvl_up_screen(self):
        self.screen.blit(self.lvl_up_image, (50, 50))

    # tinter une texture
    def tint_texture(self, surface, tint_color):
        tinted_surface = surface.copy()
        width, height = tinted_surface.get_size()
        for x in range(width):
            for y in range(height):
                color = tinted_surface.get_at((x, y))
                if color.r + color.g + color.b > 0:
                    r = min(color.r + tint_color[0], 255)
                    g = min(color.g + tint_color[1], 255)
                    b = min(color.b + tint_color[2], 255)
                    tinted_surface.set_at((x, y), (r, g, b))
        return tinted_surface
    
    #Flouter une surface
    def blur_surface(self, surface, amount):
        scale = 1.0 / amount
        surf_size = surface.get_size()
        scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf

    def update_player_direction(self):
        # Direction du joueur ?
        if self.player_velocity_x > 0:
            # Droite
            self.player_image = self.original_player_image
        elif self.player_velocity_x < 0:
            # Gauche
            self.player_image = pygame.transform.flip(self.original_player_image, True, False)


    def laser_shoot(self):
  
        # Calculer le Laser
        end_x = self.player_position[0] + self.laser_length * math.cos(math.radians(self.laser_angle))
        end_y = self.player_position[1] + self.laser_length * math.sin(math.radians(self.laser_angle))

        # Dessine le Laser
        pygame.draw.line(self.screen, self.laser_color, (self.player_position[0],self.player_position[1]), (end_x, end_y), 2)
        print(self.player_position[0])
        # Rotation
        self.laser_angle += self.laser_speed
        if self.laser_angle >= 360:
            self.laser_angle = 0
        print(self.player_position[1])
        print(self.player_position[0])


            




    # run le jeu
    def run_game(self):
        while self.run and not(self.menu):
            self.screen.fill(self.BACKGROUND_COLOR)

            # Déplace le fond pour que le joueur soit toujours centré
            for y in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE):
                for x in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE):
                    self.screen.blit(self.background_image, (x - self.camera_position[0], y - self.camera_position[1]))

            # Mise à jour de la position du joueur
            target_x = (self.player_movement_x[1] - self.player_movement_x[0]) * self.PLAYER_VELOCITY
            target_y = (self.player_movement_y[1] - self.player_movement_y[0]) * self.PLAYER_VELOCITY
                #Mise à jour verticale
            self.player_position[0], self.player_velocity_x = self.smooth_damp(
                self.player_position[0],
                self.player_position[0] + target_x,
                self.player_velocity_x,
                self.smooth_time,
                self.delta_time)
                #Mise à jour Horizontale
            self.player_position[1], self.player_velocity_y = self.smooth_damp(
                self.player_position[1],
                self.player_position[1] + target_y,
                self.player_velocity_y,
                self.smooth_time,
                self.delta_time)
            
            self.update_player_direction() #Flip

            
            # On bouge le gun avec le joueur
            self.gun_position[0] = self.player_position[0]
            self.gun_position[1] = self.player_position[1]

            # Déplace la caméra pour centrer le joueur
            self.camera_position[0] = self.player_position[0] - self.SCREEN_WIDTH // 2
            self.camera_position[1] = self.player_position[1] - self.SCREEN_HEIGHT // 2

            # Spawn de zombies à chaque itération
            if random.random() < self.ZOMBIE_SPAWNCHANCHE and self.boss_state == False:
                self.zombie_spawn(500, 400, self.zombies)

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            if elapsed_time > 60 + 120*self.bosses_spawned and self.boss_state == False:
                self.boss_state = True
                self.zombie_spawn(500, 400, self.zombies)
                self.bosses_spawned += 1


            # Spawn des boxs
            if random.random() < self.BOX_SPAWN_CHANCE:
                if self.check_number_of_close(self.boxes, rayon=2000, max_number=1):
                    self.spawn_around_player(600, 100, self.luckyblock_image, self.lucky_blocks)

            # Déplace les zombies et les balles
            for zombie in self.zombies:
                Zombie.update_hitbox(zombie)
                           
                if Zombie.move_zombies(zombie, self.player_position):
                    self.zombies.remove(zombie)  
                    self.screen.fill((255, 0, 0))
                    self.player_health -= 1 
                    random.choice(self.PLAYER_DAMAGE_SOUNDS).play()
                self.screen.blit(zombie.zombie_image, (zombie.zombie_pos[0] - self.camera_position[0], zombie.zombie_pos[1] - self.camera_position[1]))


            self.move_bullets()

            for zombie in self.zombies:
                if getattr(zombie,'zombie_vel') == 2:
                    if random.randint(0,1000) < 5:
                        Zombie.speed_boost(zombie)


            # Rammase l'xp et les box
            self.collect_xp_orbs()
            self.collect_lucky_blocks()
            self.collect_health_potion()
            self.collect_bombe()
            # Levelup
            if self.player_xp >= 100:
                self.level_up(1)
                self.player_xp -= 100

            # Dessines les orbes d'xp
            for orb in self.xp_orbs:
                self.screen.blit(self.xp_image,
                                 (orb['rect'].x - self.camera_position[0], orb['rect'].y - self.camera_position[1]))
            
            for pot in self.health_potions:
                self.screen.blit(self.health_image,
                                 (pot['rect'].x - self.camera_position[0], pot['rect'].y - self.camera_position[1]))

            for bomb in self.bombs:
                self.screen.blit(self.bombe_image,
                                 (bomb['rect'].x - self.camera_position[0], bomb['rect'].y - self.camera_position[1]))


            # Dessines les boxs
            for box in self.boxes:
                self.screen.blit(self.luckyblock_image,
                                 (box.x - self.camera_position[0], box.y - self.camera_position[1]))

            # Dessine les balles
            for bullet in self.bullets:
                self.screen.blit(
                    bullet['image'],
                    (bullet['rect'].x - self.camera_position[0], bullet['rect'].y - self.camera_position[1])
                )

            # Dessines le joueur et le gun
            self.screen.blit(self.player_image, (
            self.player_position[0] - self.camera_position[0] - 50, self.player_position[1] - self.camera_position[1]))

            self.screen.blit(self.rotated_weapon_image, (
            self.gun_position[0] - self.camera_position[0] - 50, self.gun_position[1] - self.camera_position[1]))

            # Le hud
            self.display_hud()

            # Gestion des inputs
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
                    if event.key == pygame.K_p: 
                        self.pause_menu()
                         ##CHEATS CODES ET TESTS
                    # if event.key == pygame.K_SPACE:
                    #    self.shoot_bullet()             # Tir manuel
                    # if event.key == pygame.K_a:
                    #     self.player_image = self.tint_texture(self.player_image, (0, 0, 200 ))
                   ## if event.key == pygame.K_b:
                     #   self.player_effect_bomb()
                   # if event.key == pygame.K_t:
                    #    print(self.check_number_of_close(self.boxes, 500, 2)) 
                    if event.key == pygame.K_s:
                        self.PLAYER_VELOCITY += 200
                    if event.key == pygame.K_ESCAPE:
                        self.menu = True

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

            # self.laser_shoot()

            if int(self.player_position[0]) > self.BACKGROUND_MAP_SIZE or int(self.player_position[1]) > self.BACKGROUND_MAP_SIZE or int(self.player_position[0]) < -self.BACKGROUND_MAP_SIZE or int(self.player_position[1]) < -self.BACKGROUND_MAP_SIZE:
                self.player_health -= 1

                # Mort
            if self.player_health <= 0:
                self.end_game()

            pygame.display.update()
            self.clock.tick(60)


    def main_menu(self):
        press_space_text = self.font.render("Press space to start...", True, (255, 255, 255))
        enter_skin_menu_text = self.font.render("Press M to enter skin menu", True, (255, 255, 255))
        enter_weapon_menu_text = self.font.render("Press W to enter weapon menu", True, (255, 255, 255))
        skin_menu_text = self.font.render("Bienvenue dans le Menu Skin - Work in progress", True, (255, 255, 255))
        control_menu_text = self.font.render("Use Arrows to Move, Press escape to exit, Press P to pause", True, (255, 255, 255))

        while self.run and self.menu:
            self.screen.fill((100, 100, 150))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.menu = False
                        self.run_game()  # Lance  le jeu à la fermeture du menu
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_m:
                        self.menu_skin = True
                    if event.key == pygame.K_w:
                        self.menu_weapon = True


            # Affichage des textes principaux (menu principal)
            self.screen.blit(press_space_text, (50, 50))
            self.screen.blit(enter_skin_menu_text, (50, 100))
            self.screen.blit(enter_weapon_menu_text, (50, 150))
            self.screen.blit(control_menu_text, (50, 200))
            pygame.display.flip()

            # Menu Skin
            if self.menu_skin:
                selected_index = 0  # Index du skin sélectionné (celui qui sera affiché au centre)
                gap = 300         # Espace  entre chaque skin

                while self.run and self.menu_skin:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.menu_skin = False
                            # Navigation dans la liste des skins
                            elif event.key == pygame.K_LEFT:
                                selected_index = (selected_index - 1) % len(self.skins)
                            elif event.key == pygame.K_RIGHT:
                                selected_index = (selected_index + 1) % len(self.skins)
                            # Selectionner le bon skin
                            elif event.key == pygame.K_SPACE:
                                self.player_image = self.skins[selected_index]
                                self.original_player_image = self.player_image
                                self.menu_skin = False

                    # Mise à jour du skin sélectionné
                    self.skin_selected = self.skins[selected_index]

                    self.screen.fill((100, 100, 150))
                    self.screen.blit(skin_menu_text, (self.SCREEN_WIDTH // 2 - 200, 50))
                    current_skin_text = self.font.render("Skin actuel : " + str(selected_index), True, (255, 255, 255))
                    self.screen.blit(current_skin_text, (self.SCREEN_WIDTH // 2 - 200, 100))
                    self.screen.blit(self.font.render("V", True, (255, 255, 255)),(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 - self.SCREEN_HEIGHT//8))

                    # Calculer la position centrale
                    center_x = self.SCREEN_WIDTH // 2
                    skin_y = self.SCREEN_HEIGHT // 2 - self.skins[0].get_height() // 2

                    # Affichage de chaque skin en fonction de selected_index pour centrer le skin choisi
                    for i, skin in enumerate(self.skins):
                        # La position en x est décalée selon la distance par rapport au skin sélectionné
                        x = center_x + (i - selected_index) * gap - skin.get_width() // 2
                        scaled_skin = pygame.transform.scale(skin, (skin.get_width() * 3, skin.get_height() * 3))
                        self.screen.blit(scaled_skin, (x, skin_y))
                


                    pygame.display.update()
                    self.clock.tick(60)

            #Menu Weapon
            if self.menu_weapon == True:
                weapon_menu_text = self.font.render("Bienvenue dans le Menu Weapon - Work in progress", True, (255, 255, 255))
                selected_index = 0  # Index 
                gap = self.SCREEN_WIDTH//4  # Espace
                scale_factor = 3  # Augmentation des images

                while self.run and self.main_menu and self.menu_weapon:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.menu_weapon = False
                            # Navigation
                            elif event.key == pygame.K_LEFT:
                                selected_index = (selected_index - 1) % len(self.weapons)
                            elif event.key == pygame.K_RIGHT:
                                selected_index = (selected_index + 1) % len(self.weapons)
                            # Selection des Armes
                            elif event.key == pygame.K_SPACE:
                                self.weapon_image = self.weapons[selected_index]
                                self.menu_weapon = False

                    # Update 
                    #self.weapon_selected = self.weapons[selected_index]

                    self.screen.fill((100, 100, 150))
                    self.screen.blit(weapon_menu_text, (self.SCREEN_WIDTH // 2 - 200, 50))
                    current_weapon_text = self.font.render("Weapon actuel : " + str(selected_index), True, (255, 255, 255))
                    self.screen.blit(current_weapon_text, (self.SCREEN_WIDTH // 2 - 200, 100))
                    self.screen.blit(self.font.render("V", True, (255, 255, 255)),(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 - self.SCREEN_HEIGHT//8))

                    # Position centrale
                    center_x = self.SCREEN_WIDTH // 2
                    weapon_y = self.SCREEN_HEIGHT // 2 - self.weapons_data[self.weapons_list[0]]["image"].get_height() // 2

                    for i, weapon in enumerate(self.weapons):
                        x = center_x + (i - selected_index) * gap - weapon.get_width() // 2
                        scaled_weapon = pygame.transform.scale(weapon, (weapon.get_width() * scale_factor, weapon.get_height() * scale_factor))
                        self.screen.blit(scaled_weapon, (x, weapon_y))
                    pygame.display.update()
                    self.clock.tick(60)

       

    def pause_menu(self):
        # Capture de l'écran
        paused_screen = self.screen.copy()
        # Flouter l'écran
        blurred_screen = self.blur_surface(paused_screen, 10)

        # Texte de l'écran
        pause_text = self.font.render("Press space to resume", True, (255, 255, 255))

        paused = True
        while paused:
            self.screen.blit(blurred_screen, (0, 0))
            self.screen.blit(pause_text, (self.SCREEN_WIDTH // 2 - pause_text.get_width() // 2, self.SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        paused = False
                        self.player_movement_y[0] = False
                        self.player_movement_y[1] = False
                        self.player_movement_x[0] = False
                        self.player_movement_x[1] = False

            self.clock.tick(60)

Game().main_menu()