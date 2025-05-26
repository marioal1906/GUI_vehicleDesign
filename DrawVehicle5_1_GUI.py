#!/usr/bin/env python

# Macro Begin: C:\Users\mario\AppData\Roaming\FreeCAD\Macro\asada2.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import numpy as np
from statistics import mean 
import FreeCAD
import FreeCADGui
import PartDesign
#import PartDesignGui
import Sketcher
# importing matplotlib modules
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import csv
import argparse

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="FreeCAD script with CSV input and additional parameters.")
parser.add_argument("csvFront_path", type=str, help="The path to the front CSV file.")
parser.add_argument("csvSide_path", type=str, help="The path to the front CSV file.")
parser.add_argument("csvTop_path", type=str, help="The path to the front CSV file.")
parser.add_argument("num1_min", type=float, help="The width of the part.")
parser.add_argument("num1_max", type=float, help="The width of the part.")
parser.add_argument("num2_min", type=float, help="The width of the part.")
parser.add_argument("num2_max", type=float, help="The width of the part.")
parser.add_argument("num3_min", type=float, help="The width of the part.")
parser.add_argument("num3_max", type=float, help="The width of the part.")
parser.add_argument("num4_min", type=float, help="The width of the part.")
parser.add_argument("num4_max", type=float, help="The width of the part.")
parser.add_argument("num5_min", type=float, help="The width of the part.")
parser.add_argument("num5_max", type=float, help="The width of the part.")
parser.add_argument("num6_min", type=float, help="The width of the part.")
parser.add_argument("num6_max", type=float, help="The width of the part.")
parser.add_argument("interpolation1", type=str, help="The width of the part.")
parser.add_argument("interpolation2", type=str, help="The width of the part.")
parser.add_argument("interpolation3", type=str, help="The width of the part.")
args = parser.parse_args()

csvFront_path = args.csvFront_path
csvSide_path = args.csvSide_path
csvTop_path = args.csvTop_path
num1_min = args.num1_min
num1_max = args.num1_max
num2_min = args.num2_min
num2_max = args.num2_max
num3_min = args.num3_min
num3_max = args.num3_max
num4_min = args.num4_min
num4_max = args.num4_max
num5_min = args.num5_min
num5_max = args.num5_max
num6_min = args.num6_min
num6_max = args.num6_max
interpolation0 = args.interpolation1
interpolation1 = args.interpolation2
interpolation2 = args.interpolation3

# Read the CSV file
#dfFront = pd.read_csv(csvFront_path)
#dfSide = pd.read_csv(csvSide_path)
#dfTop = pd.read_csv(csvTop_path)

#dfFront = np.array(dfFront)
#dfSide = np.array(dfSide)
#dfTop= np.array(dfTop)

# initialisation
n_draws=3

# Initialize FreeCAD (without GUI)
FreeCADGui.showMainWindow()
# Close FreeCAD
FreeCADGui.getMainWindow().close()

# initialisation
n_draws=3
view2=[csvFront_path,csvSide_path,csvTop_path]
xyz=np.array([[num1_min,num1_max],[num2_min,num2_max],[num3_min,num3_max],[num4_min,num4_max],[num5_min,num5_max],[num6_min,num6_max]])
##############


