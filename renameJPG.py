import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, 30)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import pygame, threading
from PIL import Image
# import tensorflow as tf

def addThread(threads_list, function, args):
    threads_list.append(threading.Thread(target=function, args=args))
    threads_list[-1].start()
    return [thread for thread in threads_list if thread.is_alive()]

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
    jpg_img.save(name := f'{SOURCE_DIR}{NAMED}{FOLDER}/{file_name}_{(file-1)%2 if second_page else file%2}.png')
    print('saved', name)
    return None

def saveCode(pyg_img, file_name):
    pil_string_image = pygame.image.tostring(pyg_img, "RGB", False)
    pil_image = Image.frombytes("RGB", (800,200), pil_string_image)
    pil_image.save(name := f'{SOURCE_DIR}{CODES}{FOLDER}/{file_name}.png')
    print('saved', name)
    return None

def highlightCode(codeX, codeY, rotate):
    if rotate: codeBox = pygame.Rect(min(PXL[0] - 200, max(0, codeX - 100)), min(PXL[1] - 800, max(0, codeY - 400)), 200, 800)
    else:      codeBox = pygame.Rect(min(PXL[0] - 800, max(0, codeX - 400)), min(PXL[1] - 200, max(0, codeY - 100)), 800, 200)
    codeScreen = pygame.Surface(DEFAULT_IMG, pygame.SRCALPHA, 32)
    codeScreen.fill((0, 0, 0, 50))
    codeBox_ = codeBox.scale_by(DEFAULT_IMG[0] / PXL[0])
    codeBox_.center = (codeBox.center[0] * DEFAULT_IMG[0] / PXL[0], codeBox.center[1] * DEFAULT_IMG[1] / PXL[1])
    thickness = 2
    pygame.draw.rect(codeScreen, (230, 230, 230, 0), codeBox_)
    pygame.draw.rect(codeScreen, (0, 0, 250, 160), codeBox_, thickness)
    # pygame.draw.line(codeScreen, (250, 0, 0, 100), (codeBox_.x+codeBox_.width/2, codeBox_.y+codeBox_.height/2-20),
    #                                                 (codeBox_.x+codeBox_.width/2, codeBox_.y+codeBox_.height/2+20), thickness)
    # pygame.draw.line(codeScreen, (250, 0, 0, 70), (codeBox_.x+codeBox_.width/2-30, codeBox_.y+codeBox_.height/2),
    #                                                 (codeBox_.x+codeBox_.width/2+30, codeBox_.y+codeBox_.height/2), thickness)
    return codeBox, codeScreen

def get_info_screen(WINres, file, file_name, Font, jpg_name):
    infoScreen = pygame.Surface((WINres[0] - 800, 200))
    infoScreen.fill((200, 200, 40))
    pygame.draw.rect(infoScreen, (250, 250, 250), (170, 155, 90, 30))
    infoScreen.blit(Font.render(f'File: {file}', True, (0, 0, 0)), (10, 155))
    infoScreen.blit(Font.render(f'Name: {file_name}', True, (0, 0, 0)), (105, 155))
    return infoScreen

def gradientRect(rect, color1, color2):
    bgscreen = pygame.Surface(rect, pygame.SRCALPHA, 32)
    bgscreen.fill(color2)
    gradient = pygame.Surface(rect, pygame.SRCALPHA, 32)
    for row in range(rect[1]):
        pygame.draw.line(gradient, 
                         (color1[0], color1[1], color1[2], int((1-row/rect[1])*255)), (0, row), (rect[0], row))
    bgscreen.blit(gradient, (0, 0))
    return bgscreen


record = True
second_page = 0

