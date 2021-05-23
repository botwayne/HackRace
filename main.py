#Note replit doesn't run music

import pygame
from player import user, make_user
from game import car, random_obstacle
from game import roadobject
from game import track
import random
import time

tracks = [pygame.image.load("Hackathon.png"), pygame.image.load("Hackathon2.png"), pygame.image.load("Hackathon3.png"),
          pygame.image.load("Hackathon4.png"), pygame.image.load("Hackathon5.png")]
cars = [car(10, "car2.png", 25), car(17, "car.png", 30), car(25, "car3.png", 40)]  # Different cars for now
objects = [pygame.image.load("rock.png"), pygame.image.load("cone.PNG")]


def redrawWindow():
    # Redraw the window with new coords for img
    screen.blit(track1.img, (0, track1.y))  # draws our first bg image
    screen.blit(track2.img, (0, track2.y))  # draws the second bg image
    screen.blit(car_img, (users_car.x, users_car.y))

    # Draws each obstacle out if it has something
    for i in obstacles:
        # Checks that the y is still valid for obstacle
        if i.check_active(track1.img.get_height()):
            # Update y with speed
            i.update_y(users_car.carspeed)
            screen.blit(i.img, (i.x, i.y))


def update_background():
    track1.update_y(users_car.carspeed)
    track2.update_y(users_car.carspeed)

    # Get random track that isn't a duplicate from before
    # Checks if track is still within the height of 800
    if track1.y > track1.img.get_height():
        obstacles[0] = object_spawn(objects)

        # random track
        while True:
            tempTrack = random.choice(tracks)
            if not (tempTrack == track1.img):
                track1.img = tempTrack
                break
        track1.y = 0 - track1.img.get_height()

    # Checks if second track is still within the height of 800
    if track2.y > track2.img.get_height():
        # Copy previous, 2 in a row
        obstacles[1] = object_spawn(objects)
        track2.img = track1.img
        track2.y = 0 - track2.img.get_height()


# Spawns random object and resizes
def object_spawn(objects):
    obj = random_obstacle(objects)
    # Resize image
    obj.img = pygame.transform.scale(obj.img, (100, 100))
    return obj


def check_collision():
    for i in obstacles:
        # Check collision if object is within y vicinity of car
        if users_car.y - 1 < i.y + i.img.get_height() < users_car.y + car_img.get_height():  # Checks y are in collision.
            # Check collision between sides and middle of car
            if i.x < users_car.x < (i.x + i.img.get_width()) or i.x < (users_car.x + car_img.get_width() / 2) < (
                    i.x + i.img.get_width()) or i.x < (users_car.x + car_img.get_width()) < (i.x + i.img.get_width()):
                return True

    return False


def print_stop_watch(stop_watch):
    # Print stop_watch
    time_text = pygame.font.Font('freesansbold.ttf', 40).render(str(stop_watch), True, (0, 0, 0))
    text_rect = time_text.get_rect()
    text_rect.center = (84, 67.5)  # Centers text
    pygame.draw.rect(screen, (255, 255, 255), ((15, 15), (150, 100)))
    screen.blit(time_text, text_rect)


def print_crash_screen():
    crash_text = pygame.font.Font('freesansbold.ttf', 70).render("You Crashed!", True, (0, 0, 0))
    play_again = pygame.font.Font('freesansbold.ttf', 50).render("Play Again? Y or N!", True, (255, 225, 0))
    screen.blit(crash_text, (200, 300))
    screen.blit(play_again, (175, 400))


def get_mode():
    dict_of_mode = {"easy": 0, "medium": 1, "hard": 2}
    while True:
        mode = input().lower()
        try:
            return dict_of_mode[str(mode)]
        except:
            print("Please type a valid answer")


def play_game():

    #Make a username
    global player
    player = make_user()
    print("Hi " + player.name)
    print("Would you like to play easy, medium, or hard mode?")
    mode = get_mode()
    print("Loading now...")

    #Make it accessible
    global users_car
    global car_img
    global track1
    global track2
    global obstacles
    global screen
    global clock

    pygame.init()

    pygame.display.set_caption("Jam Hack Raceway")

    clock = pygame.time.Clock()  # FPS
    screen = pygame.display.set_mode((800, 800))

    #Delay time for user to switch over
    time1 = time.time()
    while (True):
        if int((time.time() - time1)) == 3:
            break

    # Sounds for crash and music
    crash_sound = pygame.mixer.Sound("crash.mp3")
    music = pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)

    # Have rounds to upload
    rounds = 1

    while True:

        # Inititate
        users_car = cars[mode]
        car_img = pygame.image.load(users_car.car_png)  # Grab image
        car_img = pygame.transform.scale(car_img, (100, 200))  # Shrink to reasonable size
        track1 = track(0 - 800, tracks)
        track2 = track(0, tracks)

        # Just place holders
        obstacles = [roadobject(objects[0]), roadobject(objects[0])]

        playing = True
        s_time = time.time()
        ten_sec_countdown_time = time.time()


        while playing:

            clock.tick(60)

            #Check collision, if collision true it stops round
            if check_collision():
                crash_sound.play()
                # Upload time, if new round then it'll change
                #Also increase rounds
                player.upload_scores(rounds, round(time.time() - s_time, 2))
                rounds += 1
                playing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            #Get input for left or right
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT] and users_car.x > 230:
                users_car.update_x(users_car.traction * -1)
            if pressed_keys[pygame.K_RIGHT] and users_car.x < 470:
                users_car.update_x(users_car.traction)

            update_background()
            redrawWindow()

            # Outputting current time. Calculate time + center it to screen
            stop_watch = round(time.time() - s_time, 2)
            print_stop_watch(stop_watch)

            #Make car speed up
            if int(time.time() - ten_sec_countdown_time) == 5:
                ten_sec_countdown_time = time.time()
                users_car.carspeed += 1

            pygame.display.update()

        #Prints the crash message
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_y]:
                break
            elif pressed_keys[pygame.K_n]:
                return

            print_crash_screen()
            pygame.display.update()


    pygame.quit


play_game()
player.read_scores()