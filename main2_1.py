#!/usr/bin/env python

#from shiny import App, reactive, render, ui
#import pandas as pd
import plotly.express as px
from shiny import App, reactive, render, ui
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
import subprocess
import cv2
import json
import time

# Define the UI components
main_ui = ui.page_fluid(
    ui.tags.style("""
    body {
        background-color: #e6ffe6; /* Light green background */
        color: #333333; /* Dark grey text */
        font-family: 'Cinzel Decorative', cursive; #Arial, Helvetica, sans-serif; #'Times New Roman', Times, serif;
    }
    .panel-sidebar {
        background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
        border: 3px solid #28a745; /* Dark green */
        border-radius: 7px;
    }
    .panel-sidebar-active {
        background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
        border: 3px solid #28a745; /* Dark green */
        border-radius: 7px;
        opacity: 1; /* No transparency */
        pointer-events: auto; /* Enable interaction */
    }
    .panel-sidebar-inactive {
        background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
        border: 3px solid #28a745; /* Dark green */
        border-radius: 7px;
        opacity: 0.5; /* Set transparency */
        pointer-events: none; /* Disable interaction */
    }
    .panel-main {
        background-color: #333333; /* Light green */
        border-color: #dddddd; /* Light grey border */
    }
    .btn-primary1 {
        background-color: #007bff; /* Sky blue button */
        border-color: #007bff;
        color: white;
        border-radius: 3px;
    }
    .btn-primary1-active {
        background-color: #007bff; /* Sky blue button */
        border-color: #007bff;
        color: white;
        border-radius: 3px;
        opacity: 1; /* No transparency */
        pointer-events: auto; /* Enable interaction */
    }
    .btn-primary1-inactive {
        background-color: #007bff; /* Sky blue button */
        border-color: #007bff;
        color: white;
        border-radius: 3px;
        opacity: 0.5; /* Set transparency */
        pointer-events: none; /* Disable interaction */
    }
    .btn-primary2 {
        background-color: #007bff; /* Sky blue button */
        border-color: #007bff;
        color: #ffffff;
        border-radius: 3px;
    }
    .ui-output-text-verbatim {
        background-color: #e6f7ff; /* Light green background for output text */
        border: 1px solid #007bff;
        padding: 10px;
        border-radius: 5px;
    }
    .ui-output-ui {
        background-color: #e6ffe6; /* Light green background for plots */
        border: 3px solid #333333;
        border-radius: 7px;
    }
    .ui-input {
        margin-bottom: 15px; /* Space between inputs */
    }
    .radio-horizontal .form-check {
        display: inline-block;
        margin-right: 40px;
    }
    .switch-container {
        display: flex;
        gap: 20px;
        align-items: center;
    }
    .coordinate-inputs {
        display: flex;
        gap: 10px;
    }
"""),
    ui.tags.script("""
    Shiny.addCustomMessageHandler('set_class', function(message) {
        var element = document.getElementById(message.element_id);
        if (element){
            element.className = message.class_name;
        }
     });
"""),
    ui.output_ui("main_content"),
)

# Define the UI for screen 1
screen1_ui = ui.div(
    ui.tags.style("""
        body {
            background-color: #e6ffe6; /* Light green background */
            color: #333333; /* Dark grey text */
            font-family: 'Cinzel Decorative', cursive; #Arial, Helvetica, sans-serif; #'Times New Roman', Times, serif;
        }
        .panel-sidebar {
            background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
            border: 3px solid #28a745; /* Dark green */
            border-radius: 7px;
        }
        .panel-sidebar-active {
            background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
            border: 3px solid #28a745; /* Dark green */
            border-radius: 7px;
            opacity: 1; /* No transparency */
            pointer-events: auto; /* Enable interaction */
        }
        .panel-sidebar-inactive {
            background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
            border: 3px solid #28a745; /* Dark green */
            border-radius: 7px;
            opacity: 0.5; /* Set transparency */
            pointer-events: none; /* Disable interaction */
        }
        .panel-main {
            background-color: #333333; /* Light green */
            border-color: #dddddd; /* Light grey border */
        }
        .btn-primary1 {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: white;
            border-radius: 3px;
        }
        .btn-primary1-active {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: white;
            border-radius: 3px;
            opacity: 1; /* No transparency */
            pointer-events: auto; /* Enable interaction */
        }
        .btn-primary1-inactive {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: white;
            border-radius: 3px;
            opacity: 0.5; /* Set transparency */
            pointer-events: none; /* Disable interaction */
        }
        .btn-primary2 {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: #ffffff;
            border-radius: 3px;
        }
        .ui-output-text-verbatim {
            background-color: #e6f7ff; /* Light green background for output text */
            border: 1px solid #007bff;
            padding: 10px;
            border-radius: 5px;
        }
        .ui-output-ui {
            background-color: #e6ffe6; /* Light green background for plots */
            border: 3px solid #333333;
            border-radius: 7px;
        }
        .ui-input {
            margin-bottom: 15px; /* Space between inputs */
        }
        .radio-horizontal .form-check {
            display: inline-block;
            margin-right: 40px;
        }
        .switch-container {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .coordinate-inputs {
            display: flex;
            gap: 10px;
        }
    """),
    ui.tags.script("""
        Shiny.addCustomMessageHandler('set_class', function(message) {
            var element = document.getElementById(message.element_id);
            if (element){
                element.className = message.class_name;
            }
         });
    """),
    ui.div(style="margin-bottom: 10px;"),  # Adding space between rows
    ui.div(
        ui.h1(
            "------------------------------------------------------------", style="text-align: center; font-weight: bold;"),
        ui.row(
            ui.column(3, ui.h1(">>>>>>>>>>>", style="text-align: right; font-weight: bold;")),
            ui.column(6,
                      ui.h1("SILHOUETTE EXTRACTION", style="text-align: center; font-weight: bold; color: #007bff;")),
            ui.column(3, ui.h1("<<<<<<<<<<<", style="text-align: left; font-weight: bold;"))
        ),
        ui.h1(
            "------------------------------------------------------------", style="text-align: center; font-weight: bold;"),
    ),  # Adding space between rows
    ui.div(style="margin-bottom: 20px;"),  # Adding space between rows
    ui.h2("Front View", style="text-align: center; font-weight: bold;  color: #007bff;"),
    ui.row(
        # First plot
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.div(
                              ui.input_file("image_input1", "Choose a PNG or JPG File", multiple=False,
                                            accept=['.png']),
                              ui.input_switch("switchColors1", "Your silhouette is Not in White?", False),
                              ui.input_slider("filter1_value", "B&W threshold:", 0, 100, 50),
                              ui.input_switch("switchFilter1", "Need for a filter?", False)
                          ),
                          ui.output_ui("dynamic_panelFilter1")
                      ), id="finishedSilhouette1_1"
                  )
        ),
        ui.column(6,
                  ui.panel_main(
                      ui.output_ui("plotImage1"),
                      ui.div(style="margin-bottom: 10px;"),
                      ui.div(
                          ui.input_switch("readySilhouette1", "Silhouette READY?", False)
                      )
                  )
                  ),
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.div(
                              ui.input_switch("actionSilhouette1", "Silhouette Extraction", False)
                          ),
                          ui.output_ui("dynamic_panelSilhouette1")
                      ), id="finishedSilhouette1_2"
                  )
        )
    ),
    ui.div(style="margin-bottom: 10px;"),  # Adding space between rows
    ui.div(
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;")
    ),  # Adding space between rows
    ui.div(style="margin-bottom: 20px;"),  # Adding space between rows
    ui.h2("Side View", style="text-align: center; font-weight: bold; color: #007bff;"),
    ui.row(
        # Second plot
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.div(
                              ui.input_file("image_input2", "Choose a PNG or JPG File", multiple=False,
                                            accept=['.png']),
                              ui.input_switch("switchColors2", "Your silhouette is Not in White?", False),
                              ui.input_slider("filter2_value", "B&W threshold:", 0, 100, 50),
                              ui.input_switch("switchFilter2", "Need for a filter?", False)
                          ),
                          ui.output_ui("dynamic_panelFilter2")
                      ), id="finishedSilhouette2_1"
                  )
        ),
        ui.column(6,
                  ui.panel_main(
                      ui.output_ui("plotImage2"),
                      ui.div(style="margin-bottom: 10px;"),
                      ui.div(
                          ui.input_switch("readySilhouette2", "Silhouette READY?", False)
                      )
                  )
                  ),
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.div(
                              ui.input_switch("actionSilhouette2", "Silhouette Extraction", False)
                          ),
                          ui.output_ui("dynamic_panelSilhouette2")
                      ), id="finishedSilhouette2_2"
                  )
        )
    ),
    ui.div(style="margin-bottom: 10px;"),  # Adding space between rows
    ui.div(
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;")
    ),  # Adding space between rows
    ui.div(style="margin-bottom: 20px;"),  # Adding space between rows
    ui.h2("Top View", style="text-align: center; font-weight: bold; color: #007bff;"),
    ui.row(
        # Third plot
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.div(
                              ui.input_file("image_input3", "Choose a PNG or JPG File", multiple=False,
                                            accept=['.png']),
                              ui.input_switch("switchColors3", "Your silhouette is Not in White?", False),
                              ui.input_slider("filter3_value", "B&W threshold:", 0, 100, 50),
                              ui.input_switch("switchFilter3", "Need for a filter?", False)
                          ),
                          ui.output_ui("dynamic_panelFilter3")
                      ), id="finishedSilhouette3_1"
                  )
        ),
        ui.column(6,
                  ui.panel_main(
                      ui.output_ui("plotImage3"),
                      ui.div(style="margin-bottom: 10px;"),
                      ui.div(
                          ui.input_switch("readySilhouette3", "Silhouette READY?", False)
                      )
                  )
                  ),
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.div(
                              ui.input_switch("actionSilhouette3", "Silhouette Extraction", False)
                          ),
                          ui.output_ui("dynamic_panelSilhouette3")
                      ), id="finishedSilhouette3_2"
                  )
        )
    ),
    ui.div(style="margin-bottom: 30px;"),  # Adding space between rows
    ui.div(
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;"),
        ui.row(
            ui.column(3, ui.h1("<<<<<<<<<<<", style="text-align: right; font-weight: bold;")
                      ),
            ui.column(3, ui.input_action_button("to_main", "Back to Main", class_="btn-primary1"), style="text-align: center;"
                      ),
            ui.column(3, ui.div( ui.input_action_button("to_screen2_CSVfiles", "Go to Build the 3D-OBJECT", class_="btn-primary1"),
                      style="text-align: center;", id="finishedStep1")
                      ),
            ui.column(3, ui.h1(">>>>>>>>>>>", style="text-align: left; font-weight: bold;")
                      )
        ),
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;")
    )
)



