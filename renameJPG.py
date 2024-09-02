import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, 30)

import pygame, threading
from PIL import Image

def saveImage(jpg_img, file_name, file, second_page):
    jpg_img.save(f'{SOURCE_DIR}{NAMED}/{FOLDER}/{file_name}_{file%2 if second_page else (file-1)%2}.png')
    return None

PXL, WIN = (4032, 2268), (2560, 1370)
DIS = (PXL[0], int(PXL[1] * 1.1))
DEFAULT_DIS = (min(WIN[0], int(DIS[0]/(DIS[1]/WIN[1]))), min(WIN[1], int(DIS[1]/(DIS[0]/WIN[0]))))
DEFAULT_POS = (max(0, (WIN[0] - DEFAULT_DIS[0])//2), max(0, (WIN[1] - DEFAULT_DIS[1])//2))
DEFAULT_IMG = (int(DEFAULT_DIS[0]), int(DEFAULT_DIS[1] * 10/11))

pygame.init()
screen = pygame.display.set_mode(WIN)

SOURCE_DIR = 'data/surveys'
UNNAMED = '/unnamedjpg'
NAMED = '/namedpng'
FOLDER = '/1png'

os.makedirs(SOURCE_DIR + NAMED + FOLDER, exist_ok=True)

print(jpg_list := os.listdir(SOURCE_DIR + UNNAMED + '/un1jpg'))
save_threads = []

second_page = True
file = 0
file_name = 'H1E'
jpg_name = jpg_list[file]
jpg_img = Image.open(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
pyg_full_img = pygame.image.load(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)

running, frame = True, 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            for thread in save_threads:
                thread.join()
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                save_threads.append(threading.Thread(target=saveImage, args=(jpg_img, file_name, file, second_page)))
                save_threads[-1].start()
                file += 1
                jpg_name = jpg_list[file]
                jpg_img = Image.open(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
                pyg_full_img = pygame.image.load(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
                pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)

            elif event.key == pygame.K_e:
                pyg_full_img = pygame.transform.rotate(pyg_full_img, -90)
                pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)
                jpg_img = jpg_img.rotate(-90, expand=1)
            elif event.key == pygame.K_q:
                pyg_full_img = pygame.transform.rotate(pyg_full_img, 90)
                pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)
                jpg_img = jpg_img.rotate(90, expand=1)
    
    screen.fill((0, 0, 0))
    
    update1 = pygame.draw.rect(screen, (200, 200, 200), (DEFAULT_POS[0], DEFAULT_POS[1], DEFAULT_DIS[0], DEFAULT_DIS[1]//11))
    update2 = screen.blit(pyg_img, (DEFAULT_POS[0], DEFAULT_POS[1] + DEFAULT_DIS[1]//11))
    pygame.display.update((update1, update2))
    
    frame += 1
