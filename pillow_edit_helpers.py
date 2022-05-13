from PIL import Image, ImageOps
from PIL.ImageFilter import (CONTOUR)


# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image

# Resize the image
def resize_image(image):
    basewidth = 300
    img = Image.open(image)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    new_img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    return new_img

# Limit maximum value to 255
def get_max(value):
    if value > 255:
        return 255

    return int(value)


# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel


def get_sepia_pixel(red, green, blue, alpha):
    tRed = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue))
    tGreen = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
    tBlue = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))

    # Return sepia color
    return tRed, tGreen, tBlue, alpha


# Convert an image to sepia
def convert_sepia(image):
    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()

    # Convert each pixel to sepia
    for i in range(0, width, 1):
        for j in range(0, height, 1):
            p = get_pixel(image, i, j)
            pixels[i, j] = get_sepia_pixel(p[0], p[1], p[2], 255)

    # Return new image
    return new


#Sketchify the image
def sketchify_image(image):
    #Apply the blur filter
    new_img = image.filter(CONTOUR)

    return new_img

#Add a border to image
def add_border(image):
    new_img = ImageOps.expand(image, border=(10,50))

    return new_img
