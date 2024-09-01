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

import os
from PIL import Image

# Define source and destination directories
source_dir = 'path/to/source/directory'
destination_dir = 'path/to/destination/directory'

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Loop through all files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith('.jpg'):
        # Construct full file path
        jpg_path = os.path.join(source_dir, filename)
        
        # Open the .jpg file
        with Image.open(jpg_path) as img:
            # Convert and save as .png
            png_filename = os.path.splitext(filename)[0] + '.png'
            png_path = os.path.join(destination_dir, png_filename)
            img.save(png_path, 'PNG')

print("Conversion complete.")