# Define the UI for screen 2
screen2_ui = ui.div(
    ui.tags.style("""
        body {
            background-color: #e6ffe6; /* Light green background */
            color: #333333; /* Dark grey text */
            font-family: 'Cinzel Decorative', cursive; #Arial, Helvetica, sans-serif; #'Times New Roman', Times, serif;
        }
        .panel-sidebar {
            background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
            border: 3px solid #28a745; /* Dark green */
            border-radius: 7px;
            opacity: 1; /* No transparency */
            pointer-events: auto; /* Enable interaction */
        }
        .panel-sidebar-active {
            background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
            border: 3px solid #28a745; /* Dark green */
            border-radius: 7px;
            opacity: 1; /* No transparency */
            pointer-events: auto; /* Enable interaction */
        }
        .panel-sidebar-inactive {
            background-color: #e6ffe6; /* Light green background for plots */ # #ffffff; /* White sidebar */
            border: 3px solid #28a745; /* Dark green */
            border-radius: 7px;
            opacity: 0.5; /* Set transparency */
            pointer-events: none; /* Disable interaction */
        }
        .panel-main {
            background-color: #333333; /* Light green */
            border-color: #dddddd; /* Light grey border */
        }
        .btn-primary1 {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: white;
            border-radius: 3px;
        }
        .btn-primary1-active {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: white;
            border-radius: 3px;
            opacity: 1; /* No transparency */
            pointer-events: auto; /* Enable interaction */
        }
        .btn-primary1-inactive {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: white;
            border-radius: 3px;
            opacity: 0.5; /* Set transparency */
            pointer-events: none; /* Disable interaction */
        }
        .btn-primary2 {
            background-color: #007bff; /* Sky blue button */
            border-color: #007bff;
            color: #ffffff;
            border-radius: 3px;
        }
        .ui-output-text-verbatim {
            background-color: #e6f7ff; /* Light blue background for output text */
            border: 1px solid #007bff;
            padding: 10px;
            border-radius: 5px;
        }
        .ui-output-ui {
            background-color: #e6ffe6; /* Light green background for plots */
            border: 3px solid #333333;
            border-radius: 7px;
        }
        .ui-input {
            margin-bottom: 15px; /* Space between inputs */
        }
        .radio-horizontal .form-check {
            display: inline-block;
            margin-right: 40px;
        }
        .switch-container {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .coordinate-inputs {
            display: flex;
            gap: 10px;
        }
    """),
    ui.tags.script("""
        Shiny.addCustomMessageHandler('set_class', function(message) {
            var element = document.getElementById(message.element_id);
            if (element){
                element.className = message.class_name;
            }
         });
    """),
    ui.div(style="margin-bottom: 10px;"),  # Adding space between rows
    ui.div(
        ui.h1(
            "------------------------------------------------------------",
            style="text-align: center; font-weight: bold;"),
        ui.row(
            ui.column(3, ui.h1(">>>>>>>>>>>", style="text-align: right; font-weight: bold;")),
            ui.column(6,
                      ui.h1("3D-VEHICLE DESIGN",
                            style="text-align: center; font-weight: bold; color: #007bff;")),
            ui.column(3, ui.h1("<<<<<<<<<<<", style="text-align: left; font-weight: bold;"))
        ),
        ui.h1(
            "------------------------------------------------------------",
            style="text-align: center; font-weight: bold;"),
    ),  # Adding space between rows
    ui.div(style="margin-bottom: 20px;"),  # Adding space between rows
    ui.h2("Front View", style="text-align: center; font-weight: bold;  color: #007bff;"),
    ui.row(
        # First plot
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.input_file("file_input1", "Choose a CSV File", multiple=False, accept=['.csv']),
                          ui.input_numeric("num1_min", "Min value for Y", -1, min=-100, step=0.1),
                          ui.input_numeric("num1_max", "Max value for Y", 1, min=-100, step=0.1),
                          ui.input_numeric("num2_min", "Min value for Z", 0, min=-100, step=0.1),
                          ui.input_numeric("num2_max", "Max value for Z", 1, min=-100, step=0.1),
                          ui.div(
                              ui.input_radio_buttons("interpolation1_choice", "Interpolation Method:",
                                                     choices={"Linear": "linear", "B-splines": "b-splines"},
                                                     selected="Linear"), class_="radio-horizontal"
                          )
                      ), id="finishedObject1"
                  )
        ),
        ui.column(6,
            ui.panel_main(
                ui.output_ui("plot1")
            ),
            ui.div(style="margin-bottom: 10px;"),
            ui.div(
                ui.input_switch("readyObject1", "Parameters READY?", False)
            ), class_="ui-output-ui"
        )#,
        #ui.column(3,
        #          ui.panel_sidebar(
        #              ui.div(
        #                  ui.input_switch("switch1", "Holes in the object?", False),
        #                  class_="switch-container"
        #              ),
        #              ui.output_ui("dynamic_panel1")
        #          )
        #          )
    ),
    ui.div(style="margin-bottom: 10px;"),  # Adding space between rows
    ui.div(
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;")
    ),  # Adding space between rows
    ui.div(style="margin-bottom: 20px;"),  # Adding space between rows
    ui.h2("Side View", style="text-align: center; font-weight: bold; color: #007bff;"),    ui.row(
        # Second plot
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.input_file("file_input2", "Choose a CSV File", multiple=False, accept=['.csv']),
                          ui.input_numeric("num3_min", "Min value for X", -1.5, min=-100, step=0.1),
                          ui.input_numeric("num3_max", "Max value for X", 1.5, min=-100, step=0.1),
                          ui.input_numeric("num4_min", "Min value for Z", 0, min=-100, step=0.1),
                          ui.input_numeric("num4_max", "Max value for Z", 1, min=-100, step=0.1),
                          ui.div(
                              ui.input_radio_buttons("interpolation2_choice", "Interpolation Method:",
                                                     choices={"Linear": "linear", "B-splines": "b-splines"},
                                                     selected="Linear"), class_="radio-horizontal"
                          )
                      ), id="finishedObject2"
                  )
                  ),
        ui.column(6,
                  ui.panel_main(
                      ui.output_ui("plot2")
                  ),
                  ui.div(style="margin-bottom: 10px;"),
                  ui.div(
                      ui.input_switch("readyObject2", "Parameters READY?", False)
                  ), class_="ui-output-ui"
                  )#,
        #ui.column(3,
        #          ui.panel_sidebar(
        #              ui.div(
        #                  ui.input_switch("switch2", "Holes in the object?", False),
        #                  class_="switch-container"
        #              ),
        #              ui.output_ui("dynamic_panel2")
        #          )
        #          )
    ),
    ui.div(style="margin-bottom: 10px;"),  # Adding space between rows
    ui.div(
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;")
    ),  # Adding space between rows
    ui.div(style="margin-bottom: 20px;"),  # Adding space between rows
    ui.h2("Top View", style="text-align: center; font-weight: bold; color: #007bff;"),    ui.row(
        # Third plot
        ui.column(3,
                  ui.div(
                      ui.panel_sidebar(
                          ui.input_file("file_input3", "Choose a CSV File", multiple=False, accept=['.csv']),
                          ui.input_numeric("num5_min", "Min value for X", -1.5, min=-100, step=0.1),
                          ui.input_numeric("num5_max", "Max value for X", 1.5, min=-100, step=0.1),
                          ui.input_numeric("num6_min", "Min value for Y", -1, min=-100, step=0.1),
                          ui.input_numeric("num6_max", "Max value for Y", 1, min=-100, step=0.1),
                          ui.div(
                              ui.input_radio_buttons("interpolation3_choice", "Interpolation Method:",
                                                     choices={"Linear": "linear", "B-splines": "b-splines"},
                                                     selected="Linear"), class_="radio-horizontal"
                          )
                      ), id="finishedObject3"
                  )
                  ),
        ui.column(6,
                  ui.panel_main(
                      ui.output_ui("plot3")
                  ),
                  ui.div(style="margin-bottom: 10px;"),
                  ui.div(
                      ui.input_switch("readyObject3", "Parameters READY?", False)
                  ), class_="ui-output-ui"
                  )#,
        #ui.column(3,
        #          ui.panel_sidebar(
        #              ui.div(
        #                  ui.input_switch("switch3", "Holes in the object?", False),
        #                  class_="switch-container"
        #              ),
        #              ui.output_ui("dynamic_panel3")
        #          )
        #          )
    ),
    ui.div(style="margin-bottom: 30px;"),  # Adding space between rows
    ui.div(
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;"),
        ui.row(
            ui.column(3, ui.h1("<<<<<<<<<<<", style="text-align: right; font-weight: bold;")
                      ),
            ui.column(3, ui.input_action_button("to_screen1", "Back to Silhouette", class_="btn-primary1"), style="text-align: center;"
                      ),
            ui.column(3, ui.div( ui.input_action_button("run_freecad", "Build the STL file", class_="btn-primary1"),
                      style="text-align: center;", id="finishedStep2")
                      ),
            ui.column(3, ui.h1(">>>>>>>>>>>", style="text-align: left; font-weight: bold;")
                      )
        ),
        ui.h1("------------------------------------------------------------", style="text-align: center; font-weight: bold;")
    )
)

