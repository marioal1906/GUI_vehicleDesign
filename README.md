# GUI_vehicleDesign

This repository provides a Graphical User Interface (GUI) to facilitate drawing 3D vehicles within FreeCAD. This README will guide you through setting up and using the GUI, and provide an overview of its functionalities.

## **Getting Started**

To use this GUI, you'll need FreeCAD installed on your system. The Python scripts interact directly with FreeCAD's Python environment to execute drawing commands.

## **Important Pre-Configuration: File Paths**

**Before running the application, you MUST modify the file paths in the main2\_1.py file.**

On **lines 675 and 676** of main2\_1.py, you will find the following lines:

freecad\_path \= "/mnt/c/Program Files/FreeCAD 0.20/bin/python.exe"  
script\_path \= "/../../../Users/mario/Downloads/ObjectDrawingSTL/DrawVehicle5\_1\_GUI.py"

You need to change these paths to reflect the actual location of your FreeCAD Python executable and the DrawVehicle5\_1\_GUI.py script on your system.

* **freecad\_path**: This should point to the python.exe located within your FreeCAD installation's bin directory.  
* **script\_path**: This should point to the absolute path of the DrawVehicle5\_1\_GUI.py file from this repository.

**Example for Windows:**

freecad\_path \= "C:/Program Files/FreeCAD 0.20/bin/python.exe"  
script\_path \= "C:/Users/YourUser/Documents/GitHub/ObjectDrawingSTL/DrawVehicle5\_1\_GUI.py"

## **Running the GUI**

Once you have adjusted the file paths in main2\_1.py, you can run the GUI by executing main2\_1.py:

python main2\_1.py

## **GUI Functionality Overview**

This GUI is a Python-coded tool designed to streamline the reconstruction of 3D objects from 2D images, primarily for generating 3D models through extrusion and intersection. While initially designed for vehicle shapes, its potential extends to other areas requiring silhouette extraction and 3D modeling.

The process involves two main modules:

1. **Module 1: Silhouette Extraction**:  
   * **Input**: Requires three images (top, side, and front views) in PNG or JPG format.  
   * **Pre-processing**: Includes options for converting images to grayscale, inverting colors (e.g., for black background/white foreground images), and applying brightness-contrast adjustments or a Canny-Edge detector for refining foreground delineation.  
   * **Extraction**: Utilizes an enhanced Wall-Follower Algorithm (WFA\_v2) to extract external contours. Users can choose between full, optimized, or compressed versions of the silhouettes.  
   * **Output**: Generates silhouette data in CSV format, ready for the next module.  
2. **Module 2: 3D Reconstruction**:  
   * **Input**: Uploads the CSV silhouette files generated in Module 1\.  
   * **Resizing**: Allows users to resize the extracted silhouettes by entering minimum and maximum coordinates along each axis, ensuring proper intersection.  
   * **Interpolation**: Offers a choice between linear and b-Splines interpolation methods, which FreeCAD uses for the 3D reconstruction. The b-Splines method generally provides smoother reconstructions with more detail, while linear interpolation is faster and results in smaller file sizes.  
   * **3D Model Generation**: Calls FreeCAD to extrude each cross-section (silhouette) in its perpendicular direction. The resulting three volumes are then intersected using FreeCAD's "Common" Boolean operation to build the final 3D object.  
   * **Output**: Saves the final 3D object as an finalObject.stl mesh file, along with binary images and silhouette data tables (PNG and CSV files).

The GUI aims to provide a user-friendly interface with intuitive parameter adjustment tools and error-reduction mechanisms, making it useful for both novice designers and engineers.

## **Reproducing Examples**

To help you get started and reproduce the examples discussed in the associated paper, the exampleTests folder contains all the necessary input files (images) for the car, truck, and airplane models. You can use these files directly with the GUI to generate the corresponding 3D objects.

## **Using the GUI**

The GUI provides an intuitive interface to control various parameters for drawing vehicles in FreeCAD. The sections above and the detailed comments within the source code provide guidance on each input field and its effect on the vehicle drawing.

## **Documentation**

For detailed information on the functionalities, parameters, and design principles behind this GUI, please refer to the "GUI Functionality Overview" section within this README. It offers a complete overview of the system and its capabilities.
