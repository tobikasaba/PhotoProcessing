from image import Image
import numpy as np


# pylint: disable= line-too-long

def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount
    # factor is a value > 0; how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    # (x_pixels, y_pixels, num_channels)
    # The shape attribute of a NumPy array returns a tuple representing the dimensions of the array.
    x_pixels, y_pixels, num_channels = image.sobel_x_kernel.shape  # get x, y pixels of image,  # channels (R, G, B).
    # make an empty image so we don't actually modify the original one
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                   num_channels=num_channels)  # making a new array to copy values to!

    # this is the most intuitive way to do this (non-vectorised)
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_im.array[x, y, c] = image.array[x, y, c] * factor

    # vectorised version
    new_im.array = image.sobel_x_kernel * factor
    return new_im


def adjust_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.sobel_x_kernel.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                   num_channels=num_channels)  # making a new array to copy values to!

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.sobel_x_kernel[x, y, c] - mid) * factor + mid

    # vectorised version
    # new_im.array = (image.array - mid) * factor + mid

    return new_im


def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (i.e. kernel_size = 3 would be neighbours to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    x_pixels, y_pixels, num_channels = image.sobel_x_kernel.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                   num_channels=num_channels)  # making a new array to copy values to!

    neighbor_range = kernel_size // 2  # how many neighbours to one side we need to look at

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                # we are going to use a naive implementation of iterating through each neighbour and summing
                # there are faster implementations where you can use memoization,
                # but this is the most straightforward for a beginner to understand
                total = 0
                for x_i in range(max(0, x - neighbor_range), min(x_pixels - 1, x + neighbor_range) + 1):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels - 1, y + neighbor_range) + 1):
                        total += image.sobel_x_kernel[x_i, y_i, c]
                new_im.array[x, y, c] = total / (kernel_size ** 2)  # average
    return new_im


# note:
# the blur implemented above is a kernel of size n, where each value is 1/(n**2)
# for example, k=3 would be this kernel:
# [1/3 1/3 1/3]
# [1/3 1/3 1/3]
# [1/3 1/3 1/3]


def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simplicity this implementation, let's assume that the kernel is SQUARE,
    # for example, the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                   num_channels=num_channels)  # making a new array to copy values to!

    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2  # how many neighbours to one side we need to look at

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x - neighbor_range), min(x_pixels - 1, x + neighbor_range) + 1):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels - 1, y + neighbor_range) + 1):
                        # we need to find which value of the kernel this corresponds to
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_im.array[x, y, c] = total
    return new_im


def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                   num_channels=num_channels)  # making a new array to copy values to!
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image1.array[x, y, c] ** 2 + image2.array[x, y, c] ** 2) ** 0.5
    return new_im


if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')

    # # lets lighten the lake
    # brightened_im = brighten(lake, 1.7)
    # brightened_im.write_image("brightened lake.png")
    #
    # # darken the lake
    # darkened_im = brighten(lake, 0.3)
    # darkened_im.write_image("darkened lake.png")
    #
    # # increase the contrast for the lake
    # incr_contrast = adjust_contrast(lake, 2, 0.5)
    # incr_contrast.write_image("increased contrast.png")
    #
    # # decrease the contrast for the lake
    # decr_contrast = adjust_contrast(lake, 0.5, 0.5)
    # decr_contrast.write_image("decreased contrast.png")
    #
    # # blur using kernel 3
    # blur_3 = blur(city, 3)
    # blur_3.write_image('blur_k3.png')

    # # blur using kernel size of 15
    # blur_15 = blur(city, 15)
    # blur_15.write_image('blur_k15.png')

    # let's apply a sobel edge detection kernel on the x and y-axis
    sobel_x_kernel = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])
    sobel_y_kernel = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ])
    sobel_x = apply_kernel(city, sobel_x_kernel)
    sobel_x.write_image('edge_x.png')
    sobel_y = apply_kernel(city, sobel_y_kernel)
    sobel_y.write_image('edge_y.png')

    # let's combine these and make an edge detector!
    sobel_xy = combine_images(sobel_x, sobel_y)
    sobel_xy.write_image('edge_xy.png')
