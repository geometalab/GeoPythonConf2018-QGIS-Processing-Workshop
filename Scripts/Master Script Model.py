"""
This is the suggested solution for the Processing Framework: Automating Tasks with Pythong workshop for the GeoPython Conference 2018
Author: Kang Zi Jing
GitHub repository: [link]

This is a interactive script that takes from the users some inputs, i.e. filepath of the Environment gpkg, Autobahn gpkg, and then it does the rest without much more prompt.
This source code is written with a Class definition, as it asks for a user input for the file path and then consequently carries out the rest of the methods, for better encapsulation, modularity, and reusability. If you are looking for the task by task solutions (what to type on the console, which is better for beginners), or the function definitions, check the GitHub repository again. 
"""

""" Import data libraries """
from qgis import core
from PyQt5.QtWidgets import *
from qgis.utils import iface
from qgis.core import QgsProject
import processing

class HabitatAnalyzer:
    """Declaring a class for code cleanliness, encapsulation and modularity. Also allows for better organization and clarity when more than an analysis needs to be performed.
    The following are methods that an instance of HabitatAnalyzer can call.
    When 'HabitatAnalyzer(iface)' is called, the iface referred to would be used to create an instance of HabitatAnalyzer with __init__() method
    The other methods help move the script through our workflow. They can be called in success to one another with the method run_script() but can also be called inidividually by their method names if desired"""
    
    def __init__(self, iface):
        self.iface = iface
    
    """The following 4 methods are just a repackage of library included GUI user-input functions. I rewrote them as class methods to shorten them and make them more readable."""
    
    def question(self, title, content):
        return QMessageBox.question(iface.mainWindow(), title, content, QMessageBox.Yes, QMessageBox.No)
        
    def information(self, title, content):
        return QMessageBox.information(iface.mainWindow(), title, content)
        
    def fileDialog(self, title):
        return QFileDialog.getOpenFileName(QFileDialog(), title, "%APPDATA%")

    def inputDialog(self, inputType, title, content):
        if (inputType == 1):
            return QInputDialog.getText(iface.mainWindow(), title, content)
        if (inputType == 2):
            return QInputDialog.getInt(iface.mainWindow(), title, content)
        
    def welcome(self):
        self.information("Habitat Analyzer", "Welcome to Habitat Analyzer")
        return self.question("Habitat Analyzer", "Would you like to run the script?")
      
    def check_layer_exists(self, layerName):
        return (len(QgsProject.instance().mapLayersByName(layerName)))
    
    """The following methods are the core methods to help us move through our workflow. Should be essentially similar to the ones we used in the previous 2 scripts, just that these allow a bit more room for interactivity and user input by having altered parameters"""
    
    def load_layers(self, type):    
        answer = QMessageBox.No
        while (answer == QMessageBox.No):
            self.information("File Select", "Select your " + type + " layer from a Geopackage")
            input = self.fileDialog("File Select")[0]
            while (input[-5:] != ".gpkg"):
                self.information("Invalid Geopackage", "That is not a .gpkg file! Please reselect!")
                input = self.fileDialog("File Select")[0]
            answer = self.question("Confirmation", "Is " + input + " the correct file?")
            if answer == QMessageBox.Yes:
                inputAnswer = self.inputDialog(1, "Layer Name", "Name your layer: ")
                layer = iface.addVectorLayer(input, "", "ogr")
                if ((inputAnswer[1]) == True):
                    layer.setName(inputAnswer[0])
                break
            self.information("Reselect", "Please select the correct " + type + " file!")
            
    def buffer_creation(self):
        answer = self.question("Buffer Creation", "Would you like to create a buffer?")
        if answer == QMessageBox.Yes:
            bufferNumber = self.inputDialog(2, "Buffer Creation", "How many buffers do you want to create?")
        for x in range(0, (bufferNumber[0])):
            
            layerInput = self.inputDialog(1, "Buffer %d" % (x+1), "Enter the name of your layer to be buffered: ")
            while ((layerInput[1] == True) and (len(QgsProject.instance().mapLayersByName(layerInput[0])) == 0)):
                self.information("Error", "There is no layer named " + layerInput[0] + "!")
                layerInput = self.inputDialog(1, "Buffer %d" % (x+1), "Enter the name of your layer to be buffered: ")
            if layerInput[1] == False:
                break
            layerName = layerInput[0]
            bufferDist = self.inputDialog(2, "Buffer %d" % (x+1), "Enter the distance to buffer: ")[0]
            param = { 'INPUT' : QgsProject.instance().mapLayersByName(layerName)[0], 'DISTANCE' : bufferDist, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
            bufferLayer = QgsProject.instance().addMapLayer(processing.run("qgis:buffer", param)['OUTPUT'])
            inputAnswer = self.inputDialog(1, "Layer Name", "Name the output buffer layer: ")
            if (inputAnswer[1] == True):
                bufferLayer.setName(inputAnswer[0])
    
    def old_buffer_creation(self):
        answer = self.question("Buffer Creation", "Would you like to create a buffer?")
        if answer == QMessageBox.Yes:
            bufferNumber = self.inputDialog(2, "Buffer Creation", "How many buffers do you want to create?")
            print("Input selected: " + str(bufferNumber[0]))
        for x in range(0, (bufferNumber[0])):
            
            layerName = self.inputDialog(1, "Buffer %d" % x, "Enter the name of your layer to be buffered: ")
            if (layerName[1] == QMessageBox.Cancel):
                break
            while (len(QgsProject.instance().mapLayersByName(layerName[0])) == 0):
                if (layerName[1] == QMessageBox.Cancel):
                    break
                self.information("Error", "There is no layer named " + layerName[0] + "!")
                layerName = self.inputDialog(1, "Buffer %d" % x, "Enter the name of your layer to be buffered: ")
            bufferDist = self.inputDialog(2, "Buffer %d" % x, "Enter the distance to buffer: ")[0]
            while (len(layerName) != 0):
                param = { 'INPUT' : QgsProject.instance().mapLayersByName(layerName[0])[0], 'DISTANCE' : bufferDist, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
                bufferLayer = QgsProject.instance().addMapLayer(processing.run("qgis:buffer", param)['OUTPUT'])
                inputAnswer = self.inputDialog(1, "Layer Name", "Name the output buffer layer: ")
                if (inputAnswer[1] == True):
                    bufferLayer.setName(inputAnswer[0])
                if (len(layerName) == 0):
                    self.information("Error!", "The layer name you gave does not exist! Try again!")
                    
    def perform_union(self):
        answer = self.question("Union Creation", "Would you like to union 2 layers?")
        if answer == QMessageBox.Yes:
            layer1 = self.inputDialog(1, "Layer 1", "Enter the name of your first/base layer: ")
            while ((layer1[1] == True) and (len(QgsProject.instance().mapLayersByName(layer1[0])) == 0)):
                self.information("Error", "There is no layer named " + layer1[0] + "!")
                layer1 = self.inputDialog(1, "Layer 1", "Enter the name of your first/base layer: ")
            if (layer1[1] == True):
                layer2 = self.inputDialog(1, "Layer 2", "Enter the name of your second/overlay layer: ")
                while ((layer2[1] == True) and (len(QgsProject.instance().mapLayersByName(layer2[0])) == 0)):
                    self.information("Error", "There is no layer named " + layer2[0] + "!")
                    layer2 = self.inputDialog(1, "Layer 2", "Enter the name of your second/overlay layer: ")
                if (layer2[1] == True):
                    param = { 'INPUT' : QgsProject.instance().mapLayersByName(layer1[0])[0], 'OVERLAY' : QgsProject.instance().mapLayersByName(layer2[0])[0], 'OUTPUT' : 'memory:' }
                    algoOutput = processing.run("qgis:union", param)
                    unionResult = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
                    outputName = self.inputDialog(1, "Layer Name", "Name the output union layer: ")
                    if (outputName[1] == True):
                        unionResult.setName(outputName[0])
                        
    def perform_intersection(self):
        answer = self.question("Intersect Layers", "Would you like to intersect 2 layers?")
        if answer == QMessageBox.Yes:
            layer1 = self.inputDialog(1, "Layer 1", "Enter the name of your first/base layer: ")
            while ((layer1[1] == True) and (len(QgsProject.instance().mapLayersByName(layer1[0])) == 0)):
                self.information("Error", "There is no layer named " + layer1[0] + "!")
                layer1 = self.inputDialog(1, "Layer 1", "Enter the name of your first/base layer: ")
            if (layer1[1] == True):
                layer2 = self.inputDialog(1, "Layer 2", "Enter the name of your second/overlay layer: ")
                while ((layer2[1] == True) and (len(QgsProject.instance().mapLayersByName(layer2[0])) == 0)):
                    self.information("Error", "There is no layer named " + layer2[0] + "!")
                    layer2 = self.inputDialog(1, "Layer 2", "Enter the name of your second/overlay layer: ")
                if (layer2[1] == True):
                    param = { 'INPUT' : QgsProject.instance().mapLayersByName(layer1[0])[0], 'OVERLAY' : QgsProject.instance().mapLayersByName(layer2[0])[0], 'INPUT_FIELDS' : [], 'OVERLAY_FIELDS' : [], 'OUTPUT' : 'memory:' }
                    algoOutput = processing.run("qgis:intersection", param)
                    intersectResult = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
                    outputName = self.inputDialog(1, "Layer Name", "Name the output intersected layer: ")
                    if (outputName[1] == True):
                        intersectResult.setName(outputName[0])
                        
    def query_features(self):
        bslash = '"'
        answer = self.question("Query Features", "Would you like to query any features?")
        if answer == QMessageBox.Yes:
            baseLayer = self.inputDialog(1, "Base Layer", "Enter the name of the layer to be queried: ")
            while ((baseLayer[1] == True) and (len(QgsProject.instance().mapLayersByName(baseLayer[0])) == 0)):
                self.information("Error", "There is no layer named " + baseLayer[0] + "!")
                baseLayer = self.inputDialog(1, "Base Layer", "Enter the name of your base layer: ")
            if (baseLayer[1] != False):
                self.information("Instructions", "The query input is sensitive, please input \" before and after your attributes, example: [" + bslash + "ffh_typ_nr" + bslash +" = 1 or " + bslash +"geschuetzt_biotop" + bslash + " = 1]")
                query = self.inputDialog(1, "Query", "Enter your query (input-sensitive, please type " + bslash + " before and after your attributes): ")
                print(query)
                if (query[1] == True):
                    query = QgsExpression(query[0])
                    baseLayer = QgsProject.instance().mapLayersByName(baseLayer[0])[0]
                    it = baseLayer.getFeatures(QgsFeatureRequest(query))
                    ids = [i.id() for i in it]
                    baseLayer.selectByIds(ids)
                    valuable = baseLayer.materialize(QgsFeatureRequest().setFilterFids(baseLayer.selectedFeatureIds()))
                    QgsProject.instance().addMapLayer(valuable)
                    outputName = self.inputDialog(1, "Output Name", "Name the output queried layer: ")
                    if (outputName[1] == True):
                        valuable.setName(outputName[0])


"""Method to run the script in the order of the workflow."""

def run_script(iface):    
    project = HabitatAnalyzer(iface)
    if (project.welcome() == QMessageBox.Yes):
        print("Continuing")
        project.load_layers("Environment")
        project.load_layers("Autobahn")
        project.buffer_creation()
        project.perform_union()
        project.perform_union()
        project.perform_intersection()
        project.query_features()
        print("End")
    else:
        print("Stopping")
        

"""Automatically run script"""    
run_script(iface)


"""Disclaimer: As this is a simple and rater straightforward workflow, there wasn't much error checking involved. For the more obvious loops or decision forks that lead to potential errors, I created some basic exception handling, such that the script doesn't go into a loop or crash the program. Example: giving a non .gpkg file as an input to be added (technically, you can add .shp and other similar files, but we want to encourage the use of .gpkg, thus we only allow .gpkg files to pass the check)"""