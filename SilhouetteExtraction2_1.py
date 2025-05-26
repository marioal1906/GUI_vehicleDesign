#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import cv2
import json

def contour_tracing3(M, M_new,xy,startXY,d,startD):
    def tag_simple(M_new, M_new2, xy, d_ast, startXY, startD):
        nonlocal finish, index1, indexFinal
        if (xy[0] == startXY[0]) and (xy[1] == startXY[1]) and (d_ast[1] == startD[1]):
            finish = 1
            indexFinal = index1
        M_new[xy[0], xy[1]] += 1
        M_new2.append([xy[1], xy[0]])
        index1 += 1
        return M_new, M_new2

    def move_complex(M, M_new, M_new2, xy, d, startXY, startD):
        xyd = xy + d
        while 0 <= xyd[0] < M.shape[0] and 0 <= xyd[1] < M.shape[1] and M[xyd[0], xyd[1]] == 1:
            d = d[[1, 0]] * np.sign(abs(d[0]) - abs(d[1]))
            M_new, M_new2 = tag_simple(M_new, M_new2, xyd, d, startXY, startD)
            xyd = xy + d
        if 0 <= xyd[0] < M.shape[0] and 0 <= xyd[1] < M.shape[1]:
            xy = xyd
        return M_new, M_new2, xy, d

    def tag_complex(M, M_new, M_new2, xy, d, startXY, startD):
        tagged = 0
        while tagged == 0:
            d_right = d[[1, 0]] * np.sign(abs(d[1]) - abs(d[0]))
            xyd_right = xy + d_right
            if 0 <= xyd_right[0] < M.shape[0] and 0 <= xyd_right[1] < M.shape[1] and M[xyd_right[0], xyd_right[1]] == 1:
                M_new, M_new2 = tag_simple(M_new, M_new2, xyd_right, d, startXY, startD)
                tagged = 1
            else:
                d = d_right
                xy = xyd_right
            #print(xy)
        return M_new, M_new2, xy, d

    #print(xy)
    finish = 0
    index1 = 1
    indexFinal = 1
    M_new2 = []

    while finish == 0:
        #print(xy,d,1)
        M_new, M_new2, xy, d = move_complex(M, M_new, M_new2, xy, d, startXY, startD)
        #print(xy,d,2)
        M_new, M_new2, xy, d = tag_complex(M, M_new, M_new2, xy, d, startXY, startD)
        #print(xy,d,3)
    M_new2 = M_new2[:indexFinal]
    return M_new, np.array(M_new2, dtype=float)

# Load the image
img_path = 'img_gray.png'
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Check if the image was loaded properly
if img is None:
    raise FileNotFoundError(f"Image file '{img_path}' not found or could not be opened.")

img = img / 255.0

# Invert the image for visualization after the processing
M_original = img
#img = cv2.flip(img, 0)

# Initial plot
#plt.imshow(M_original[::1], cmap='gray')
#plt.show()

# Add a border of zeros
M = np.pad(M_original, pad_width=1, mode='constant', constant_values=0)

# Call the W-FA
M_new = np.zeros_like(M)
xy = np.array([0, M.shape[1] // 2])
# print(xy)
# print(M.shape)
startD = np.array([1, 0])
while 0 <= xy[0] + startD[0] < M.shape[0] and 0 <= xy[1] + startD[1] < M.shape[1] and M[
    xy[0] + startD[0], xy[1] + startD[1]] == 0:
    xy += startD
startXY = xy + startD
d = startD[[1, 0]] * np.sign(abs(startD[0]) - abs(startD[1]))
startD = d
#print(xy,startXY,d,startD)

M_new, M_new2 = contour_tracing3(M, M_new,xy,startXY,d,startD)

M_final = M_new2
# Loop through the vector
j = 0
for i, value1 in enumerate(M_new2[3:]):
    if np.abs(M_new2[i-1][0]-M_new2[i-2][0]) == np.abs(M_new2[i-1][1]-M_new2[i-2][1]) and (M_new2[i-1][0]-M_new2[i-2][0] != 0 or M_new2[i-1][0]-M_new2[i-2][0] != 0):
        if M_new2[i][0] == M_new2[i - 1][0] or M_new2[i][1] == M_new2[i - 1][1]:
            if M_new2[i - 2][0] == M_new2[i - 3][0] or M_new2[i - 2][1] == M_new2[i - 3][1]:
                #print(j, M_new2[i - 2], M_new2[i - 1])
                M_final[i - 2] = (M_new2[i - 2] + M_new2[i - 1]) / 2
                #print(j, M_final[i - 2])
                M_final[i - 1] = M_final[i - 2]
                j += 1

# Plots
#plt.imshow(M_new[::1], cmap='gray')
#plt.contour(M_new[::1], colors='r')
#plt.show()

# M_new2 plotting
#plt.plot(M_new2[:,0],M_new2[:,1],'--')
#plt.gca().set_aspect('equal', adjustable='box')  # Ensures equal aspect ratio
#plt.show()


def keep_unique_repeated_rows(matrix):
    # Convert each row to a tuple (hashable) to use as dictionary keys
    row_tuples = [tuple(row) for row in matrix]

    # Count occurrences of each row
    counts = {}
    for row in row_tuples:
        if row in counts:
            counts[row] += 1
        else:
            counts[row] = 1

    # Filter rows that occur more than once, keeping the first occurrence
    seen = set()
    unique_repeated_rows = []
    for row in row_tuples:
        if counts[row] > 1 and row not in seen:
            unique_repeated_rows.append(row)
            seen.add(row)

    # Convert list of tuples back to a numpy array
    result_matrix = np.array(unique_repeated_rows)

    return result_matrix

# Debugging
M_final = np.array(M_final)
# Use np.diff() to find differences between consecutive rows
diffs = np.diff(M_final, axis=0)

# Identify where rows are not equal (i.e., where diffs are not all zero)
not_equal = np.any(diffs != 0, axis=1)

#plt.plot(M_final[:,0],M_final[:,1])
#plt.show()

# Keep the first row and the non-equal rows
M_final_debugged = M_final[np.append(True, not_equal)]

M_final2 = keep_unique_repeated_rows(M_final)

identical = np.array_equal(M_final, M_final2)

if identical:
    M_final2 = M_final_debugged

#print(len(M_new2),len(M_final),len(M_final2))

# Save the data to a .npz file
np.savez('output_data.npz', mFull=M_new2, mReduced=M_final2)