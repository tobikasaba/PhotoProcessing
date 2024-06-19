from image import Image
import numpy as np


# pylint: disable= line-too-long

def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount
    # factor is a value > 0; how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    # (x_pixels, y_pixels, num_channels)
    # The shape attribute of a NumPy array returns a tuple representing the dimensions of the array.
    x_pixels, y_pixels, num_channels = image.array.shape  # get x, y pixels of image,  # channels (R, G, B).
    # make an empty image so we don't actually modify the original one
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                   num_channels=num_channels)  # making a new array to copy values to!

    # this is the most intuitive way to do this (non-vectorised)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = image.array[x, y, c] * factor

    return new_im


def adjust_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    pass


def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    pass


def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    pass


def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    pass


if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')

    # lets lighten the lake
    brightened_im = brighten(lake, 1.7)
    brightened_im.write_image("brightened lake.png")

    # darken the lake
    darkened_im = brighten(lake, 0.3)
    darkened_im.write_image("darkened lake.png")
