import os
from PIL import Image


# Code used to convert images to gif and change their sizes for gameplay
directory = "./assets"
backup_path = "./assets/backup"
for file in os.listdir(directory):
    if file.endswith((".png", ".jpg", ".jpeg")):
        image_name, ext = os.path.splitext(file)
        new_image_name = f"{image_name}.gif"
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_image_name)
        os.rename(old_path, new_path)
        print(f"Extension changed: {file} -> {new_image_name}")

for file in os.listdir(directory):
    if file == "laser.gif":
        print(f"Processing: {file}")
        image = Image.open(os.path.join(directory, file))
        image.save(os.path.join(backup_path, file))
        image = image.rotate(180)
        image.save(os.path.join(directory, file))
