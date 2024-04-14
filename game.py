import pygame
import random
import os

class FlightMasterGame:
    def __init__(self):
        self.initialize_variables()

    def initialize_variables(self):

        # Directory containing game assets
        assets_dir = 'gallery\sprites'

        # File paths for game assets
        self.player_image_path = os.path.join(assets_dir, 'player.png')
        self.background_image_path = os.path.join(assets_dir, 'background.jpg')
        self.welcome_image_path = os.path.join(assets_dir, 'welcome-screen.png')
        self.end_image_path = os.path.join(assets_dir, 'end-screen.png')
        self.dino_image_path = os.path.join(assets_dir, 'dino.png')
        self.icon_image_path = os.path.join(assets_dir, 'score.png')

        # Colors
        self.WHITE = (255, 255, 255)
        self.GOLDEN = (255, 215, 0)
        self.BLACK = (0, 0, 0)

        # Initialize Pygame
        pygame.init()

        # Create the game window
        self.screen_width = 400
        self.screen_height = 680
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Load the icon image
        print("loading icon image", self.icon_image_path)
        self.icon_image = pygame.image.load(self.icon_image_path)
        pygame.display.set_icon(self.icon_image)

        # Frames per second
        self.FPS = 30

        # Initial SPEED of the player
        self.SPEED = 300

        # Level up threshold 
        self.LEV_THRESHOLD = 20 

        # List to store player movement
        self.dx = []

        # Horizontal position of the player
        self.xx = -2

        # Vertical position of the background
        self.back_Y = -700

        # Initial ball number
        self.ball_no = -9

        # Set up the font
        self.font = pygame.font.Font(None, 36)

        # Initialize clock
        self.clock = pygame.time.Clock()


        # Load background and welcome images
        self.bck_image = pygame.image.load(self.background_image_path)
        self.welcome_image = pygame.image.load(self.welcome_image_path).convert()
        self.welcome_image = pygame.transform.smoothscale(self.welcome_image, self.screen.get_size())  

        # Initialize best score
        self.best_score = self.load_best_score()


    def load_best_score(self):
        try:
            with open("best_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_best_score(self, best_score):
        with open("best_score.txt", "w") as file:
            file.write(str(best_score))


    def restart_game(self):
        self.FPS = 30
        self.SPEED = 300
        self.xx = -2
        self.back_Y = -700
        self.dx = []
        self.score = 1
        self.welcome_screen()

    def show_end_screen(self, current_score):
        end_image = pygame.image.load(self.end_image_path)  
        end_image = pygame.transform.scale(end_image, (400, 680))  
        
        print(current_score, self.best_score)
        best_score = max(current_score, self.best_score)
        self.save_best_score(best_score)

        pygame.mixer.music.load('gallery\music\\thunderbird-game-over-9232.mp3') 
        pygame.mixer.music.play(-1)

        refresh_button = self.font.render("Replay", True, (255,255,255))
        
        refresh_rect = refresh_button.get_rect(center=(self.screen_width // 2, self.screen_height -40))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if refresh_rect.collidepoint(event.pos):
                        self.restart_game()
                        return

            # Detect mouse position
            mouse_pos = pygame.mouse.get_pos()
            # Check if mouse is hovering over refresh button text
            if refresh_rect.collidepoint(mouse_pos):
                # Change cursor to hand when hovering over refresh button
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            else:
                # Reset cursor to default when not hovering over refresh button
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                
            # Clear the screen
            self.screen.fill((0, 0, 0))
            # Display end image
            self.screen.blit(end_image, (0,0))

            # Render and display text for current score
            current_score_text = self.font.render(f"{current_score}", True, (255, 255, 255))
            self.screen.blit(current_score_text, (200, 353))

            # Render and display text for best score
            best_score_text = self.font.render(f"{best_score}", True, (255, 255, 255))
            self.screen.blit(best_score_text, (200, 393))

            # Render and display refresh button text
            self.screen.blit(refresh_button, refresh_rect)
            # Update the display
            pygame.display.flip()

    def welcome_screen(self):
        pygame.mixer.music.load('gallery\music\\thunderbird-game-over-9232.mp3') 
        pygame.mixer.music.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                    self.main_game()
                    # return

                else:
                    self.screen.fill((0, 0, 0))  
                    welcome_image = pygame.image.load(self.welcome_image_path).convert()
                    welcome_image = pygame.transform.smoothscale(welcome_image, self.screen.get_size())
                    self.screen.blit(welcome_image, (0, 0))  
                    pygame.display.update()

    def main_game(self):
        pygame.mixer.music.load('gallery\music\music-for-arcade-style-game-146875.mp3') 
        pygame.mixer.music.play(-1)

        level_up_sound = pygame.mixer.Sound('gallery\music\level-up.mp3')
        collision_sound = pygame.mixer.Sound("gallery\music\collision.wav")

        level_thresh = 20
        player_image = pygame.image.load(self.player_image_path).convert_alpha()
        player_rect = player_image.get_rect()
        player_rect.center = (200, 600)  
        print("refe:", player_rect.center)
        player_mask = pygame.mask.from_surface(player_image)

        y_offset = 20  
        ball_x = random.randrange(12, 350)  
        angle = 0
        score = 1

        while True:
            dt = self.clock.tick(self.FPS) / 1000.0  

            ball_image = pygame.image.load(self.get_ball()).convert_alpha()
            standard_width = 70
            standard_height = 70
            ball_image = pygame.transform.scale(ball_image, (standard_width, standard_height))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.dx.insert(0, -self.SPEED)  
                    elif event.key == pygame.K_RIGHT:
                        self.dx.insert(0, self.SPEED)  

            if self.dx:  
                player_rect.x += self.dx[0] * dt  
                if player_rect.x > 345 or player_rect.x < -3:  
                    self.show_end_screen(int(score/10))

            f = self.get_update()  
            bck_motion = self.bck_update()  

            self.screen.fill((0, 0, 0))  
            ball_y = y_offset + f  
            if ball_y > 700:
                self.xx = -2
                y_offset = 20
                ball_x = random.randrange(11, 350)

            if (player_rect.colliderect((ball_x, ball_y, ball_image.get_width(), ball_image.get_height()))):
                collision_sound.play()
                score -= 5*10
                self.xx = -2
                y_offset = 20

            if score <= 0:
                self.show_end_screen(int(score/10))

            self.screen.blit(self.bck_image, (0, bck_motion))  
            self.screen.blit(self.bck_image, (0, (bck_motion - 1300)))  
            if bck_motion > 860:
                self.back_Y = -700
                
            self.screen.blit(player_image, player_rect)  
            self.screen.blit(ball_image, (ball_x, ball_y))  

            current_score = int(score/10)
            if current_score == 0:
                current_score = 1
            score_text = self.font.render(str(current_score), True, self.GOLDEN)
            text_rect = score_text.get_rect()
            text_rect.topright = (self.screen_width - 10, 10)  
            self.screen.blit(score_text, text_rect)

            if current_score % level_thresh == 0:
                self.FPS += 2
                self.SPEED += 20
                level_thresh += 20

                level_up_sound.play()
                print('bangg!!')
                
            score += 1

            rotated_icon = pygame.transform.rotate(self.icon_image, angle)
            icon_rect = rotated_icon.get_rect()
            icon_rect.topright = (self.screen_width-40, 10)  
            self.screen.blit(rotated_icon, icon_rect)

            angle += 3
            
            if angle >= 360:
                angle = 0

            pygame.display.update()  

    def get_update(self):
        self.xx += 15
        return self.xx

    def bck_update(self):    
        self.back_Y += 1
        return self.back_Y

    def get_ball(self):
        balls = (
            'gallery/sprites/a-1.png',
            'gallery/sprites/a-2.png',
            'gallery/sprites/a-3.png',
            'gallery/sprites/a-4.png',
            'gallery/sprites/a-5.png'
        )
        if self.xx == -2:
            self.ball_no = random.randrange(0, 5)
        return balls[self.ball_no]

    def run_game(self):
        self.initialize_variables()
        self.welcome_screen()

if __name__ == "__main__":
    game = FlightMasterGame()
    game.run_game()

