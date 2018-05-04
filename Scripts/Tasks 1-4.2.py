"""
This is the solution for the Processing Framework: Automating Tasks with Pythong workshop for the GeoPython Conference 2018
Author: Kang Zi Jing
GitHub repository: [link]

This covers the solution up till Task 4.2. These lines of code are what you should enter into your QGIS Python Console to follow the problem tasks.
This source code is intentionally written with bad practice and non-reusability and non-modularity as it seeks to help entry-level Python users to learn the language. If you are looking for the Master Script, Interactable Script, or solution to Task 4.2 onwards which uses more reusable code through defining method calls, check the GitHub repository again. 
If you are experienced in Python or other programming languages and familiar with methon calls and definition, feel free to skip this script.
"""

""" Import data libraries """
from qgis import core
from PyQt5.QtWidgets import *
from qgis.utils import iface
from qgis.core import QgsProject
import processing


""" Task 1. Adding Geopackae as Layers into QGIS """


""" 1.2. Creating a Dialog Box to ask for User Input on File to Add """
envPath = QFileDialog.getOpenFileName(QFileDialog(), "Environment Layer Select", "C:\\")[0]

""" 1.3. Adding Vector Layers into QGIS """
env = iface.addVectorLayer(envPath, "", "ogr")
env.setName("Environment")

atbnPath = QFileDialog.getOpenFileName(QFileDialog(), "Autobahn Layer Select", "C:\\")[0]
atbn = iface.addVectorLayer(atbnPath, "", "ogr")
atbn.setName("Autobahn")


""" Task 2. Adding Buffers to Autobahn Layer """


""" 2.3. Creating a Buffer with a Standalone Script """
""" This line can be ignored since we previously already declared \atbn\ but if not, we can declare it again with:
atbn = QgsProject.instance().mapLayersByName("Autobahn")[0] """
param = { 'INPUT' : atbn, 'DISTANCE' : 20, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
algoOutput = processing.run("qgis:buffer", param)
autobahn20 = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
autobahn20.setName("Autobahn 20")

""" 2.4. Creating 2 more Buffers """
param = { 'INPUT' : autobahn20, 'DISTANCE' : 100, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
algoOutput = processing.run("qgis:buffer", param)
autobahn100 = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
autobahn100.setName("Autobahn 100")

param = { 'INPUT' : autobahn100, 'DISTANCE' : 200, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
algoOutput = processing.run("qgis:buffer", param)
autobahn300 = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
autobahn300.setName("Autobahn 300")


""" Task 3. Performing Union on the Buffer Areas """
param = { 'INPUT' : autobahn20, 'OVERLAY' : autobahn100, 'OUTPUT' : 'memory:' }
algoOutput = processing.run("qgis:union", param)
innerImpactArea = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
innerImpactArea.setName("Inner Impact Area")

param = { 'INPUT' : innerImpactArea, 'OVERLAY' : autobahn300, 'OUTPUT' : 'memory:' }
algoOutput = processing.run("qgis:union", param)
impactArea = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
impactArea.setName("Impact Area")


""" Task 4. Refining Code """


""" 4.1. Performing Intersection on Environment and Impact Area """
def intersect_layers(layer1, layer2, outputName):
    param = param = { 'INPUT' : layer1, 'OVERLAY' : layer2, 'INPUT_FIELDS' : [], 'OVERLAY_FIELDS' : [], 'OUTPUT' : 'memory:' }
    intxnOp = QgsProject.instance().addMapLayer(processing.run("qgis:intersection", param)['OUTPUT'])
    intxnOp.setName(outputName)
    
""" This is an example of defining a method or function. This encourages the reusability of code as it can work with any form of inputs and outputs you can specify. All you need to do is to declare your variables before passing them through the method as \layer1\, 'layer2\ and \outputName\, which are the parameters you defined for the method. """

outputName = "Intersected"

intersect_layers(env, impactArea, outputName)
intersected = QgsProject.instance().mapLayersByName(outputName)

""" 4.2. Method Definition for Previous Tasks
The suggested solution for Task 4.2 onwards would be in another script as we try to refine and clean up the code by introducing reusability and modularity though method definitions """