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