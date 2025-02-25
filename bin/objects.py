import sys
class Objects:
    def __init__ (self, pos, type):

        self.obj_pos = pos
        self.obj_type = type

    # collecter les luckys blocks
    def collect_object(self, player_pos):
            obj_dx = self.player_position[0] - self.obj_pos[0]
            obj_dy = self.player_position[1] - self.obj_pos[1]
            distance = math.sqrt(obj_dx ** 2 + obj_dy ** 2)

            if distance <= 100:
                if self.obj_type == "lucky_block"
                    self.open_lucky_blocks()
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
            self.zombies.remove(zombie)
            xp_orb_rect = self.xp_image.get_rect(center=zombie.zombie_hitbox.center)
            self.xp_orbs.append({'rect': xp_orb_rect, 'value': 10})
            self.screen.fill((255, 255, 255))
            self.kill_count += 1

        return True
                

    # effet lucky : soin
    def player_effect_heal(self):
        if self.PLAYER_HP < 10:
            self.PLAYER_HP += 1
        return True

    # effet lucky : bouclier
    def player_effect_invincibility(self):
        print("a")
        return True
