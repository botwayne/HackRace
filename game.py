import random


class track:

    def __init__(self, y, img_list):
        self.img_list = img_list
        self.img = img_list[0]
        self.y = y

    # Update y value of track img
    def update_y(self, value):
        self.y += value


class car:

    def __init__(self, carspeed, car_png="car.png", traction=15, y=450):
        self.carspeed = carspeed
        self.car_png = car_png
        self.car_name = self.car_png.replace(".png", "")
        self.x = 300
        self.traction = traction  # Move side to side speed
        self.y = y

    def update_x(self, value):
        # Updates the x value to change
        self.x += value

    def update_speed(self, value):
        self.carspeed += value


class roadobject:

    def __init__(self, img, left_side = False, y=1000): #y = 1000 for check_active
        self.img = img
        self.left_side = left_side  # If not left side it's right side
        self.y = y
        if self.left_side:
            self.x = 250
        else:
            self.x = 450

    #Checks whether road object is still within play (moving down in the screen)
    def check_active(self, height):
        if self.y < height:
            return True

        return False

    def update_y(self, speed):
        self.y += speed


def random_obstacle(roadobjects):
    # Random number. 35% chance of spawning
    chance = random.randint(0, 100)
    if chance > 65:
        random_side = random.choice([True, False])
        random_object = random.choice(roadobjects)
        return roadobject(random_object, random_side, -800)
    return roadobject(roadobjects[0], False, 1000) #Invalid road object to pass on y = 1000