# Define the server logic for the main app
def server(input, output, session):
    current_screen = reactive.Value("main")

    shapeFull1 = reactive.Value()
    shapeReduced1 = reactive.Value()
    nPoints_silhouette1 = reactive.Value()
    shapeFull2 = reactive.Value()
    shapeReduced2 = reactive.Value()
    nPoints_silhouette2 = reactive.Value()
    shapeFull3 = reactive.Value()
    shapeReduced3 = reactive.Value()
    nPoints_silhouette3 = reactive.Value()

    @reactive.Effect
    @reactive.event(input.to_screen1)
    def go_to_screen1():
        current_screen.set("screen1")

    @reactive.Effect
    @reactive.event(input.to_screen2)
    def go_to_screen2():
        current_screen.set("screen2")

    @reactive.Effect
    @reactive.event(input.to_screen2_CSVfiles)
    def go_to_screen2_and_CSVfiles():
        # Save the silhouettes to CSV files
        finalSilhouette1 = nPoints_silhouette1.get()
        finalSilhouette2 = nPoints_silhouette2.get()
        finalSilhouette3 = nPoints_silhouette3.get()
        finalSilhouette1[:,1] = -finalSilhouette1[:,1] + max(finalSilhouette1[:,1])
        finalSilhouette2[:,1] = -finalSilhouette2[:,1] + max(finalSilhouette2[:,1])
        finalSilhouette3[:,1] = -finalSilhouette3[:,1] + max(finalSilhouette3[:,1])

        np.savetxt('finalSilhouette_front.csv', finalSilhouette1, delimiter=',')
        np.savetxt('finalSilhouette_side.csv', finalSilhouette2, delimiter=',')
        np.savetxt('finalSilhouette_top.csv', finalSilhouette3, delimiter=',')

        current_screen.set("screen2")

    @reactive.Effect
    @reactive.event(input.to_main)
    def go_to_main():
        current_screen.set("main")


    # Define a function to generate a rainbow color map
    def get_rainbow_color(index, total_points):
        hue = int(179 * index / total_points)  # Calculate hue based on the index
        color_hsv = np.uint8([[[hue, 255, 255]]])  # Full saturation and value
        color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]  # Convert to BGR
        return tuple(int(c) for c in color_bgr)  # Convert to a tuple of integers

    freecad_path = "/mnt/c/Program Files/FreeCAD 0.20/bin/python.exe"
    script_path = "/../../../Users/mario/Downloads/ObjectDrawingSTL/DrawVehicle5_1_GUI.py"

    @output
    @render.ui
    def main_content():
        if current_screen.get() == "main":
            return ui.div(
                ui.h2("The Object Reconstructor"),
                ui.p("THIS APP ALLOWS THE USER TO OBTAIN A 3D-VEHICLE SAVED IN A STL FILE FROM:"),
                ui.p("1) A SET OF 3 IMAGES (FRONT, SIDE AND TOP VIEWS) OR WELL,"),
                ui.p("2) A SET OF 3 CSV FILES WITH THE CORRESPONDING SILHOUETTES, EACH ONE WITH ORDERED POINTS TRACKING THE CONTOUR OF THE VEHICLE."),
                ui.p("Unless your csv files satisfy the last condition, go to Silhouette Extraction"),
                ui.input_action_button("to_screen1", "Go to Silhouette Extraction", class_="btn-primary"),
                ui.input_action_button("to_screen2", "Go to 3D-Object Design", class_="btn-primary")
            )
        elif current_screen.get() == "screen1":
            return screen1_ui
        elif current_screen.get() == "screen2":
            return screen2_ui

    @output
    @render.ui
    def plotImage1():
        file_info = input.image_input1()
        if file_info is None:
            return ui.tags.blockquote(
                "PLEASE, READ CAREFULLY:", ui.tags.br(),
                "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PRE-PROCESSING (LEFT) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", ui.tags.br(),
                "1) Upload a PNG or JPG file to see the image", ui.tags.br(),
                "NOTE: Be careful that the Silhouette is in White, and the Background in Black (LEFT)", ui.tags.br(),
                "2) Then, if necessary, adjust threshold and filters", ui.tags.br(),
                " ", ui.tags.br(),
                ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXTRACTION (RIGHT) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", ui.tags.br(),
                "3) Finally, activate the extraction silhouette button, select the type of silhouette", ui.tags.br(),
                "and % of points", ui.tags.br(),
                " ", ui.tags.br(),
                "-------------------------------- CONFIRMATION (DOWN) --------------------------------", ui.tags.br(),
                "4) And once the silhouette is ready, activate the following button to lock your results:",
                style="border-left: 4px solid #ccc; padding: 10px; font-style: italic; color: #555;"
            )
        else:
            # Read the PNG file
            img_path = file_info[0]["datapath"]
            img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if input.switchFilter1():
                if input.filter1_choice() == "Manual1":
                    # print("Manual filter is selected and switch is on.")
                    # Get brightness and contrast values from inputs
                    brightness1 = input.brightness1()
                    contrast1 = input.contrast1()
                    # Apply brightness and contrast adjustments
                    alpha1 = 1 + contrast1 / 100.0  # Scaling factor
                    beta1 = brightness1  # Brightness offset
                    img_gray = cv2.convertScaleAbs(img_gray, alpha=alpha1, beta=beta1)

                if input.filter1_choice() == "Canny-Edge1":
                    # Get current threshold values
                    low_threshold1 = input.low_threshold1()
                    high_threshold1 = input.high_threshold1()

                    # Apply Canny edge detection
                    img_gray = cv2.Canny(img_gray, low_threshold1, high_threshold1)

            if input.switchColors1():
                img_gray = -img_gray + 255

            # Apply filters and treatment of data
            img_grayFiltered = np.where(img_gray < input.filter1_value() * 255 / 100, 255, 0).astype(np.uint8)

            # Convert the image to PNG and return it
            _, buffer = cv2.imencode('.png', img_grayFiltered)

            # Convert the PNG buffer to a base64 string
            image_base64 = base64.b64encode(buffer).decode('utf-8')

            # Save img_color as a .npy file
            # np.save('/path/to/save/img_color.npy', img_color)
            # Alternatively, save as PNG
            cv2.imwrite('binaryImg_front.png', img_grayFiltered)
            cv2.imwrite('img_gray.png', img_grayFiltered)

            silhouette1 = None
            # Return the HTML to display the image
            #            # Start time
            #            start_time = time.time()
            if input.actionSilhouette1():

                # Convert grayscale image to BGR for color support
                img_color = cv2.cvtColor(img_grayFiltered, cv2.COLOR_GRAY2BGR)

                subprocess.run(['python', 'SilhouetteExtraction2_1.py'], capture_output=True, text=True, check=True)

                # Load the data from the .npz file
                data = np.load('output_data.npz')

                # Extract the mFull and mReduced
                mFull1 = data['mFull']
                mReduced1 = data['mReduced']
                shapeFull1.set(mFull1.shape[0])
                shapeReduced1.set(mReduced1.shape[0])

                # Store the matrix in the reactive value
                if input.numberPoints1() == "full":
                    new_num_rows = int(input.nRelativePoints1() / 100 * shapeFull1.get())
                    #print(shapeFull1.get(),new_num_rows)
                    # Calculate the step to select rows
                    step = shapeFull1.get() // new_num_rows
                    #print(step)
                    # Select rows at equal intervals
                    nPoints_silhouette1.set(mFull1[::step])
                else:
                    new_num_rows = int(input.nRelativePoints1() / 100 * shapeReduced1.get())

                    # Calculate the step to select rows
                    step = shapeReduced1.get() // new_num_rows

                    # Select rows at equal intervals
                    nPoints_silhouette1.set(mReduced1[::step])

                # Get the matrix from reactive values
                silhouette1 = nPoints_silhouette1.get()

                #            # End time
                #            end_time = time.time()
                #            # Calculate elapsed time
                #            elapsed_time = end_time - start_time
                #            print(f"Elapsed time: {elapsed_time:.6f} seconds")

                # if silhouette1 is not None:
                # Iterate over the points and draw them with rainbow colors
                total_points = len(silhouette1)

                # Highlight points with the rainbow palette
                for i, point in enumerate(silhouette1):
                    color = get_rainbow_color(i, total_points)
                    cv2.circle(img_color, tuple(map(int, point)), radius=3, color=color, thickness=-1)

                # Convert the image to a base64 string
                _, buffer = cv2.imencode('.png', img_color)
                image_base64 = base64.b64encode(buffer).decode('utf-8')

            image_html = image_base64

            # Define the title with the slider value included
            title_html = "<h5 style='text-align: right;'>Number of points</h5>"
            if input.actionSilhouette1():
                title_html = f"<h5 style='text-align: right;'>Number of points = {total_points}</h5>"

            return ui.HTML(f'''
                    <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{image_html}" 
                     style="max-width: 100%; height: auto; border: 5px solid black; border-radius: 10px;">
            </div>
            {title_html} <!-- Title appears centered below the image -->
        </div>
            ''')

    @output
    @render.ui
    def plotImage2():

        file_info = input.image_input2()
        if file_info is None:
            return ui.tags.blockquote(
                "PLEASE, READ CAREFULLY:", ui.tags.br(),
                "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PRE-PROCESSING (LEFT) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", ui.tags.br(),
                "1) Upload a PNG or JPG file to see the image", ui.tags.br(),
                "NOTE: Be careful that the Silhouette is in White, and the Background in Black (LEFT)", ui.tags.br(),
                "2) Then, if necessary, adjust threshold and filters", ui.tags.br(),
                " ", ui.tags.br(),
                ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXTRACTION (RIGHT) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", ui.tags.br(),
                "3) Finally, activate the extraction silhouette button, select the type of silhouette", ui.tags.br(),
                "and % of points", ui.tags.br(),
                " ", ui.tags.br(),
                "-------------------------------- CONFIRMATION (DOWN) --------------------------------", ui.tags.br(),
                "4) And once the silhouette is ready, activate the following button to lock your results:",
                style="border-left: 4px solid #ccc; padding: 10px; font-style: italic; color: #555;"
            )
        else:
            # Read the PNG file
            img_path = file_info[0]["datapath"]
            img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if input.switchFilter2():
                if input.filter2_choice() == "Manual2":
                    # print("Manual filter is selected and switch is on.")
                    # Get brightness and contrast values from inputs
                    brightness2 = input.brightness2()
                    contrast2 = input.contrast2()
                    # Apply brightness and contrast adjustments
                    alpha2 = 1 + contrast2 / 100.0  # Scaling factor
                    beta2 = brightness2  # Brightness offset
                    img_gray = cv2.convertScaleAbs(img_gray, alpha=alpha2, beta=beta2)

                if input.filter2_choice() == "Canny-Edge2":
                    # Get current threshold values
                    low_threshold2 = input.low_threshold2()
                    high_threshold2 = input.high_threshold2()

                    # Apply Canny edge detection
                    img_gray = cv2.Canny(img_gray, low_threshold2, high_threshold2)

            if input.switchColors2():
                img_gray = -img_gray + 255

            # Apply filters and treatment of data
            img_grayFiltered = np.where(img_gray < input.filter2_value() * 255 / 100, 255, 0).astype(np.uint8)

            # Convert the image to PNG and return it
            _, buffer = cv2.imencode('.png', img_grayFiltered)

            # Convert the PNG buffer to a base64 string
            image_base64 = base64.b64encode(buffer).decode('utf-8')

            # Save img_color as a .npy file
            # np.save('/path/to/save/img_color.npy', img_color)
            # Alternatively, save as PNG
            cv2.imwrite('binaryImg_side.png', img_grayFiltered)
            cv2.imwrite('img_gray.png', img_grayFiltered)

            silhouette2 = None
            # Return the HTML to display the image
            #            # Start time
            #            start_time = time.time()
            if input.actionSilhouette2():

                # Convert grayscale image to BGR for color support
                img_color = cv2.cvtColor(img_grayFiltered, cv2.COLOR_GRAY2BGR)

                subprocess.run(['python', 'SilhouetteExtraction2_1.py'], capture_output=True, text=True, check=True)

                # Load the data from the .npz file
                data = np.load('output_data.npz')

                # Extract the mFull and mReduced
                mFull2 = data['mFull']
                mReduced2 = data['mReduced']
                shapeFull2.set(mFull2.shape[0])
                shapeReduced2.set(mReduced2.shape[0])

                # Store the matrix in the reactive value
                if input.numberPoints2() == "full":
                    new_num_rows = int(input.nRelativePoints2() / 100 * shapeFull2.get())
                    #print(shapeFull2.get(),new_num_rows)
                    # Calculate the step to select rows
                    step = shapeFull2.get() // new_num_rows
                    #print(step)
                    # Select rows at equal intervals
                    nPoints_silhouette2.set(mFull2[::step])
                else:
                    new_num_rows = int(input.nRelativePoints2() / 100 * shapeReduced2.get())

                    # Calculate the step to select rows
                    step = shapeReduced2.get() // new_num_rows

                    # Select rows at equal intervals
                    nPoints_silhouette2.set(mReduced2[::step])

                # Get the matrix from reactive values
                silhouette2 = nPoints_silhouette2.get()

                #            # End time
                #            end_time = time.time()
                #            # Calculate elapsed time
                #            elapsed_time = end_time - start_time
                #            print(f"Elapsed time: {elapsed_time:.6f} seconds")

                # if silhouette2 is not None:
                # Iterate over the points and draw them with rainbow colors
                total_points = len(silhouette2)

                # Highlight points with the rainbow palette
                for i, point in enumerate(silhouette2):
                    color = get_rainbow_color(i, total_points)
                    cv2.circle(img_color, tuple(map(int, point)), radius=3, color=color, thickness=-1)

                # Convert the image to a base64 string
                _, buffer = cv2.imencode('.png', img_color)
                image_base64 = base64.b64encode(buffer).decode('utf-8')

            image_html = image_base64

            # Define the title with the slider value included
            title_html = "<h5 style='text-align: right;'>Number of points</h5>"
            if input.actionSilhouette2():
                title_html = f"<h5 style='text-align: right;'>Number of points = {total_points}</h5>"

            return ui.HTML(f'''
                        <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="display: flex; justify-content: center; align-items: center;">
                    <img src="data:image/png;base64,{image_html}" 
                         style="max-width: 100%; height: auto; border: 5px solid black; border-radius: 10px;">
                </div>
                {title_html} <!-- Title appears centered below the image -->
            </div>
                ''')

    @output
    @render.ui
    def plotImage3():

        file_info = input.image_input3()
        if file_info is None:
            return ui.tags.blockquote(
                "PLEASE, READ CAREFULLY:", ui.tags.br(),
                "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PRE-PROCESSING (LEFT) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", ui.tags.br(),
                "1) Upload a PNG or JPG file to see the image", ui.tags.br(),
                "NOTE: Be careful that the Silhouette is in White, and the Background in Black (LEFT)", ui.tags.br(),
                "2) Then, if necessary, adjust threshold and filters", ui.tags.br(),
                " ", ui.tags.br(),
                ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXTRACTION (RIGHT) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", ui.tags.br(),
                "3) Finally, activate the extraction silhouette button, select the type of silhouette", ui.tags.br(),
                "and % of points", ui.tags.br(),
                " ", ui.tags.br(),
                "-------------------------------- CONFIRMATION (DOWN) --------------------------------", ui.tags.br(),
                "4) And once the silhouette is ready, activate the following button to lock your results:",
                style="border-left: 4px solid #ccc; padding: 10px; font-style: italic; color: #555;"
            )
        else:
            # Read the PNG file
            img_path = file_info[0]["datapath"]
            img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if input.switchFilter3():
                if input.filter3_choice() == "Manual3":
                    #print("Manual filter is selected and switch is on.")
                    # Get brightness and contrast values from inputs
                    brightness3 = input.brightness3()
                    contrast3 = input.contrast3()
                    # Apply brightness and contrast adjustments
                    alpha3 = 1 + contrast3 / 100.0  # Scaling factor
                    beta3 = brightness3  # Brightness offset
                    img_gray = cv2.convertScaleAbs(img_gray, alpha=alpha3, beta=beta3)

                if input.filter3_choice() == "Canny-Edge3":
                    # Get current threshold values
                    low_threshold3 = input.low_threshold3()
                    high_threshold3 = input.high_threshold3()

                    # Apply Canny edge detection
                    img_gray = cv2.Canny(img_gray, low_threshold3, high_threshold3)

            if input.switchColors3():
                img_gray = -img_gray + 255

            # Apply filters and treatment of data
            img_grayFiltered = np.where(img_gray < input.filter3_value() * 255 / 100, 255, 0).astype(np.uint8)

            # Convert the image to PNG and return it
            _, buffer = cv2.imencode('.png', img_grayFiltered)

            # Convert the PNG buffer to a base64 string
            image_base64 = base64.b64encode(buffer).decode('utf-8')

            # Save img_color as a .npy file
            # np.save('/path/to/save/img_color.npy', img_color)
            # Alternatively, save as PNG
            cv2.imwrite('binaryImg_top.png', img_grayFiltered)
            cv2.imwrite('img_gray.png', img_grayFiltered)

            # Return the HTML to display the image
