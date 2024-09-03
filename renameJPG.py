import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, 30)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import pygame, threading
from PIL import Image
# import tensorflow as tf

def saveImage(jpg_img, file_name, file, second_page):
    jpg_img.save(f'{SOURCE_DIR}{NAMED}/{FOLDER}/{file_name}_{file%2 if second_page else (file-1)%2}.png')
    return None

def join_threads(threads_list):
    for threads in threads_list:
        for thread in threads:
            thread.join()
    return None

record = False

PXL, WIN = (4032, 2268), (1800, 1050)
DIS = (WIN[0], WIN[1] - 200)
DEFAULT_IMG = (min(DIS[0], int(PXL[0]/(PXL[1]/DIS[1]))), min(DIS[1], int(PXL[1]/(PXL[0]/DIS[0]))))
DEFAULT_DIS = (DEFAULT_IMG[0], DEFAULT_IMG[1] + 200)
DEFAULT_POS = (max(0, (WIN[0] - DEFAULT_IMG[0])//2), max(0, (WIN[1] - DEFAULT_DIS[1])//2))
print(DIS)
print(DEFAULT_IMG)
print(DEFAULT_DIS)
print(DEFAULT_POS)

pygame.init()
screen = pygame.display.set_mode(WIN)
update1 = pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIN[0], 200))
pygame.display.update((update1))

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
            join_threads([save_threads])
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if record:
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
    
    update2 = pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIN[0], 200))
    update1 = screen.blit(pyg_img, (DEFAULT_POS[0], DEFAULT_POS[1] + 200))
    pygame.display.update((update1, update2))
    
    frame += 1
