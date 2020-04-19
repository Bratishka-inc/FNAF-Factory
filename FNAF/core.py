import pygame
import time

START_MENU = 0
OFFICE = 1
MONITOR = 3
HALL = 31
HALL_EAST = 32
WORKSHOP = 33
STORAGE = 34
HALL_1 = 35
FACTORY = 36
VENT_ROOM = 37
VENT_CENTER = 38
VENT_EAST = 39
VENT = 5


class Game():
    def __init__(self):
        self.midnight = 0
        self.timecost = 20 # если прошла 1сек реального времени, то прошло 20сек игрового
        self.timestamp = time.time()
        self.level = 1
        self.backstage = Backstage()
        self.office = Office()
        self.energy_bar = Energy_bar()
        self.status =  START_MENU
        pygame.mixer.music.set_volume(0.5)

    def update(self, event):
        if self.status == START_MENU:
             if event.type == pygame.MOUSEBUTTONDOWN:
                 if self.backstage.start.infocus(event.pos):
                     self.status = OFFICE
        elif self.status == OFFICE:
            if self.office.focus == OFFICE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.status = START_MENU
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    if 224 < event.pos[0] < 413 and 167 < event.pos[1] < 312:
                        self.office.focus = MONITOR
                        print("focus",self.office.focus)

            elif self.office.focus == MONITOR:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    def getcam(pos):

                        def getpos(line):
                            line = line.strip(" ()\n")
                            return map(int, line.split(", "))

                        with open("../src/map.data") as f:
                            for n in range(1, 10):
                                x_left, y_up = getpos(f.readline())
                                x_right, y_down = getpos(f.readline())
                                print(x_left, x_right, y_up, y_down)
                                print(pos)
                                if x_left < pos[0] < x_right and y_up < pos[1] < y_down:
                                    return n

                    selected_cam = getcam(event.pos)
                    if selected_cam:
                        self.office.monitor.camera = selected_cam + 30
                    elif self.office.monitor.exit_button.infocus(event.pos):
                        self.office.focus = OFFICE
                    elif self.office.monitor.camera == HALL and self.office.monitor.hall.door_button.infocus(event.pos):
                        self.office.monitor.hall.toogle_door()
                    elif self.office.monitor.camera == VENT_EAST and self.office.monitor.vent_east.vent_button.infocus(event.pos):
                        self.office.monitor.vent_east.toogle_vent()

    def flip(self):
        if self.status == START_MENU:
            self.backstage.draw()
        elif self.status == OFFICE:
            self.office.draw()
            self.energy_bar.draw(self.office.focus, self.timecost)

            current_time = int(pygame.time.get_ticks() / 1000 * self.timecost)
            if current_time == 60*60*4 and not self.midnight: # в полночь -1 заряд
                self.energy_bar.charge -= 1
                self.midnight = 1


class Backstage():
    def __init__(self):
        self.original_image = pygame.image.load("../src/images/menu_backstage.png")
        self.start = Button("start", (57, 299), "btn_play.png")
        self.sound = pygame.mixer.Sound("../src/music/background.wav")

    def draw(self):
        self.image = pygame.transform.scale(self.original_image, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))
        self.start.draw()
        self.sound.play(-1)



class Monitor():
    def __init__(self):
        self.camera = FACTORY
        self.factory = Factory()
        self.hall = Hall()
        self.hall_east = Hall_east()
        self.workshop = Workshop()
        self.storage = Storage()
        self.hall_1 = Hall_1()
        self.vent_room = Vent_room()
        self.vent_center = Vent_center()
        self.vent_east = Vent_east()
        self.map = Map()
        self.exit_button = Button("exit_button", (48, 530), "monitor_down.png")
        self.sound = pygame.mixer.Sound("../src/music/sound_camera.wav")

    def draw(self):
        if self.camera == FACTORY:
            self.factory.draw()
        elif self.camera == HALL:
            self.hall.draw()
        elif self.camera == HALL_EAST:
            self.hall_east.draw()
        elif self.camera == WORKSHOP:
            self.workshop.draw()
        elif self.camera == STORAGE:
            self.storage.draw()
        elif self.camera == HALL_1:
            self.hall_1.draw()
        elif self.camera == VENT_ROOM:
            self.vent_room.draw()
        elif self.camera == VENT_CENTER:
            self.vent_center.draw()
        elif self.camera == VENT_EAST:
            self.vent_east.draw()
        self.map.draw()
        self.exit_button.draw()
        #pygame.mixer.stop()
        self.sound.play(-1)

