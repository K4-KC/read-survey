import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, 30)

import copy, pickle
import pygame

# images flipping

# (4032, 2268)
def get_images(directory, EK, limit):
    images = []
    names = [f'{i//2}{EK}{i%2}' for i in range(0, limit*2)]
    for image in names:
        try:
            img = pygame.image.load(f'{directory}/{image}.jpg')
            images.append(img)
        except:
            pass
    return images

def drawPoint(surface, point, zoom):
    pygame.draw.circle(surface, (255, 0, 0), [point[0]*zoom, point[1]*zoom], 25)
    pygame.draw.circle(surface, (0, 0, 0, 0), [point[0]*zoom, point[1]*zoom], 23)
    pygame.draw.line(surface, (255, 0, 0), [point[0]*zoom-35, point[1]*zoom], [point[0]*zoom+35, point[1]*zoom], 1)
    pygame.draw.line(surface, (255, 0, 0), [point[0]*zoom, point[1]*zoom-35], [point[0]*zoom, point[1]*zoom+35], 1)
    return surface

# load list from file
def loadList(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except:
        return None

def dumpList(list, filename):
    with open(filename, 'wb') as file:
        pickle.dump(list, file)
    return None

# [[[775.0, 456.0], [1050.0, 455.0], [1166.0, 454.0], [1430.0, 453.0], [1689.0, 444.0], [1938.0, 419.0], [817.0, 1912.0], [1034.0, 1811.0], [1120.0, 1794.0], [1408.0, 1821.0], [1676.0, 1829.0], [1896.0, 1956.0]], [], [[731.0, 349.0], [1038.0, 351.0], 
# [1168.0, 352.0], [1466.0, 356.0], [1765.0, 358.0], [2064.0, 350.0], [736.0, 1992.0], [982.0, 1881.0], [1079.0, 1865.0], [1406.0, 1903.0], [1721.0, 1910.0], [1992.0, 2041.0]], []]

points_list = loadList('data/text files/points_E0.txt')
print(points_list)

points_list = points_list if points_list else []
points_list = []
current_img = len(points_list)
print(current_img)

images = get_images('data/surveys/E', 'E', 300)
print(len(images), 'images loaded')

pygame.init()

PXL, WIN = (4032, 2268), (2560, 1370)
DEFAULT_ZOOM, DEFAULT_POS = WIN[1]/PXL[1], [62, 0]
zoom, print_pos = DEFAULT_ZOOM, copy.deepcopy(DEFAULT_POS)
zoomed, NEW_ZOOM = False, 3

screen = pygame.display.set_mode(WIN)
screen_points = pygame.Surface(PXL, pygame.SRCALPHA, 32)
screen_points_out_zoom = pygame.transform.scale(screen_points, (PXL[0]*zoom, PXL[1]*zoom))
screen_points_zoom = pygame.transform.scale(screen_points, (PXL[0]*NEW_ZOOM, PXL[1]*NEW_ZOOM))

image = pygame.transform.scale(images[current_img], (PXL[0]*zoom, PXL[1]*zoom))
image_zoom = pygame.transform.scale(images[current_img], (PXL[0]*NEW_ZOOM, PXL[1]*NEW_ZOOM))

points = []
running, frame = True, 0
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if event.button == 1:
                point = [(pos[0] - print_pos[0])//zoom, (pos[1] - print_pos[1])//zoom]
                print(point)
                points.append(point)
                # dumpList(points_list, 'data/text files/points_E0.txt')
                # pygame.draw.circle(screen_points, (255, 0, 0), point, 5)
                # pygame.draw.circle(screen_points_out_zoom, (255, 0, 0), [point[0]*DEFAULT_ZOOM, point[1]*DEFAULT_ZOOM], 5)
                screen_points_zoom = drawPoint(screen_points_zoom, point, NEW_ZOOM)
                screen_points_out_zoom = drawPoint(screen_points_out_zoom, point, DEFAULT_ZOOM)
                # screen_points_out_zoom = pygame.transform.scale(screen_points, (PXL[0]*zoom, PXL[1]*zoom))
                # screen_points_zoom = pygame.transform.scale(screen_points, (PXL[0]*NEW_ZOOM, PXL[1]*NEW_ZOOM))
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoomed = True
                print_pos[0] = pos[0] - (pos[0] - print_pos[0]) * NEW_ZOOM / zoom
                print_pos[1] = pos[1] - (pos[1] - print_pos[1]) * NEW_ZOOM / zoom
                zoom = NEW_ZOOM
            else:
                zoomed = False
                print_pos = copy.deepcopy(DEFAULT_POS)
                zoom = DEFAULT_ZOOM
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                current_img += 1
                if current_img >= len(images):
                    running = False
                else:
                    image = pygame.transform.scale(images[current_img], (PXL[0]*zoom, PXL[1]*zoom))
                    image_zoom = pygame.transform.scale(images[current_img], (PXL[0]*NEW_ZOOM, PXL[1]*NEW_ZOOM))
                    screen_points = pygame.Surface(PXL, pygame.SRCALPHA, 32)
                    screen_points_out_zoom = pygame.transform.scale(screen_points, (PXL[0]*zoom, PXL[1]*zoom))
                    screen_points_zoom = pygame.transform.scale(screen_points, (PXL[0]*NEW_ZOOM, PXL[1]*NEW_ZOOM))
                    points_list.append(points)
                    dumpList(points_list, 'data/text files/points_E0.txt')
                    points = []
            elif event.key == pygame.K_RIGHT:
                images[current_img] = pygame.transform.rotate(images[current_img], -90)
                image = pygame.transform.scale(images[current_img], (PXL[0]*zoom, PXL[1]*zoom))
                image_zoom = pygame.transform.scale(images[current_img], (PXL[0]*NEW_ZOOM, PXL[1]*NEW_ZOOM))         

    
    # screen.fill((255, 255, 255))
    screen.fill((0, 0, 0))
    # screen_points.fill((0, 0, 0, 0))
    
    screen.blit(image_zoom if zoomed else image, print_pos)
    screen.blit(screen_points_zoom if zoomed else screen_points_out_zoom, print_pos)
    
    pygame.display.flip()
    # print(frame)
    frame += 1
    
pygame.quit()