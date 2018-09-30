"""Functions used to clean images of train tickets. The cleaning process
essentially entails grayscaling the image and getting rid of any unwanted
artifacts that prevent optical character recognition routines from extracting
important text from the image."""

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

MAX_COLOR_VALUE = 255
RED_COLOR_THRESHOLD = 180
GREYSCALE_THRESHOLD = 230

train_ticket_location = 'test_images/glasgow_to_lnd_euston.jpg'


def clean_train_ticket_image(
    train_ticket_filepath,
    greyscale_threshold=GREYSCALE_THRESHOLD,
):
    train_ticket_image = cv.imread(train_ticket_filepath)
    ticket_image_no_dom_color = remove_dominant_color(train_ticket_image)
    greyscale_ticket_image = cv.cvtColor(ticket_image_no_dom_color,
                                         cv.COLOR_BGR2GRAY)
    binarized_ticket_image = cv.threshold(greyscale_ticket_image,
                                          greyscale_threshold,
                                          greyscale_threshold,
                                          cv.THRESH_BINARY)
    return binarized_ticket_image


def remove_dominant_color(image):
    blue, green, red = cv.split(image)
    red_total, blue_total, green_total = red.sum(), blue.sum(), green.sum()

    if red_is_the_dominant_color(blue_total, green_total, red_total):
        return remove_red_from_image(blue, green, red)
    elif blue_is_the_dominant_color(blue_total, green_total, red_total):
        return remove_blue_from_image(blue, green, red)


def red_is_the_dominant_color(blue_sum, green_sum, red_sum):
    return red_sum > blue_sum and red_sum > green_sum


def blue_is_the_dominant_color(blue_sum, green_sum, red_sum):
    return blue_sum > red_sum and blue_sum > green_sum


def remove_red_from_image(blue_channel, green_channel, red_channel):
    mask = np.where(red_channel > RED_COLOR_THRESHOLD)

    # Make all pixels white where red was above the threshold
    red_channel[mask] = MAX_COLOR_VALUE
    blue_channel[mask] = MAX_COLOR_VALUE
    green_channel[mask] = MAX_COLOR_VALUE

    # Combine the colour channels into a single image
    return cv.merge([blue_channel, green_channel, red_channel])


def remove_blue_from_image(blue_channel, green_channel, red_channel):
    pass


img = clean_train_ticket_image(train_ticket_location)
plt.imshow(img[1])
