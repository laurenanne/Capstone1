from PIL import Image


def image_resize(image):
    image = Image.open(image)
    new_image = image.thumbnail((200, 200))

    return (new_image)
