import numpy as np
import time


def convert_colors(image_path, new_value, verbose=False, save_file=False):

    # I know it's bad form to have imports in your functions, but I didn't want
    # to install scipy and plt on my raspberry pi
    from scipy import misc
    from matplotlib import pyplot as plt
    arr = misc.imread(image_path)
    for i, row in enumerate(arr):
        for j, pixel in enumerate(row):
            if pixel[3] > 0:
                arr[i, j] = new_value

    if verbose:
        plt.imshow(arr, interpolation='nearest')
    if save_file:
        misc.imsave(save_file, arr)


def fade_colors(pi1, old_colors, new_colors, rgb_gpio):
    deltas = new_colors - old_colors
    max_d = np.max(np.absolute(deltas))
    increments = deltas / max_d
    for i in range(max_d):
        old_colors = old_colors + increments
        # turn negatives into 0
        old_colors = (old_colors + np.absolute(old_colors))/2
        update_strip(pi1, old_colors, rgb_gpio)
        time.sleep(.01)


def update_strip(pi1, new_colors, rgb_gpio):
    pi1.set_PWM_dutycycle(rgb_gpio[0], new_colors[0])
    pi1.set_PWM_dutycycle(rgb_gpio[1], new_colors[1])
    pi1.set_PWM_dutycycle(rgb_gpio[2], new_colors[2])

if __name__ == '__main__':

    convert_colors('static/new_window_old.png', [34, 228, 144, 255],
                   save_file='static/new_window.png')