for draw in range(n_draws):

    file=open(view2[draw], 'r')
    file2=csv.reader(file)

    header=[]
    header=next(file2)

    file3=[]
    for row in file2:
        file3.append(row)

    data = []
    for sublist in file3:
        float_sublist = [float(element) for element in sublist]
        data.append(float_sublist)
    data = np.array(data)
    #print(data)

    def normalize_column(array, col_index, min_val, max_val):
        # Extract the column
        column = array[:, col_index]
    
        # Find the minimum and maximum values of the column
        min_col = np.min(column)
        max_col = np.max(column)
    
        # Perform min-max scaling
        normalized_column = ((column - min_col) / (max_col - min_col)) * (max_val - min_val) + min_val
    
        # Replace the original column with the normalized column in the array
        array[:, col_index] = normalized_column
    
        return array

    if draw == 0: # front yz

        data=normalize_column(data, 0, xyz[0,0], xyz[0,1])
        data=normalize_column(data, 1, xyz[1,0], xyz[1,1])

        sizeData=data.shape

        #print(sizeData[0])
        #data[:,0]=-data[:,0]
        #data[:,[0,1]]=data[:,[1,0]]
        #dataIndex=list(range(0, sizeData[0]))
        #dataIndex=list(range(0, sizeData[0],round(sizeData[0]/300)))
        #sizeShortData=len(dataIndex)
        #dataIndex.insert(sizeShortData,0)
        #print(dataIndex)
        #data=data[dataIndex,:]
        sizeShortData=sizeData[0]+1
        data = np.insert(data, sizeShortData-1, data[0,:], axis=0)
        print(sizeShortData)
        #print(data[0,:])
        #print(data[sizeShortData-1,:])

        App.newDocument("Unnamed0")

        App.activeDocument().addObject('Sketcher::SketchObject','Sketch0')

        #data[:,[0,1]]=data[:,[1,0]]
        #App.activeDocument().Sketch0.Support = (App.activeDocument().YZ_Plane, ['']) # front yz 
        App.activeDocument().Sketch0.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))

        App.activeDocument().Sketch0.MapMode = "Deactivated"

        App.ActiveDocument.recompute()

        if interpolation0 == "B-splines":
            geoList0 = []
            App.ActiveDocument.Sketch0.addGeometry(
                Part.Circle(App.Vector(data[0, 0], data[0, 1], 0), App.Vector(0, 0, 1), 10), True)
            App.ActiveDocument.Sketch0.addConstraint(Sketcher.Constraint('Radius', 0, 3.000000))
            geoList0.append(App.Vector(data[0, 0], data[0, 1]))
            for i in range(sizeShortData - 1):
                App.ActiveDocument.Sketch0.addGeometry(
                    Part.Circle(App.Vector(data[i + 1, 0], data[i + 1, 1], 0), App.Vector(0, 0, 1), 10), True)
                App.ActiveDocument.Sketch0.addConstraint(Sketcher.Constraint('Equal', 0, i + 1))
                geoList0.append(App.Vector(data[i + 1, 0], data[i + 1, 1]))
                # print(i)
            App.ActiveDocument.Sketch0.addGeometry(Part.BSplineCurve(geoList0, None, None, False, 3, None, False),
                                                   False)
            # print(geoList0)
            conList = []
            for i in range(sizeShortData):
                # print(i)
                conList.append(
                    Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint', i, 3, sizeShortData, i))
            App.ActiveDocument.Sketch0.addConstraint(conList)
            App.ActiveDocument.Sketch0.exposeInternalGeometry(sizeShortData)

        if interpolation0 == "Linear":
            App.ActiveDocument.Sketch0.addGeometry(
                Part.LineSegment(App.Vector(data[0, 0], data[0, 1], 0), App.Vector(data[1, 0], data[1, 1], 0)), False)
            for i in range(sizeShortData - 2):
                App.ActiveDocument.Sketch0.addGeometry(
                    Part.LineSegment(App.Vector(data[i + 1, 0], data[i + 1, 1], 0), App.Vector(data[i + 2, 0], data[i + 2, 1], 0)), False)
                App.ActiveDocument.Sketch0.addConstraint(Sketcher.Constraint('Coincident', i, 2, i + 1, 1))

        App.getDocument('Unnamed0').recompute()

        App.activeDocument().addObject('Part::Extrusion', 'Extrude0')
        App.ActiveDocument.Extrude0.Base = App.getDocument('Unnamed0').getObject('Sketch0')
        App.ActiveDocument.Extrude0.DirMode = "Normal"
        App.ActiveDocument.Extrude0.DirLink = None
        App.ActiveDocument.Extrude0.LengthFwd = 20.000000000000000
        App.ActiveDocument.Extrude0.LengthRev = 20.000000000000000
        App.ActiveDocument.Extrude0.Solid = True
        App.ActiveDocument.Extrude0.Reversed = False
        App.ActiveDocument.Extrude0.Symmetric = True
        App.ActiveDocument.Extrude0.TaperAngle = 0.000000000000000
        App.ActiveDocument.Extrude0.TaperAngleRev = 0.000000000000000
        App.ActiveDocument.recompute()


    if draw==1: # side xy

        data=normalize_column(data, 0, xyz[2,0], xyz[2,1])
        data=normalize_column(data, 1, xyz[3,0], xyz[3,1])

        sizeData=data.shape

        sizeShortData=sizeData[0]+1
        data = np.insert(data, sizeShortData-1, data[0,:], axis=0)
        print(sizeShortData)

        App.newDocument("Unnamed1")

        App.activeDocument().addObject('Sketcher::SketchObject','Sketch1')

        #App.activeDocument().Sketch1.Support = (App.activeDocument().XY_Plane, ['']) # side xy
        App.activeDocument().Sketch1.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

        App.activeDocument().Sketch1.MapMode = "Deactivated"

        App.ActiveDocument.recompute()

        if interpolation1 == "B-splines":
            geoList1 = []
            App.ActiveDocument.Sketch1.addGeometry(
                Part.Circle(App.Vector(data[0, 0], data[0, 1], 0), App.Vector(0, 0, 1), 10), True)
            App.ActiveDocument.Sketch1.addConstraint(Sketcher.Constraint('Radius', 0, 3.000000))
            geoList1.append(App.Vector(data[0, 0], data[0, 1]))
            for i in range(sizeShortData - 1):
                App.ActiveDocument.Sketch1.addGeometry(
                    Part.Circle(App.Vector(data[i + 1, 0], data[i + 1, 1], 0), App.Vector(0, 0, 1), 10), True)
                App.ActiveDocument.Sketch1.addConstraint(Sketcher.Constraint('Equal', 0, i + 1))
                geoList1.append(App.Vector(data[i + 1, 0], data[i + 1, 1]))
                # print(i)
            App.ActiveDocument.Sketch1.addGeometry(Part.BSplineCurve(geoList1, None, None, False, 3, None, False),
                                                   False)
            # print(geoList1)
            conList = []
            for i in range(sizeShortData):
                # print(i)
                conList.append(
                    Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint', i, 3, sizeShortData, i))
            App.ActiveDocument.Sketch1.addConstraint(conList)
            App.ActiveDocument.Sketch1.exposeInternalGeometry(sizeShortData)

        if interpolation1 == "Linear":
            App.ActiveDocument.Sketch1.addGeometry(
                Part.LineSegment(App.Vector(data[0, 0], data[0, 1], 0), App.Vector(data[1, 0], data[1, 1], 0)), False)
            for i in range(sizeShortData - 2):
                App.ActiveDocument.Sketch1.addGeometry(
                    Part.LineSegment(App.Vector(data[i + 1, 0], data[i + 1, 1], 0), App.Vector(data[i + 2, 0], data[i + 2, 1], 0)), False)
                App.ActiveDocument.Sketch1.addConstraint(Sketcher.Constraint('Coincident', i, 2, i + 1, 1))

        App.getDocument('Unnamed1').recompute()

        App.activeDocument().addObject('Part::Extrusion', 'Extrude1')
        App.ActiveDocument.Extrude1.Base = App.getDocument('Unnamed1').getObject('Sketch1')
        App.ActiveDocument.Extrude1.DirMode = "Normal"
        App.ActiveDocument.Extrude1.DirLink = None
        App.ActiveDocument.Extrude1.LengthFwd = 20.000000000000000
        App.ActiveDocument.Extrude1.LengthRev = 20.000000000000000
        App.ActiveDocument.Extrude1.Solid = True
        App.ActiveDocument.Extrude1.Reversed = False
        App.ActiveDocument.Extrude1.Symmetric = True
        App.ActiveDocument.Extrude1.TaperAngle = 0.000000000000000
        App.ActiveDocument.Extrude1.TaperAngleRev = 0.000000000000000
        App.ActiveDocument.recompute()


    if draw==2: # top xz

        data=normalize_column(data, 0, xyz[4,0], xyz[4,1])
        data=normalize_column(data, 1, xyz[5,0], xyz[5,1])

        sizeData=data.shape

        sizeShortData=sizeData[0]+1
        data = np.insert(data, sizeShortData-1, data[0,:], axis=0)
        print(sizeShortData)

        App.newDocument("Unnamed2")

        App.activeDocument().addObject('Sketcher::SketchObject','Sketch2')

        #centerY =np.mean(xyz[1,:])/100

        #App.activeDocument().Sketch2.Support = (App.activeDocument().XZ_Plane, ['']) # top xz
        App.activeDocument().Sketch2.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))

        App.activeDocument().Sketch2.MapMode = "Deactivated"

        App.ActiveDocument.recompute()

        if interpolation2 == "B-splines":
            geoList2 = []
            App.ActiveDocument.Sketch2.addGeometry(
                Part.Circle(App.Vector(data[0, 0], data[0, 1], 0), App.Vector(0, 0, 1), 10), True)
            App.ActiveDocument.Sketch2.addConstraint(Sketcher.Constraint('Radius', 0, 3.000000))
            geoList2.append(App.Vector(data[0, 0], data[0, 1]))
            for i in range(sizeShortData - 1):
                App.ActiveDocument.Sketch2.addGeometry(
                    Part.Circle(App.Vector(data[i + 1, 0], data[i + 1, 1], 0), App.Vector(0, 0, 1), 10), True)
                App.ActiveDocument.Sketch2.addConstraint(Sketcher.Constraint('Equal', 0, i + 1))
                geoList2.append(App.Vector(data[i + 1, 0], data[i + 1, 1]))
                # print(i)
            App.ActiveDocument.Sketch2.addGeometry(Part.BSplineCurve(geoList2, None, None, False, 3, None, False),
                                                   False)
            # print(geoList1)
            conList = []
            for i in range(sizeShortData):
                # print(i)
                conList.append(
                    Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint', i, 3, sizeShortData, i))
            App.ActiveDocument.Sketch2.addConstraint(conList)
            App.ActiveDocument.Sketch2.exposeInternalGeometry(sizeShortData)

        if interpolation2 == "Linear":
            App.ActiveDocument.Sketch2.addGeometry(
                Part.LineSegment(App.Vector(data[0, 0], data[0, 1], 0), App.Vector(data[1, 0], data[1, 1], 0)), False)
            for i in range(sizeShortData - 2):
                App.ActiveDocument.Sketch2.addGeometry(
                    Part.LineSegment(App.Vector(data[i + 1, 0], data[i + 1, 1], 0), App.Vector(data[i + 2, 0], data[i + 2, 1], 0)), False)
                App.ActiveDocument.Sketch2.addConstraint(Sketcher.Constraint('Coincident', i, 2, i + 1, 1))

        App.getDocument('Unnamed2').recompute()

        App.activeDocument().addObject('Part::Extrusion', 'Extrude2')
        App.ActiveDocument.Extrude2.Base = App.getDocument('Unnamed2').getObject('Sketch2')
        App.ActiveDocument.Extrude2.DirMode = "Normal"
        App.ActiveDocument.Extrude2.DirLink = None
        App.ActiveDocument.Extrude2.LengthFwd = 20.000000000000000
        App.ActiveDocument.Extrude2.LengthRev = 20.000000000000000
        App.ActiveDocument.Extrude2.Solid = True
        App.ActiveDocument.Extrude2.Reversed = False
        App.ActiveDocument.Extrude2.Symmetric = True
        App.ActiveDocument.Extrude2.TaperAngle = 0.000000000000000
        App.ActiveDocument.Extrude2.TaperAngleRev = 0.000000000000000
        App.ActiveDocument.recompute()


App.newDocument("Unnamed3")

App.activeDocument().moveObject(App.getDocument('Unnamed0').getObject('Extrude0'), True)
App.activeDocument().moveObject(App.getDocument('Unnamed1').getObject('Extrude1'), True)
App.activeDocument().moveObject(App.getDocument('Unnamed2').getObject('Extrude2'), True)

App.activeDocument().addObject("Part::MultiCommon","Common")
App.activeDocument().Common.Shapes = [App.activeDocument().Extrude1,App.activeDocument().Extrude2,App.activeDocument().Extrude0]
App.ActiveDocument.recompute()


### Begin command Std_Export


__objs__=[]
__objs__.append(FreeCAD.getDocument("Unnamed3").getObject("Common"))
import Mesh
Mesh.export(__objs__,u"Unnamed0-BodyPad.stl")

del __objs__


App.closeDocument("Unnamed0")
App.closeDocument("Unnamed1")
App.closeDocument("Unnamed2")
#App.closeDocument("Unnamed3")