import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, 30)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import pygame, threading
from PIL import Image

def join_threads(threads_list):
    for threads in threads_list:
        for thread in threads:
            thread.join()
    return None

def getNextFile(file, second_page):
    if second_page:
        file += ((file-1)%2) * 3 - (file%2)
        return file
    return file+1

def saveImage(jpg_img, file_name, file, second_page):
    jpg_img.save(name := f'{SOURCE_DIR}{NAMED}{FOLDER}/{file_name}_{file%2 if second_page else (file-1)%2}.png')
    print('saved', name)
    return None

def highlightCode(codeX, codeY):
    codeBox = pygame.Rect(min(PXL[0] - 800, max(0, codeX - 400)), min(PXL[1] - 200, max(0, codeY - 100)), 800, 200)
    codeScreen = pygame.Surface(DEFAULT_IMG, pygame.SRCALPHA, 32)
    codeScreen.fill((0, 0, 0, 50))
    codeBox_ = codeBox.scale_by(DEFAULT_IMG[0] / PXL[0])
    codeBox_.center = (codeBox.center[0] * DEFAULT_IMG[0] / PXL[0], codeBox.center[1] * DEFAULT_IMG[1] / PXL[1])
    thickness = 2
    pygame.draw.rect(codeScreen, (250, 0, 0, 160), codeBox_)
    pygame.draw.rect(codeScreen, (230, 230, 230, 0), (codeBox_.x+thickness, codeBox_.y+thickness,
                                                      codeBox_.width-thickness*2, codeBox_.height-thickness*2))
    return codeBox, codeScreen


record = True
second_page = 0

PXL, WIN = (4032, 2268), (1800, 1050)
DIS = (WIN[0], WIN[1] - 200)
DEFAULT_IMG = (min(DIS[0], int(PXL[0]/(PXL[1]/DIS[1]))), min(DIS[1], int(PXL[1]/(PXL[0]/DIS[0]))))
DEFAULT_DIS = (DEFAULT_IMG[0], DEFAULT_IMG[1] + 200)
DEFAULT_POS = (max(0, (WIN[0] - DEFAULT_IMG[0])//2), max(0, (WIN[1] - DEFAULT_DIS[1])//2))

pygame.init()
screen = pygame.display.set_mode(WIN)
pygame.draw.rect(screen, (200, 200, 200), (800, 0, WIN[0]-800, 200))

SOURCE_DIR = 'data/surveys'
UNNAMED = '/unnamedjpg'
NAMED = '/namedpng'
FOLDER = '/1png'

os.makedirs(SOURCE_DIR + NAMED + FOLDER, exist_ok=True)

print(jpg_list := os.listdir(SOURCE_DIR + UNNAMED + '/un1jpg'))
save_threads = []

file = second_page
file_name = 'H1E'
jpg_name = jpg_list[file]
jpg_img = Image.open(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
pyg_full_img = pygame.image.load(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
if(pyg_full_img.get_size() != PXL):
    jpg_img = jpg_img.rotate(90)
    pyg_full_img = pygame.transform.rotate(pyg_full_img, 90)
pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)

codeX, codeY = 0, 0
codeBox = pygame.Rect(min(PXL[0] - 800, max(0, codeX - 400)), min(PXL[1] - 200, max(0, codeY - 100)), 800, 200)
code_img = pyg_full_img.subsurface(codeBox)
codeScreen = pygame.Surface(DEFAULT_IMG, pygame.SRCALPHA, 32)
codeScreen.fill((0, 0, 0, 50))
codeBox_ = codeBox.scale_by(DEFAULT_IMG[0] / PXL[0])
codeBox_.center = (codeBox.center[0] * DEFAULT_IMG[0] / PXL[0], codeBox.center[1] * DEFAULT_IMG[1] / PXL[1])
pygame.draw.rect(codeScreen, (230, 230, 230, 0), codeBox_)
screen.blit(codeScreen, (DEFAULT_POS[0], DEFAULT_POS[1] + 200))
screen.blit(code_img, (0, 0))
pygame.display.update()

running, frame = True, 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            codeX, codeY = (int((pos[0] - DEFAULT_POS[0]) * PXL[0] / DEFAULT_IMG[0]), int((pos[1] - DEFAULT_POS[1] - 200) * PXL[1] / DEFAULT_IMG[1]))
            codeScreen.fill((0, 0, 0, 50))
            if file%2 == second_page:
                codeBox, codeScreen = highlightCode(codeX, codeY)
                code_img = pyg_full_img.subsurface(codeBox)
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                save_threads.append(threading.Thread(target=saveImage, args=(jpg_img, file_name, file, second_page)))
                save_threads[-1].start()
                file += 1
                jpg_name = jpg_list[file]
                jpg_img = Image.open(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
                pyg_full_img = pygame.image.load(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
                if(pyg_full_img.get_size() != PXL):
                    jpg_img = jpg_img.rotate(90)
                    pyg_full_img = pygame.transform.rotate(pyg_full_img, 90)
                pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)
                codeX, codeY = 0, 0
                codeScreen.fill((0, 0, 0, 50))
                if file%2 == second_page:
                    codeBox, codeScreen = highlightCode(codeX, codeY)
                    code_img = pyg_full_img.subsurface(codeBox)

            elif event.key == pygame.K_r:
                jpg_img = jpg_img.rotate(180)
                pyg_full_img = pygame.transform.rotate(pyg_full_img, 180)
                pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)
                codeX, codeY = 0, 0
                if file%2 == second_page:
                    codeBox, codeScreen = highlightCode(codeX, codeY)
                    code_img = pyg_full_img.subsurface(codeBox)
    
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (200, 200, 200), (800, 0, WIN[0]-800, 200))
    screen.blit(code_img, (0, 0))
    screen.blit(pyg_img, (DEFAULT_POS[0], DEFAULT_POS[1] + 200))
    screen.blit(codeScreen, (DEFAULT_POS[0], DEFAULT_POS[1] + 200))
    pygame.display.update()

pygame.quit()
join_threads([save_threads])