from scipy import misc
from matplotlib import pyplot as plt

def convert_colors(image_path, new_value, verbose=False, save_file=False):
    arr = misc.imread(image_path)
    for i, row in enumerate(arr):
        for j, pixel in enumerate(row):
            if pixel[3] > 0:
                arr[i,j] = new_value

    if verbose:
        plt.imshow(arr, interpolation='nearest')
    if save_file:
        misc.imsave(save_file, arr)

if __name__ == '__main__':

    convert_colors('static/new_window_old.png', [34, 228, 144, 255], save_file='static/new_window.png')