#            # Start time
#            start_time = time.time()
            if input.actionSilhouette3():

                # Convert grayscale image to BGR for color support
                img_color = cv2.cvtColor(img_grayFiltered, cv2.COLOR_GRAY2BGR)

                subprocess.run(['python', 'SilhouetteExtraction2_1.py'], capture_output=True, text=True, check=True)

                # Load the data from the .npz file
                data = np.load('output_data.npz')

                # Extract the mFull and mReduced
                mFull3 = data['mFull']
                mReduced3 = data['mReduced']
                shapeFull3.set(mFull3.shape[0])
                shapeReduced3.set(mReduced3.shape[0])

                # Store the matrix in the reactive value
                if input.numberPoints3() == "full":
                    new_num_rows = int(input.nRelativePoints3() / 100 * shapeFull3.get())
                    #print(shapeFull3.get(),new_num_rows)
                    # Calculate the step to select rows
                    step = shapeFull3.get() // new_num_rows
                    #print(step)
                    # Select rows at equal intervals
                    nPoints_silhouette3.set(mFull3[::step])
                else:
                    new_num_rows = int(input.nRelativePoints3() / 100 * shapeReduced3.get())

                    # Calculate the step to select rows
                    step = shapeReduced3.get() // new_num_rows

                    # Select rows at equal intervals
                    nPoints_silhouette3.set(mReduced3[::step])

                # Get the matrix from reactive values
                silhouette3 = nPoints_silhouette3.get()

