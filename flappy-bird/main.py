import pygame
import random


pygame.init()
clock = pygame.time.Clock()

win_height = 720
win_width = 551

window = pygame.display.set_mode((win_width, win_height))

skyline_image = pygame.image.load('assets/background.png')
bird_images = [
    pygame.image.load('assets/bird_down.png'),
    pygame.image.load('assets/bird_mid.png'),
    pygame.image.load('assets/bird_up.png')
]

game_over = pygame.image.load('assets/game_over.png')

pipe_top = pygame.image.load('assets/pipe_top.png')
pipe_bottom = pygame.image.load('assets/pipe_bottom.png')

bird_start_position = (100, 250)

score = 0

font = pygame.font.SysFont('Comic Sans',53)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, direction,x, y):
        pygame.sprite.Sprite.__init__(self)

        self.passed = False

        if direction == 'top':
            self.image = pipe_top

        else:
            self.image = pipe_bottom

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

    def update(self):
        self.rect.x += -1
        if self.rect.x < -win_width:
            self.kill()
        global score
        if self.rect.x <= 48 and not self.passed and self.direction == 'top':
            score += 1
            self.passed = True



class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position

        self.image_index = 0
        self.flap = False
        self.alive = True
        self.vel = 0

    def update(self, user_input):
        # Animate Bird
        if self.alive:
            self.image_index += 1

        # Resets the animation
        if self.image_index >= 30:
            self.image_index = 0

        current_index = self.image_index // 10
        self.image = bird_images[current_index]

        # Gravity and Flap
        self.vel += 0.5

        if self.vel > 7:
            self.vel = 7

        if self.rect.y < 700:
            self.rect.y += int(self.vel)

        if self.vel == 0:
            self.flap = False

        # User Input
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7


def main():
    run = True

    # Instantiate the bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    pipe_timer = 0

    pipes = pygame.sprite.Group()




    while run:
        pygame.event.pump()
        user_input = pygame.key.get_pressed()

        # Reset frame
        window.fill((0, 0, 0))

        window.blit(skyline_image, (0, 0))

        bird.draw(window)
        pipes.draw(window)

        global score
        score_text = font.render('score: ' + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20,20))

        bird.update(user_input)
        if bird.sprite.alive:
            pipes.update()

        bird_sprites = bird.sprites()
        ground_colide = bird.sprite.rect.y > win_height -40
        pipe_collide = pygame.sprite.spritecollide(bird_sprites[0], pipes, False)
        if pipe_collide or ground_colide:
            bird.sprite.alive = False
            window.blit(game_over, (win_width // 2 - game_over.get_width() // 2,
                                              win_height // 2 - game_over.get_height() // 2))
            if user_input[pygame.K_r]:
                score = 0
                bird = pygame.sprite.GroupSingle()
                bird.add(Bird())

                pipe_timer = 0

                pipes = pygame.sprite.Group()

        # spawning pipes logic
        if pipe_timer <= 0 and bird.sprite.alive:
            x = 550
            y_top = random.randint(-600, -480)
            y_bot = y_top + random.randint(90, 130) + pipe_bottom.get_height()
            pipes.add(Pipe('top',x, y_top))
            pipes.add(Pipe('bot',x, y_bot))
            pipe_timer = random.randint(180, 250)

        pipe_timer -= 1




        clock.tick(60)


        pygame.display.update()
main()