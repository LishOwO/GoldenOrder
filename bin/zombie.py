import sys
import math
import tools

class Zombie:
    def __init__ (self, hp, ):
        
        pass

        #deplace les zombie
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
                self.screen.fill((255, 0, 0))
                self.PLAYER_HP -= 1 
                self.PLAYER_DAMAGE_SOUND.play()
                break #fix

