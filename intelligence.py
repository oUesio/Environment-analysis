from matplotlib import pyplot
from numpy import *

def find_red_pixels(*args,**kwargs):
    """
    Finds the red pixels in an image and creates a new image changing red pixels to white and everything else black

    Args:
        *args: File name of the image
        **kwargs: Upper and lower theshold of the rgb values

    Returns:
        array: Binary image of the new image
    """
    rgb_img = pyplot.imread('data/' + str(args[0]))
    rgb_img = rgb_img * 255

    for row_pos in range(len(rgb_img)):
        for col_pos in range (len(rgb_img[row_pos])):
            if rgb_img[row_pos][col_pos][0] > kwargs[list(kwargs.keys())[0]] and rgb_img[row_pos][col_pos][1] < kwargs[list(kwargs.keys())[1]] and rgb_img[row_pos][col_pos][2] < kwargs[list(kwargs.keys())[1]]: #checks if pixel is red
                rgb_img[row_pos][col_pos] = [1, 1, 1, 1]
            else:
                rgb_img[row_pos][col_pos] = [0, 0, 0, 1]      
    pyplot.imsave('map-red-pixels.jpg', rgb_img)
    return rgb_img

def find_cyan_pixels(*args,**kwargs):
    """
    Finds the cyan pixels in an image and creates a new image changing cyan pixels to white and everything else black

    Args:
        *args: File name of the image
        **kwargs: Upper and lower theshold of the rgb values

    Returns:
        array: Binary image of the new image
    """
    rgb_img = pyplot.imread('data/' + str(args[0]))
    rgb_img = rgb_img * 255

    for row_pos in range(len(rgb_img)):
        for col_pos in range (len(rgb_img[row_pos])):
            if rgb_img[row_pos][col_pos][0] < kwargs[list(kwargs.keys())[0]] and rgb_img[row_pos][col_pos][1] > kwargs[list(kwargs.keys())[1]] and rgb_img[row_pos][col_pos][2] > kwargs[list(kwargs.keys())[1]]: #checks if pixel is cyan
                rgb_img[row_pos][col_pos] = [1, 1, 1, 1]
            else:
                rgb_img[row_pos][col_pos] = [0, 0, 0, 1]      
    pyplot.imsave('map-cyan-pixels.jpg', rgb_img)
    return rgb_img


def detect_connected_components(*args,**kwargs):
    """
    Detects the connected components of the binary image created by find_red_pixels and writes into a text file. Implements a circular queue to 
    store the positions of the white pixels.

    Args:
        *args: Binary image of the red pixels image

    Returns:
        array: Array of elements visited
    """
    connected = []
    img = pyplot.imread(args[0])
    q = empty((100,), dtype=list)
    front_pointer = 0
    back_pointer = 0
    visit = zeros((len(img), len(img[0])), dtype=int)
    surrounding = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]
    
    for row_pos in range (len(img)):
        for col_pos in range (len(img[row_pos])):
            if min(list(img[row_pos][col_pos])) > 210 and visit[row_pos][col_pos] == 0:
                count = 0
                visit[row_pos][col_pos] = 1
                q[back_pointer] = [row_pos, col_pos]
                back_pointer += 1 #increments when new positions are added
                if back_pointer > 99: #returns to start of the array when pointer exceeds the length of the array
                    back_pointer = 0
                while any(q):
                    count += 1
                    coords = q[front_pointer]
                    q[front_pointer] = None
                    front_pointer += 1 #increments when positions get removed
                    if front_pointer > 99:
                        front_pointer = 0
                    for s in surrounding:
                        try:
                            if min(list(img[coords[0]+s[0]][coords[1]+s[1]])) > 210 and visit[coords[0]+s[0]][coords[1]+s[1]] == 0:
                                visit[coords[0]+s[0]][coords[1]+s[1]] = 1
                                q[back_pointer] = [coords[0]+s[0], coords[1]+s[1]]
                                back_pointer += 1
                                if back_pointer > 99:
                                    back_pointer = 0
                        except:
                            pass
                connected.append(count)
    length = len(connected)
    with open('cc-output-2a.txt', 'w') as f:
        for x in range (length):
            f.write('Connected Component {num}, number of pixels = {pixels}\n'.format(num=x+1, pixels=connected[x]))
        f.write('Total number of connected components = '+str(length))
    return visit

def detect_connected_components_sorted(*args,**kwargs):
    """
    Sorts connected components in descending order by the number of pixels and writes into a text file.

    Args:
        *args: Array of elements visited from detect_connected_components
    """
    connected = []
    img = args[0]
    q = []
    surrounding = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]
    visit = zeros((len(img), len(img[0])), dtype=int)
    for row_pos in range (len(img)):
        for col_pos in range (len(img[row_pos])):
            if img[row_pos][col_pos] == 1 and visit[row_pos][col_pos] == 0:
                count = 0
                visit[row_pos][col_pos] = 1
                q.append([row_pos, col_pos])
                while len(q) != 0:
                    count += 1
                    coords = q.pop()
                    for s in surrounding:
                        try:
                            if img[coords[0]+s[0]][coords[1]+s[1]] == 1 and visit[coords[0]+s[0]][coords[1]+s[1]] == 0:
                                visit[coords[0]+s[0]][coords[1]+s[1]] = 1
                                q.append([coords[0]+s[0], coords[1]+s[1]])
                        except:
                            pass
                connected.append(count)
    length = len(connected)
    new_con = [[pos+1, connected[pos]] for pos in range (length)]
    swap = False
    for x in range(length-1):
        for y in range(0, length-1-x):
            if new_con[y][1] < new_con[y+1][1]:
                swap = True
                new_con[y], new_con[y+1] = new_con[y+1], new_con[y]
        if not swap:
            break
    with open('cc-output-2b.txt', 'w') as f:
        for x in new_con:
            f.write('Connected Component {num}, number of pixels = {pixels}\n'.format(num=x[0], pixels=x[1]))
        f.write('Total number of connected components = '+str(length))

