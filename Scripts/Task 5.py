"""
This is the suggested solution for the Processing Framework: Automating Tasks with Pythong workshop for the GeoPython Conference 2018
Author: Kang Zi Jing
GitHub repository: [link]

This are the function definitions that follow the problem tasks. To use: run this script on your QGIS Python console and call the functions with the respective parameters.
This source code is written without a Class definition as I believe that not more than 1 Environment layer would be analyzed per project, but if needed, feel free to edit the code to be a Class definition for better encapsulation and modularity. If you are looking for the Master Script, Interactable Script, or the straightforward solutions (what to type on the console, which is better for beginners), check the GitHub repository again. 
If you are experienced in Python or other programming languages and familiar with methon calls and definition, feel free to skip this script and go into the bonus scripts.
"""

""" Import data libraries """
from qgis import core
from PyQt5.QtWidgets import *
from qgis.utils import iface
from qgis.core import QgsProject
import processing


""" Quality of Life Function(s) 
    Defined to make life easier than calling the entire method of a class """
def get_layer(layerName):
    """ returns the vector layer object of the name in string pass as parameter 
        basically a short version to write QgsProject.instance().mapLayersByName(layerName)[0] """
    return QgsProject.instance().mapLayersByName(layerName)[0]
    

""" Task 1. Adding Geopackage as Layers into QGIS """


def add_layer(layerName):
    layerPath = QFileDialog.getOpenFileName(QFileDialog(), "Geopackage Select", "C:\\")[0]
    layer = iface.addVectorLayer(layerPath, "", "ogr")
    layer.setName(layerName)
""" Note that after this function is called, you have to assign the layers to  variables so that you can pass them into the next few functions. Of course, there are ways to go about doing this so that you do not need to repetitively assign new layers, but we shall not explore that in this script. """


""" Task 2. Adding Buffers """


def add_buffer(vLayer, dist, outputName):
    param = { 'INPUT' : vLayer, 'DISTANCE' : dist, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
    algoOutput = processing.run("qgis:buffer", param)
    bufferResult = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
    bufferResult.setName(outputName)
""" Once again, as this script's aim is to explore the modularity of functions, there's no automation in parsing through the resultant layers. For that, you can check the following script.

    Another way which may simplify things than declaring every variable is to parse the results like this:
    
    atbn = get_layer("Autobahn")
    add_buffer(atbn, 20, "Autobahn 20")
    add_buffer(get_layer("Autobahn 20")[0], 100, "Autobahn 100")
    add_buffer(get_layer("Autobahn 100"), 200, "Autobahn 300") 
    """

""" Task 3. Performing Unions """


def perform_union(layer1, layer2, outputName):
    param = { 'INPUT' : layer1, 'OVERLAY' : layer2, 'OUTPUT' : 'memory:' }
    algoOutput = processing.run("qgis:union", param)
    unionResult = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
    unionResult.setName(outputName)
    
    
""" Task 4. Calling Intersections """


def call_intersection(layer, overlay, outputName):
    param = param = { 'INPUT' : layer, 'OVERLAY' : overlay, 'INPUT_FIELDS' : [], 'OVERLAY_FIELDS' : [], 'OUTPUT' : 'memory:' }
    intxnResult = QgsProject.instance().addMapLayer(processing.run("qgis:intersection", param)['OUTPUT'])
    intxnResult.setName(outputName)
    
    
""" Task 5. Query Features """


def query_features(layer, expr, outputName):
    querySelect = layer.getFeatures(QgsFeatureRequest(expr))
    ids = [i.id() for i in layer.getFeatures(QgsFeatureRequest(expr))]
    layer.selectByIds(ids)
    result = layer.materialize(QgsFeatureRequest().setFilterFids(layer.selectedFeatureIds()))
    QgsProject.instance().addMapLayer(result)
    layer.selectByIds([])
    result.setName(outputName)