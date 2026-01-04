# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision H, 01/02/2026

Verified working on: Python 3.12/13 for Windows 10/11 64-bit (Backend = "CAP_DSHOW") and Raspberry Pi Bullseye (Backend = "CAP_ANY").
'''

__author__ = 'reuben.brewer'

############################################
import math

from fpdf import FPDF #pip install fpdf2, https://pyfpdf.readthedocs.io/en/latest/reference/image/index.html
############################################

USE_RECTILINEAR_GRID_FLAG = 1

USE_CIRCULAR_PATTERN_FLAG = 0

pdf = FPDF()
pdf.set_auto_page_break(0)


############################################
Directory_FullPath = "G:\My Drive\CodeReuben\ArucoTagDetectionFromCameraFeed_ReubenPython3Class"
Filename_Prefix = "ArucoTag_Type_DICT_4X4_50_ID_"
Filename_Extention = ".png"
ListOfFilePaths = []

for Index in range(1,13):
    Filename_FullPath = Directory_FullPath + "\\" + Filename_Prefix + str(Index) + Filename_Extention
    ListOfFilePaths.append(Filename_FullPath)

print("ListOfFilePaths: " + str(ListOfFilePaths))
############################################

############################################
if USE_RECTILINEAR_GRID_FLAG == 1:
    pdf.add_page(orientation="portrait", format="letter")

    y = -1
    w = 45
    h = w
    space_x = 7
    space_y = 15

    for index, image in enumerate(ListOfFilePaths):

        x = (index%4)

        if x == 0:
            y = y + 1

        print("(" + str(x) + ", " + str(y) +")")
        pdf.image(image,space_x + x*(w+space_x),space_y + y*(h+space_y),w,h)
############################################

############################################
if USE_CIRCULAR_PATTERN_FLAG == 1:
    pdf.add_page(orientation="portrait", format="letter")

    y = -1
    w = 25
    h = w
    radius = 75

    center_X = (8.5/2.0)*25.4 - w/2.0
    center_Y = (11/2.0)*25.4 - w/2.0
    for index, image in enumerate(ListOfFilePaths):

        theta = index*(2.0*math.pi/len(ListOfFilePaths))

        x = center_X + radius*math.cos(theta)

        y = center_Y + radius*math.sin(theta)

        print("(" + str(x) + ", " + str(y) + ")")
        pdf.image(image, x, y, w, h)
############################################

pdf.output("AssembledImages.pdf", "F")