PXL, WIN = (4032, 2268), (1800, 1050)
DIS = (WIN[0], WIN[1] - 200)
DEFAULT_IMG = (min(DIS[0], int(PXL[0]/(PXL[1]/DIS[1]))), min(DIS[1], int(PXL[1]/(PXL[0]/DIS[0]))))
DEFAULT_DIS = (DEFAULT_IMG[0], DEFAULT_IMG[1] + 200)
DEFAULT_POS = (max(0, (WIN[0] - DEFAULT_IMG[0])//2), max(0, (WIN[1] - DEFAULT_DIS[1])//2))
bgcolor = (200, 200, 40)
fillcolor = (150, 100, 10)

pygame.init()
screen = pygame.display.set_mode(WIN)
screen.fill(fillcolor)
pygame.draw.rect(screen, (200, 200, 200), (800, 0, WIN[0]-800, 200))
Font = pygame.font.Font('data/fonts/Manrope-VariableFont_wght.ttf', 22)

SOURCE_DIR = 'data/surveys'
UNNAMED = '/unnamedjpg'
NAMED = '/namedpng'
CODES = '/codespng'
FOLDER = '/1png'

os.makedirs(SOURCE_DIR + NAMED + FOLDER, exist_ok=True)
os.makedirs(SOURCE_DIR + CODES + FOLDER, exist_ok=True)

print(jpg_list := os.listdir(SOURCE_DIR + UNNAMED + '/un1jpg'))
save_threads = []

file = second_page
file_prefix = 'H'
file_name = file_prefix
typing = True
jpg_name = jpg_list[file]
jpg_img = Image.open(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
pyg_full_img = pygame.image.load(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
if(pyg_full_img.get_size() != PXL):
    jpg_img = jpg_img.rotate(90, expand=1)
    pyg_full_img = pygame.transform.rotate(pyg_full_img, 90)
pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)

codeX, codeY = 0, 0
codeBox, codeScreen = highlightCode(codeX, codeY, 0)
code_img = pyg_full_img.subsurface(codeBox)
screen.blit(code_img, (0, 0))
# if DEFAULT_POS[0] != 0: screen.blit(gradient := gradientRect((DEFAULT_POS[0], DEFAULT_IMG[1]), bgcolor, fillcolor), 
#                                     (WIN[0]-DEFAULT_POS[0], 200))
# elif DEFAULT_POS[1] != 0: screen.blit(gradient := gradientRect((WIN[0], DEFAULT_POS[1]), bgcolor, fillcolor), 
#                                       (0, 200))
screen.blit(gradient := gradientRect((WIN[0], WIN[1]-200), bgcolor, fillcolor), 
                                    (0, 200))

pygame.display.update()

running, frame = True, 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if pos[1] > 200: 
                codeX, codeY = (int((pos[0] - DEFAULT_POS[0]) * PXL[0] / DEFAULT_IMG[0]), 
                                int((pos[1] - DEFAULT_POS[1] - 200) * PXL[1] / DEFAULT_IMG[1]))
            elif pos[0] > 800: typing = True
            else: typing = False
            codeScreen.fill((0, 0, 0, 50))
            if file%2 == second_page:
                codeBox, codeScreen = highlightCode(codeX, codeY, 0)
                code_img = pyg_full_img.subsurface(codeBox)
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                typing = True
                if record: save_threads = addThread(save_threads, saveImage, (jpg_img, file_name, file, second_page))
                if file%2 == second_page and record: save_threads = addThread(save_threads, saveCode, (code_img, file_name))
                file += 1
                if file == len(jpg_list):
                    running = False
                    break
                jpg_name = jpg_list[file]
                jpg_img = Image.open(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
                pyg_full_img = pygame.image.load(f'{SOURCE_DIR}{UNNAMED}/un1jpg/{jpg_name}')
                if(pyg_full_img.get_size() != PXL):
                    jpg_img = jpg_img.rotate(90, expand=1)
                    pyg_full_img = pygame.transform.rotate(pyg_full_img, 90)
                pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)
                codeX, codeY = 0, 0
                codeScreen.fill((0, 0, 0, 50))
                if file%2 == second_page:
                    file_name = file_prefix
                    codeBox, codeScreen = highlightCode(codeX, codeY, 0)
                    code_img = pyg_full_img.subsurface(codeBox)
            
            elif event.key == pygame.K_r:
                jpg_img = jpg_img.rotate(180)
                pyg_full_img = pygame.transform.rotate(pyg_full_img, 180)
                pyg_img = pygame.transform.scale(pyg_full_img, DEFAULT_IMG)
                codeX, codeY = 0, 0
                if file%2 == second_page:
                    codeBox, codeScreen = highlightCode(codeX, codeY, 0)
                    code_img = pyg_full_img.subsurface(codeBox)
            
            elif event.key == pygame.K_UP:
                codeY -= 1
                codeScreen.fill((0, 0, 0, 50))
                if file%2 == second_page:
                    codeBox, codeScreen = highlightCode(codeX, codeY, 0)
                    code_img = pyg_full_img.subsurface(codeBox)
            elif event.key == pygame.K_DOWN:
                codeY += 1
                codeScreen.fill((0, 0, 0, 50))
                if file%2 == second_page:
                    codeBox, codeScreen = highlightCode(codeX, codeY, 0)
                    code_img = pyg_full_img.subsurface(codeBox)
            elif event.key == pygame.K_LEFT:
                codeX -= 1
                codeScreen.fill((0, 0, 0, 50))
                if file%2 == second_page:
                    codeBox, codeScreen = highlightCode(codeX, codeY, 0)
                    code_img = pyg_full_img.subsurface(codeBox)
            elif event.key == pygame.K_RIGHT:
                codeX += 1
                codeScreen.fill((0, 0, 0, 50))
                if file%2 == second_page:
                    codeBox, codeScreen = highlightCode(codeX, codeY, 0)
                    code_img = pyg_full_img.subsurface(codeBox)
            
            elif typing and file%2 == second_page:
                if event.key == pygame.K_BACKSPACE: file_name = file_name[0:-1]
                else: file_name += event.unicode
    
    # screen.fill(bgcolor)
    
    # pygame.draw.rect(screen, (200, 200, 200), (800, 0, WIN[0]-800, 200))
    screen.blit(code_img, (0, 0))
    screen.blit(pyg_img, (DEFAULT_POS[0], DEFAULT_POS[1] + 200))
    screen.blit(codeScreen, (DEFAULT_POS[0], DEFAULT_POS[1] + 200))
    # screen.blit(Font.render('test', True, (0, 0, 0)), (1000, 0))
    screen.blit(infoScreen := get_info_screen(WIN, file, file_name, Font, jpg_list[file]), (800, 0))
    # screen.blit(gradient, (0, 200))
    # screen.blit(gradient, (WIN[0]-DEFAULT_POS[0], 200))
    pygame.display.update()

pygame.quit()
join_threads([save_threads])