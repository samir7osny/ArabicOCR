from Utilities import *
 
def intarray(binstring):
    '''Change a 2D matrix of 01 chars into a list of lists of ints'''
    return [[1 if ch == '1' else 0 for ch in line] 
            for line in binstring.strip().split()]
 
def chararray(intmatrix):
    '''Change a 2d list of lists of 1/0 ints into lines of 1/0 chars'''
    return '\n'.join(''.join(str(p) for p in row) for row in intmatrix)
 
def toTxt(intmatrix):
    '''Change a 2d list of lists of 1/0 ints into lines of '#' and '.' chars'''
    return '\n'.join(''.join(('#' if p else '.') for p in row) for row in intmatrix)
 
def neighbours(x, y, image):
    '''Return 8-neighbours of point p1 of picture, in order'''
    i = image
    x1, y1, x_1, y_1 = x+1, y-1, x-1, y+1
    #print ((x,y))
    return [i[y1][x],  i[y1][x1],   i[y][x1],  i[y_1][x1],  # P2,P3,P4,P5
            i[y_1][x], i[y_1][x_1], i[y][x_1], i[y1][x_1]]  # P6,P7,P8,P9
 
def transitions(neighbours):
    n = neighbours + neighbours[0:1]    # P2, ... P9, P2
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

def zhangSuen(image):
    image = image.copy()
    image = addPadding(image, (1, 1, 1, 1))
    image[image == 255] = 1
    changing1 = changing2 = [(-1, -1)]
    while changing1 or changing2:
        # Step 1
        changing1 = []
        for y in range(1, len(image) - 1):
            for x in range(1, len(image[0]) - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, image)
                if (image[y][x] == 1 and    # (Condition 0)
                    P4 * P6 * P8 == 0 and   # Condition 4
                    P2 * P4 * P6 == 0 and   # Condition 3
                    transitions(n) == 1 and # Condition 2
                    2 <= sum(n) <= 6):      # Condition 1
                    changing1.append((x,y))
        for x, y in changing1: image[y][x] = 0
        # Step 2
        changing2 = []
        for y in range(1, len(image) - 1):
            for x in range(1, len(image[0]) - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, image)
                if (image[y][x] == 1 and    # (Condition 0)
                    P2 * P6 * P8 == 0 and   # Condition 4
                    P2 * P4 * P8 == 0 and   # Condition 3
                    transitions(n) == 1 and # Condition 2
                    2 <= sum(n) <= 6):      # Condition 1
                    changing2.append((x,y))
        for x, y in changing2: image[y][x] = 0
        #print changing1
        #print changing2
    image[image == 1] = 255
    image = removePadding(image, (1, 1, 1, 1))
    return image
 
# from Utilities import *
# img = loadImage('1.png')
# Parts = seperateToParts(img)
# for Part in Parts:
#     Part[Part <= 100] = 0
#     Part[Part > 0] = 1
#     Part = addPadding(Part, 1, 1)
#     Part = zhangSuen(Part)
#     Part[Part != 0] = 255
#     showImageZoomed(Part, ratio = 10)
    
# img = loadImage('2.png')
# Parts = seperateToParts(img)
# for Part in Parts:
#     Part[Part <= 100] = 0
#     Part[Part > 0] = 1
#     Part = addPadding(Part, 1, 1)
#     showImageZoomed(Part, ratio = 10)
#     Part = zhangSuen(Part)
#     Part[Part != 0] = 255
#     showImageZoomed(Part, ratio = 10)

    
# img = loadImage('3.png')
# Parts = seperateToParts(img)
# for Part in Parts:
#     Part[Part <= 100] = 0
#     Part[Part > 0] = 1
#     Part = addPadding(Part, 1, 1)
#     Part = zhangSuen(Part)
#     Part[Part != 0] = 255
#     showImageZoomed(Part, ratio = 10)