class Energy_bar():
    def __init__(self):
        self.font = pygame.font.Font("../src/fonts/clock.ttf", 26)
        self.charge = 4
    def draw(self, focus, timecost):
        ori_image = pygame.image.load(f"../src/images/battary_{self.charge}.png").convert_alpha()
        pygame.time.get_ticks()
        time_s = self.font.render(
            time.strftime(
                "%H:%M",
                time.gmtime(
                    pygame.time.get_ticks() / 1000 * timecost
                )
            ),
            True,
            [255, 255, 255]
        )
        if focus == MONITOR:
            image = pygame.transform.scale(ori_image, (80, 40))
            screen.blit(image, (5, 5))
            screen.blit(time_s, (15, 60))
        elif focus == OFFICE:
            image = pygame.transform.scale(ori_image, (50, 25))
            screen.blit(image, (294, 253))
            screen.blit(time_s, (341, 190))

class Button():
    def __init__(self, name, pos, image, width=None, height=None):
        self.name = name
        self.pos = pos
        self.ori_image = pygame.image.load(f"../src/images/{image}")
        self.width = width or self.ori_image.get_width()
        self.height = height or self.ori_image.get_height()

    def infocus(self, pos):
        if self.pos[0] < pos[0] and pos[0] < self.pos[0] + self.width and self.pos[1] < pos[1] and pos[1] < self.pos[1] + self.height:
            return True
        else:
            return False

    def draw(self):
        image = pygame.transform.scale(self.ori_image, (self.width, self.height))
        screen.blit(image, self.pos)

class Toogle_button():
    def __init__(self, name, pos, image1, image2=None, width=None, height=None):
        self.name = name
        self.pos = pos
        self.ori_image1 = pygame.image.load(f"../src/images/{image1}")
        self.ori_image2 = pygame.image.load(f"../src/images/{image2 or image1}")
        self.width = width or self.ori_image1.get_width()
        self.height = height or self.ori_image1.get_height()
        self.value = False

    def infocus(self, pos):
        if self.pos[0] < pos[0] and pos[0] < self.pos[0] + self.width and self.pos[1] < pos[1] and pos[1] < self.pos[1] + self.height:
            return True
        else:
            return False

    def draw(self):
        if self.value:
            image = pygame.transform.scale(self.ori_image1, (self.width, self.height))
        else:
            image = pygame.transform.scale(self.ori_image2, (self.width, self.height))
        screen.blit(image, self.pos)

    def switch(self):
        self.value = not self.value

class Office():
    def __init__(self):
        self.image = pygame.image.load("../src/images/office.png")
        self.energy = 100
        self.monitor = Monitor()
        self.focus = OFFICE
        self.sound = pygame.mixer.Sound("../src/music/sound_office.wav")

    def draw(self):
        if self.focus == OFFICE:
            self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
            screen.blit(self.image, (0, 0))
            pygame.mixer.stop()
            self.sound.play(-1)
        elif self.focus == MONITOR:
            self.monitor.draw()


class Map():
    def __init__(self):
        self.ori_image = pygame.image.load("../src/images/map1.png")

    def draw(self):
        self.image = pygame.transform.scale(self.ori_image, (400, 350))
        screen.blit(self.image, (screen_width - 450, screen_height - 350))

class Room():
    def __init__(self, image_path=""):
        self.ori_image = pygame.image.load(image_path)

    def draw(self):
        self.image = pygame.transform.scale(self.ori_image, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))

class Hall(Room):
    def __init__(self):
        super().__init__("../src/images/cam1.png")
        self.door_button = Toogle_button("door", [56, 437], "door_open.png", "door_close.png")

    def draw(self):
        super().draw()
        self.door_button.draw()

    def toogle_door(self):
        self.door_button.switch()

    '''
    def door_is_open(self):
        return not self.door_button.value
    '''

class Hall_east(Room):
    def __init__(self):
        super().__init__("../src/images/cam5,2.png")


class Workshop(Room):
    def __init__(self):
        super().__init__("../src/images/cam3.png")


class Storage(Room):
    def __init__(self):
        super().__init__("../src/images/cam4.png")

class Hall_1(Room):
    def __init__(self):
        super().__init__("../src/images/cam5,2.png")

class Factory(Room):
    def __init__(self):
        super().__init__("../src/images/cam6.png")


class Vent_room(Room):
    def __init__(self):
        super().__init__("../src/images/cam7.png")


class Vent_center(Room):
    def __init__(self):
        super().__init__("../src/images/cam8.png")


class Vent_east(Room):
    def __init__(self):
        super().__init__("../src/images/cam9.png")
        self.vent_button = Toogle_button("vent", [56, 437], "vent_open.png", "vent_close.png")

    def draw(self):
        super().draw()
        self.vent_button.draw()

    def toogle_vent(self):
        self.vent_button.switch()

    '''
    def vent_is_open(self):
        return not self.vent_button.value
    '''

class Animatronic():
    def __init__(self):
        self.map = []

class Fantom():
        pass

if __name__ == '__main__':
    pygame.init()
    (screen_width, screen_height) = (800, 600)
    screen = pygame.display.set_mode((screen_width, screen_height))

    game = Game()

    done = False
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                game.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos) #координаты


        game.flip()
        pygame.display.flip()  # бновляет вывод на экран

    pygame.quit()