#            # End time
#            end_time = time.time()
#            # Calculate elapsed time
#            elapsed_time = end_time - start_time
#            print(f"Elapsed time: {elapsed_time:.6f} seconds")

            #if silhouette3 is not None:
                # Iterate over the points and draw them with rainbow colors
                total_points = len(silhouette3)

                # Highlight points with the rainbow palette
                for i,point in enumerate(silhouette3):
                    color = get_rainbow_color(i, total_points)
                    cv2.circle(img_color, tuple(map(int, point)), radius=3, color=color, thickness=-1)

                # Convert the image to a base64 string
                _, buffer = cv2.imencode('.png', img_color)
                image_base64 = base64.b64encode(buffer).decode('utf-8')

            image_html = image_base64

            # Define the title with the slider value included
            title_html = "<h5 style='text-align: right;'>Number of points</h5>"
            if input.actionSilhouette3():
                title_html = f"<h5 style='text-align: right;'>Number of points = {total_points}</h5>"

            return ui.HTML(f'''
                    <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{image_html}" 
                     style="max-width: 100%; height: auto; border: 5px solid black; border-radius: 10px;">
            </div>
            {title_html} <!-- Title appears centered below the image -->
        </div>
            ''')

    # Observe the switch button state and update the CSS class of the panel
    @reactive.Effect
    async def update_panel_class1():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readySilhouette1():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette1_1", "class_name": "panel-sidebar-inactive"}
            )
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette1_2", "class_name": "panel-sidebar-inactive"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette1_1", "class_name": "panel-sidebar-active"}
            )
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette1_2", "class_name": "panel-sidebar-active"}
            )

    # Observe the switch button state and update the CSS class of the panel
    @reactive.Effect
    async def update_panel_class2():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readySilhouette2():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette2_1", "class_name": "panel-sidebar-inactive"}
            )
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette2_2", "class_name": "panel-sidebar-inactive"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette2_1", "class_name": "panel-sidebar-active"}
            )
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette2_2", "class_name": "panel-sidebar-active"}
            )

    # Observe the switch button state and update the CSS class of the panel
    @reactive.Effect
    async def update_panel_class3():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readySilhouette3():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette3_1", "class_name": "panel-sidebar-inactive"}
            )
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette3_2", "class_name": "panel-sidebar-inactive"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette3_1", "class_name": "panel-sidebar-active"}
            )
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedSilhouette3_2", "class_name": "panel-sidebar-active"}
            )

    # Observe the switch button state and update the CSS class of the panel
    @reactive.Effect
    async def update_panel_finalSilhouette():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readySilhouette1() and input.readySilhouette2() and input.readySilhouette3()\
                and input.actionSilhouette1() and input.actionSilhouette2() and input.actionSilhouette3():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedStep1", "class_name": "btn-primary1-active"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedStep1", "class_name": "btn-primary1-inactive"}
            )


    @output
    @render.ui
    def plot1():

        file_info = input.file_input1()
        if file_info is None:
            return ui.tags.blockquote(
                "PLEASE, READ CAREFULLY:", ui.tags.br(),
                "1) Upload a CSV file to see the silhouette.", ui.tags.br(),
                "NOTE: If the silhouette was reconstructed by this GUI, then load finalSilhouette_FRONT.csv.", ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "2) Then, define the length in each direction.", ui.tags.br(),
                "NOTE: Be careful that silhouettes intersect each other.", ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "3) Finally, select the method to interpolate the silhouette points.", ui.tags.br(),
                "NOTE: If the silhouette is very wrinkled and was full reconstructed, then lineal method is recommended.",
                ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "4) And once those parameters are set, activate the following button to lock your results:",
                style="border-left: 4px solid #ccc; padding: 10px; font-style: italic; color: #555;"
            )

        # Read the CSV file
        file_content = file_info[0]["datapath"]
        df = pd.read_csv(file_content)

        # Get the input values
        num1_min = input.num1_min()
        num1_max = input.num1_max()

        num2_min = input.num2_min()
        num2_max = input.num2_max()

        filtered_df = (df - df.min()) / (df.max() - df.min())
        filtered_df.iloc[:, 0] = filtered_df.iloc[:, 0] * (num1_max - num1_min) + num1_min
        filtered_df.iloc[:, 1] = filtered_df.iloc[:, 1] * (num2_max - num2_min) + num2_min

        # Generate the plot
        fig = px.scatter(filtered_df, x=filtered_df.columns[0], y=filtered_df.columns[1], color_discrete_sequence = ['cyan'])

        # Update the layout to change the background color
        fig.update_layout(
            plot_bgcolor='#333333',  # Dark grey background for the plotting area
            paper_bgcolor='#e6ffe6',  # Light green background for the entire figure
            xaxis_title="Y-direction",  # Custom X axis label
            yaxis_title="Z-direction",  # Custom Y axis label
            font=dict(
                family="'Cinzel Decorative', cursive",
                size=12
            )
        )
        # Setting equal aspect ratio for the axes
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        fig.update_xaxes(constrain='domain')

        fig_html = fig.to_html(full_html=False)
        return ui.HTML(fig_html)

    @output
    @render.ui
    def plot2():

        file_info = input.file_input2()
        if file_info is None:
            return ui.tags.blockquote(
                "PLEASE, READ CAREFULLY:", ui.tags.br(),
                "1) Upload a CSV file to see the silhouette.", ui.tags.br(),
                "NOTE: If the silhouette was reconstructed by this GUI, then load finalSilhouette_SIDE.csv.", ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "2) Then, define the length in each direction.", ui.tags.br(),
                "NOTE: Be careful that silhouettes intersect each other.", ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "3) Finally, select the method to interpolate the silhouette points.", ui.tags.br(),
                "NOTE: If the silhouette is very wrinkled and was full reconstructed, then lineal method is recommended.",
                ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "4) And once those parameters are set, activate the following button to lock your results:",
                style="border-left: 4px solid #ccc; padding: 10px; font-style: italic; color: #555;"
            )

        # Read the CSV file
        file_content = file_info[0]["datapath"]
        df = pd.read_csv(file_content)

        # Get the input values
        num3_min = input.num3_min()
        num3_max = input.num3_max()

        num4_min = input.num4_min()
        num4_max = input.num4_max()

        filtered_df = (df - df.min()) / (df.max() - df.min())
        filtered_df.iloc[:, 0] = filtered_df.iloc[:, 0] * (num3_max - num3_min) + num3_min
        filtered_df.iloc[:, 1] = filtered_df.iloc[:, 1] * (num4_max - num4_min) + num4_min

        # Generate the plot
        fig = px.scatter(filtered_df, x=filtered_df.columns[0], y=filtered_df.columns[1], color_discrete_sequence = ['cyan'])

        # Update the layout to change the background color
        fig.update_layout(
            plot_bgcolor='#333333',  # Dark grey background for the plotting area
            paper_bgcolor='#e6ffe6',  # Light green background for the entire figure
            xaxis_title="X-direction",  # Custom X axis label
            yaxis_title="Z-direction",  # Custom Y axis label
            font=dict(
                family="'Cinzel Decorative', cursive",
                size=12
            )
        )
        # Setting equal aspect ratio for the axes
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        fig.update_xaxes(constrain='domain')

        fig_html = fig.to_html(full_html=False)
        return ui.HTML(fig_html)

    @output
    @render.ui
    def plot3():

        file_info = input.file_input3()
        if file_info is None:
            return ui.tags.blockquote(
                "PLEASE, READ CAREFULLY:", ui.tags.br(),
                "1) Upload a CSV file to see the silhouette.", ui.tags.br(),
                "NOTE: If the silhouette was reconstructed by this GUI, then load finalSilhouette_TOP.csv.", ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "2) Then, define the length in each direction.", ui.tags.br(),
                "NOTE: Be careful that silhouettes intersect each other.", ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "3) Finally, select the method to interpolate the silhouette points.", ui.tags.br(),
                "NOTE: If the silhouette is very wrinkled and was full reconstructed, then lineal method is recommended.",
                ui.tags.br(),
                "-------------------------", ui.tags.br(),
                "4) And once those parameters are set, activate the following button to lock your results:",
                style="border-left: 4px solid #ccc; padding: 10px; font-style: italic; color: #555;"
            )

        # Read the CSV file
        file_content = file_info[0]["datapath"]
        df = pd.read_csv(file_content)

        # Get the input values
        num5_min = input.num5_min()
        num5_max = input.num5_max()

        num6_min = input.num6_min()
        num6_max = input.num6_max()

        # Filter the data based on the numeric input values
        # filtered_df = df[(df.iloc[:, 0] >= num1_min) & (df.iloc[:, 0] <= num1_max)]

        filtered_df = (df - df.min()) / (df.max() - df.min())
        filtered_df.iloc[:, 0] = filtered_df.iloc[:, 0] * (num5_max - num5_min) + num5_min
        filtered_df.iloc[:, 1] = filtered_df.iloc[:, 1] * (num6_max - num6_min) + num6_min

        # Calculate the data range
        x_range = filtered_df.iloc[:, 0].max() - filtered_df.iloc[:, 0].min()
        y_range = filtered_df.iloc[:, 1].max() - filtered_df.iloc[:, 1].min()
        max_range = max(x_range, y_range)

        # Generate the plot
        fig = px.scatter(filtered_df, x=filtered_df.columns[0], y=filtered_df.columns[1], color_discrete_sequence = ['cyan'])

        # Update the layout to change the background color
        fig.update_layout(
            plot_bgcolor='#333333',  # Dark grey background for the plotting area
            paper_bgcolor='#e6ffe6',  # Light green background for the entire figure
            xaxis_title="X-direction",  # Custom X axis label
            yaxis_title="Y-direction",  # Custom Y axis label
            font=dict(
                family="'Cinzel Decorative', cursive",
                size=12
            )
        )
        # Setting equal aspect ratio for the axes
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        fig.update_xaxes(constrain='domain')

        fig_html = fig.to_html(full_html=False)
        return ui.HTML(fig_html)

    #@output
    #@render.ui
    #def dynamic_panel1():
    #    if not input.switch1():
    #        return None
    #
    #    return ui.div(
    #        ui.input_numeric("num_fields1", "Number of Holes", 1, min=1, step=1),
    #        ui.output_ui("additional_inputs1"),
    #        class_="panel"
    #    )

    #@output
    #@render.ui
    #def additional_inputs1():
    #    num_fields1 = input.num_fields1()
    #    inputs1 = []
    #    for i in range(num_fields1):
    #        inputs1.append(
    #            ui.div(
    #                ui.input_numeric(f"input1_x_{i}", f"X{i+1}", 0),
    #                ui.input_numeric(f"input1_y_{i}", f"Y{i+1}", 0),
    #                class_="coordinate-inputs"
    #            )
    #        )
    #    return ui.div(*inputs1)

    #@output
    #@render.ui
    #def dynamic_panel2():
    #    if not input.switch2():
    #        return None
    #
    #    return ui.div(
    #        ui.input_numeric("num_fields2", "Number of Holes", 1, min=1, step=1),
    #        ui.output_ui("additional_inputs2"),
    #        class_="panel"
    #    )

    #@output
    #@render.ui
    #def additional_inputs2():
    #    num_fields2 = input.num_fields2()
    #    inputs2 = []
    #    for i in range(num_fields2):
    #        inputs2.append(
    #            ui.div(
    #                ui.input_numeric(f"input2_x_{i}", f"X{i+1}", 0),
    #                ui.input_numeric(f"input2_y_{i}", f"Y{i+1}", 0),
    #                class_="coordinate-inputs"
    #            )
    #        )
    #    return ui.div(*inputs2)

    #@output
    #@render.ui
    #def dynamic_panel3():
    #    if not input.switch3():
    #        return None
    #
    #    return ui.div(
    #        ui.input_numeric("num_fields3", "Number of Holes", 1, min=1, step=1),
    #        ui.output_ui("additional_inputs3"),
    #        class_="panel"
    #    )

    #@output
    #@render.ui
    #def additional_inputs3():
    #    num_fields3 = input.num_fields3()
    #    inputs3 = []
    #    for i in range(num_fields3):
    #        inputs3.append(
    #            ui.div(
    #                ui.input_numeric(f"input3_x_{i}", f"X{i+1}", 0),
    #                ui.input_numeric(f"input3_y_{i}", f"Y{i+1}", 0),
    #                class_="coordinate-inputs"
    #            )
    #        )
    #    return ui.div(*inputs3)

    # Observe the switch button state and update the CSS class of the panel
    @reactive.Effect
    async def update_panel_object1():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readyObject1():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedObject1", "class_name": "panel-sidebar-inactive"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedObject1", "class_name": "panel-sidebar-active"}
            )

    @reactive.Effect
    async def update_panel_object2():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readyObject2():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedObject2", "class_name": "panel-sidebar-inactive"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedObject2", "class_name": "panel-sidebar-active"}
            )

    @reactive.Effect
    async def update_panel_object3():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readyObject3():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedObject3", "class_name": "panel-sidebar-inactive"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedObject3", "class_name": "panel-sidebar-active"}
            )

    @reactive.Effect
    async def update_panel_finalObject():

        # Apply the class by setting a style (workaround for full class replacement)
        # Update the style directly within the div (no direct method to change the class)
        if input.readyObject1() and input.readyObject2() and input.readyObject3():
            # When switch is OFF, display the panel fully
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedStep2", "class_name": "btn-primary1-active"}
            )
        else:
            # When switch is ON, show the panel with reduced opacity and disable interaction
            await session.send_custom_message(
                "set_class",
                {"element_id": "finishedStep2", "class_name": "btn-primary1-inactive"}
            )



    @output
    @render.ui
    def dynamic_panelFilter1():
        if not input.switchFilter1():
            return None

        return ui.div(
            ui.input_radio_buttons("filter1_choice", "Filter Method:",
                                   choices={"Manual1": "brightness-contrast", "Canny-Edge1": "canny-edge (Gaussian)"},
                                   selected="Manual1"),
            ui.output_ui("additional_inputsFilter1"),
            class_="panel"
        )

    @output
    @render.ui
    def dynamic_panelFilter2():
        if not input.switchFilter2():
            return None

        return ui.div(
            ui.input_radio_buttons("filter2_choice", "Filter Method:",
                                   choices={"Manual2": "brightness-contrast", "Canny-Edge2": "canny-edge (Gaussian)"},
                                   selected="Manual2"),
            ui.output_ui("additional_inputsFilter2"),
            class_="panel"
        )

    @output
    @render.ui
    def dynamic_panelFilter3():
        if not input.switchFilter3():
            return None

        return ui.div(
            ui.input_radio_buttons("filter3_choice", "Filter Method:",
                                   choices={"Manual3": "brightness-contrast", "Canny-Edge3": "canny-edge (Gaussian)"},
                                   selected="Manual3"),
            ui.output_ui("additional_inputsFilter3"),
            class_="panel"
        )

    @output
    @render.ui
    def additional_inputsFilter1():
        filter1 = input.filter1_choice()

        if filter1 == "Manual1":
            return ui.div(
                ui.input_slider("brightness1", "Brightness", min=-100, max=100, value=0),
                ui.input_slider("contrast1", "Contrast", min=-100, max=100, value=0),
            )
        if filter1 == "Canny-Edge1":
            return ui.div(
                ui.input_slider("low_threshold1", "Low Threshold", min=0, max=255, value=50),
                ui.input_slider("high_threshold1", "High Threshold", min=0, max=255, value=150)
            )

    @output
    @render.ui
    def additional_inputsFilter2():
        filter2 = input.filter2_choice()

        if filter2 == "Manual2":
            return ui.div(
                ui.input_slider("brightness2", "Brightness", min=-100, max=100, value=0),
                ui.input_slider("contrast2", "Contrast", min=-100, max=100, value=0),
            )
        if filter2 == "Canny-Edge2":
            return ui.div(
                ui.input_slider("low_threshold2", "Low Threshold", min=0, max=255, value=50),
                ui.input_slider("high_threshold2", "High Threshold", min=0, max=255, value=150)
            )

    @output
    @render.ui
    def additional_inputsFilter3():
        filter3 = input.filter3_choice()

        if filter3 == "Manual3":
            return ui.div(
                ui.input_slider("brightness3", "Brightness", min=-100, max=100, value=0),
                ui.input_slider("contrast3", "Contrast", min=-100, max=100, value=0),
            )
        if filter3 == "Canny-Edge3":
            return ui.div(
                ui.input_slider("low_threshold3", "Low Threshold", min=0, max=255, value=50),
                ui.input_slider("high_threshold3", "High Threshold", min=0, max=255, value=150)
            )

    @output
    @render.ui
    def dynamic_panelSilhouette1():
        if not input.actionSilhouette1():
            return None

        return ui.div(
            ui.input_radio_buttons("numberPoints1", "Type of silhouette:",
                                   choices={"full": "Full", "partial": "Optimized"},
                                   selected="full"),
            ui.input_slider("nRelativePoints1", "Number of points (%) :", min=1, max=100, value=100),
                             class_="panel"
        )


    @output
    @render.ui
    def dynamic_panelSilhouette2():
        if not input.actionSilhouette2():
            return None

        return ui.div(
            ui.input_radio_buttons("numberPoints2", "Type of silhouette:",
                                   choices={"full": "Full", "partial": "Optimized"},
                                   selected="full"),
            ui.input_slider("nRelativePoints2", "Number of points (%) :", min=1, max=100, value=100),
            class_="panel"
        )

    @output
    @render.ui
    def dynamic_panelSilhouette3():
        if not input.actionSilhouette3():
            return None

        return ui.div(
            ui.input_radio_buttons("numberPoints3", "Type of silhouette:",
                                   choices={"full": "Full", "partial": "Optimized"},
                                   selected="full"),
            ui.input_slider("nRelativePoints3", "Number of points (%) :", min=1, max=100, value=100),
            class_="panel"
        )

    #@output
    #@render.ui
    #def dynamic_panelSilhouette3():
    #    if not input.actionSilhouette3():
    #        return None
    #
    #    return ui.div(
    #        ui.input_slider("numberPoints3", "Number of silhouette points:", shapeReduced3.get(), shapeFull3.get(), shapeReduced3.get())
    #    )

    #@reactive.Effect
    #@reactive.event(input.numberPoints3)
    #def run_external_script():
    #    # Run the external script
    #    # result = subprocess.run(['python', 'SilhouetteExtraction1_1.py'], capture_output=True, text=True, check=True)
    #
    #    print(shapeReduced3.get())
    #    print(shapeFull3.get())



    @reactive.Effect
    @reactive.event(input.run_freecad)  # Only trigger when the button is clicked
    def run_freecad():

        num1_min = input.num1_min()
        num1_max = input.num1_max()
        num2_min = input.num2_min()
        num2_max = input.num2_max()
        num3_min = input.num3_min()
        num3_max = input.num3_max()
        num4_min = input.num4_min()
        num4_max = input.num4_max()
        num5_min = input.num5_min()
        num5_max = input.num5_max()
        num6_min = input.num6_min()
        num6_max = input.num6_max()
        interpolation1 = input.interpolation1_choice()
        interpolation2 = input.interpolation2_choice()
        interpolation3 = input.interpolation3_choice()
        fileFront_info = input.file_input1()
        fileSide_info = input.file_input2()
        fileTop_info = input.file_input3()
        print(fileFront_info)
        # Read again the CSV file
        csvFront_path = fileFront_info[0]["name"]
        csvSide_path = fileSide_info[0]["name"]
        csvTop_path = fileTop_info[0]["name"]

        command = [freecad_path, script_path, csvFront_path, csvSide_path, csvTop_path,
                   str(num1_min), str(num1_max), str(num2_min), str(num2_max), str(num3_min), str(num3_max),
                   str(num4_min), str(num4_max), str(num5_min), str(num5_max), str(num6_min), str(num6_max),
                   interpolation1, interpolation2, interpolation3]

        # Use subprocess.Popen to execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to finish and capture the output
        output, error = process.communicate()

        # Print the output and error
        print("Output:")
        print(output.decode("utf-8"))
        print("Error:")
        print(error.decode("utf-8"))

# Create the main app
app = App(main_ui, server)

# Run the main app
if __name__ == "__main__":
    app.run()