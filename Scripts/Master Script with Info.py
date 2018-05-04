"""This is the master script for the GeoPython Conference 2018"""

"""Import some key tools"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from qgis.core import QgsVectorLayer, QgsMapSettings, QgsProject, QgsExpression, QgsFeatureRequest, QgsSymbol, QgsSimpleFillSymbolLayer, QgsRendererCategory, QgsCategorizedSymbolRenderer, QgsLayerTreeNode
from qgis.gui import QgsMapToolEmitPoint
from qgis.gui import QgsMapTool
from qgis.utils import iface
from qgis import core
from random import random, randrange
import processing

"""
1. Create project file / Show the land use
    a. ask for envrironment.gpkg
    b. set CRS and unit system
    c. save project (if possible)
    d. set symbologyExport
    
    Prompt the user of the script and have option to cancel
    Be more verbal about the steps that are happening
    Double check if inputs are correct
    
"""
"""QMessageBox creates a message pop-up whereas QFileDialog creates a file selection dialog. Find out more uses and options in the documentations"""

runScript = QMessageBox.question(iface.mainWindow(), 'Habitat Analyzer', 'Do you want to run the script?', QMessageBox.Yes, QMessageBox.No)

if runScript == QMessageBox.Yes:
    QMessageBox.information(iface.mainWindow(), "Habitat Analyzer", "Welcome to Habitat Analyzer")
    
    QMessageBox.information(iface.mainWindow(), "File Select", "Select your Environment layer from a Geopackage")
    envInput = QFileDialog.getOpenFileName(QFileDialog(), "Environment Layer Selection", "\\svm-c113.hsr.ch\zkang\Desktop\QGIS-Steilkurs_MSE_Maerz_2017\QGIS-Steilkurs_MSE_Maerz_2017\daten_autobahn")
    envPath = envInput[0]
    env = iface.addVectorLayer(envPath, 'Environment', 'ogr')
    env.setName("Environment")

    """Setting CRS of Environment layer"""
    my_crs = core.QgsCoordinateReferenceSystem(31467, core.QgsCoordinateReferenceSystem.EpsgCrsId)
    QgsMapSettings().setDestinationCrs(my_crs)
    iface.mapCanvas().refresh()

    """Now, change the stylization of the envrionment layer"""
    QMessageBox.information(iface.mainWindow(), "", "Setting the layer color to RGB 200, 220, 135 and opacity to 0.5")
    envL = iface.activeLayer()
    renderer = envL.renderer()
    symbol = renderer.symbol()
    symbol.setColor(QColor(0, 200, 220, 135))
    symbol.setOpacity(.5)
    envL.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(envL.id())

    """Next, we add the line file of the Autobahn, set it to red and then create a buffer around it to represent its physical form"""
    QMessageBox.information(iface.mainWindow(), "File Select", "Select your Autobahn layer from a Geopackage")
    atbnInput = QFileDialog.getOpenFileName(QFileDialog(), "Autobahn Layer Selection", "\\svm-c113.hsr.ch\zkang\Desktop\QGIS-Steilkurs_MSE_Maerz_2017\QGIS-Steilkurs_MSE_Maerz_2017\daten_autobahn")
    atbnPath = atbnInput[0]
    atbn = iface.addVectorLayer(atbnPath, 'Autobahn', 'ogr')

    """Now, change the stylization of the autobahn layer"""
    QMessageBox.information(iface.mainWindow(), "", "Setting the color of the Autobahn line to Red")
    atbnL = iface.activeLayer()
    renderer = atbnL.renderer()
    symbol = renderer.symbol()
    symbol.setColor(QColor(255, 0, 0, 255))
    atbnL.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(atbnL.id())


    """Now, we run the QGIS algorithm, buffer, on the Autobahn to recreate an actual physical representation of the autobahn with 20m radius"""
    QMessageBox.information(iface.mainWindow(), "Autobahn 20", "Creating Buffer 1: Actual physical representation of Autobahn")
    param = { 'INPUT' : atbnL, 'DISTANCE' : 20, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
    styles = processing.run("qgis:buffer", param)
    autobahnSpace = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    layer = iface.activeLayer()
    atbn20 = layer
    layer.setName("Autobahn 20")
    QMessageBox.information(iface.mainWindow(), "", "Setting color of the Autobahn 20 to RGB 58, 26, 52")
    renderer = atbn20.renderer()
    symbol = renderer.symbol()
    symbol.setColor(QColor(58, 26, 52))
    
    """Next, we add 2 more buffers, 1 100m away from the autobahn, and the other 300m away from the autobahn. These are used to illustrate that the impact of constructing an autobahn is far more than just the physical space that it uses."""

    QMessageBox.information(iface.mainWindow(), "Autobahn 100", "Creating Buffer 2: 100m radius from Autobahn 20")
    atbn_map = iface.activeLayer()
    param = { 'INPUT' : atbn_map, 'DISTANCE' : 100, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
    styles = processing.run("qgis:buffer", param)
    autobahnBuffer1 = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    layer = iface.activeLayer()
    layer.setName("Autobahn 100")
    QMessageBox.information(iface.mainWindow(), "", "Unchecking Autobahn 100 as it is an intermediate file")
    QgsProject.instance().layerTreeRoot().findLayer(layer).setItemVisibilityChecked(False)

    QMessageBox.information(iface.mainWindow(), "Autobahn 300", "Creating Buffer 3: 200m radius from Autobahn 100")
    atbn_map = iface.activeLayer()
    param = { 'INPUT' : atbn_map, 'DISTANCE' : 200, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
    styles = processing.run("qgis:buffer", param)
    autobahnBuffer1 = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    layer = iface.activeLayer()
    layer.setName("Autobahn 300")
    QMessageBox.information(iface.mainWindow(), "", "Unchecking Autobahn 300 as it is an intermediate file")
    QgsProject.instance().layerTreeRoot().findLayer(layer).setItemVisibilityChecked(False)


    """Now that we have the 3 files buffered from the red Autobahn line file, let's perform an Union on them"""

    QMessageBox.information(iface.mainWindow(), "Impact Area", "Performing Unions on the 3 Buffers to aggregate total impact area of Autobahn construction")
    autobahn20 = QgsProject.instance().mapLayersByName("Autobahn 20")[0]
    autobahn100 = QgsProject.instance().mapLayersByName("Autobahn 100")[0]
    autobahn300 = QgsProject.instance().mapLayersByName("Autobahn 300")[0]

    QMessageBox.information(iface.mainWindow(), "Impact Area Minor", "Creating first union of inner buffers")
    param = { 'INPUT' : autobahn20, 'OVERLAY' : autobahn100, 'OUTPUT': 'memory:' }
    styles = processing.run("qgis:union", param)
    autobahnUnion1 = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    impactAreaMinor = iface.activeLayer()
    impactAreaMinor.setName("Impact Area 1")
    QMessageBox.information(iface.mainWindow(), "", "Unchecking Impact Area Minor as it is an intermediate file")
    QgsProject.instance().layerTreeRoot().findLayer(impactAreaMinor).setItemVisibilityChecked(False)


    impactArea1 = QgsProject.instance().mapLayersByName("Impact Area 1")[0]
    QMessageBox.information(iface.mainWindow(), "Impact Area Major", "Creating the total aggregated impact area")
    param = { 'INPUT' : impactArea1, 'OVERLAY' : autobahn300, 'OUTPUT': 'memory:' }
    styles = processing.run("qgis:union", param)
    autobahnUnion1 = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    impactAreaMajor = iface.activeLayer()
    impactAreaMajor.setName("Impact Area")

    """We take the intersection of the impact area and the environment to cut off the excess parts"""
    QMessageBox.information(iface.mainWindow(), "Impacted Habitats", "Running an intersection between the impact area and environment area to determine the habitats within the impact")
    param = { 'INPUT' : impactAreaMajor, 'OVERLAY' : env, 'INPUT_FIELDS' : [], 'OVERLAY_FIELDS' : [], 'OUTPUT' : 'memory:' }
    styles = processing.run("qgis:intersection", param)
    impactIntersected = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    impactIntersected.setName("Impact Area Intersected")
    QMessageBox.information(iface.mainWindow(), "", "Setting the color of the impacted habitats to RGB 90, 190, 150 and opacity to 0.8")
    renderer = impactIntersected.renderer()
    symbol = renderer.symbol()
    symbol.setColor(QColor(90, 190, 150, 205))
    symbol.setOpacity(.8)
    impactIntersected.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(impactIntersected.id())


    """Next, we are going to select the notable/important habitats by passing through a query on the attribute of the environment layer"""
    
    QMessageBox.information(iface.mainWindow(), "", "Selecting protected and valuable habitats using a query")
    expr = QgsExpression("\"ffh_typ_nr\"=1 or \"geschuetzt_biotop\" = 1 or \"bedeutend_gruenland_typ\" = 1")
    it = env.getFeatures(QgsFeatureRequest(expr))
    ids = [i.id() for i in it]
    env.selectByIds(ids)
    valuable = env.materialize(QgsFeatureRequest().setFilterFids(env.selectedFeatureIds()))
    QgsProject.instance().addMapLayer(valuable)
    valuable.setName("Valuable")
    empty = []
    env.selectByIds(empty)


    """Now, we intersect the valuable habitats and non-valuable habitats against the impact zone to sieve out what habitats are actually affected by the construction of the autobahn"""

    QMessageBox.information(iface.mainWindow(), "", "Intersecting the selected features against impact area to get the valuable habitats that are impacted")
    expr2 = QgsExpression("\"ffh_typ_nr\"=1")
    it = valuable.getFeatures(QgsFeatureRequest(expr2))
    ids = [i.id() for i in it]
    valuable.selectByIds(ids)
    valuableIntersected = valuable.materialize(QgsFeatureRequest().setFilterFids(valuable.selectedFeatureIds()))
    """QgsProject.instance().addMapLayer(valuableIntersected)"""
    param = { 'INPUT' : valuableIntersected, 'OVERLAY' : impactAreaMajor, 'INPUT_FIELDS' : [], 'OVERLAY_FIELDS' : [], 'OUTPUT' : 'memory:' }
    styles = processing.run("qgis:intersection", param)
    valuableIntersected = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    valuableIntersected.setName("Valuable Intersected")
    """valuableIntersected = iface.activeLayer()"""
    valuable.selectByIds(empty)

    
    QMessageBox.information(iface.mainWindow(), "", "Doing the same for the non valuable habitats")
    expr3 = QgsExpression("\"ffh_typ_nr\"=0")
    it = valuable.getFeatures(QgsFeatureRequest(expr3))
    ids = [i.id() for i in it]
    valuable.selectByIds(ids)
    nValuableIntersected = valuable.materialize(QgsFeatureRequest().setFilterFids(valuable.selectedFeatureIds()))
    """QgsProject.instance().addMapLayer(nValuableIntersected)"""
    nValuableIntersected.setName("Non-Valuable Intersected")
    param = { 'INPUT' : nValuableIntersected, 'OVERLAY' : impactAreaMajor, 'INPUT_FIELDS' : [], 'OVERLAY_FIELDS' : [], 'OUTPUT' : 'memory:' }
    styles = processing.run("qgis:intersection", param)
    nValuableIntersected = QgsProject.instance().addMapLayer(styles['OUTPUT'])
    nValuableIntersected.setName("Non-Valuable Intersected")
    valuable.selectByIds(empty)


    """Now, we stylize the map layer by category for easy readability"""

    QMessageBox.information(iface.mainWindow(), "", "Now we stylize the map for better readability")
    QMessageBox.information(iface.mainWindow(), "", "We categorize by color: valuable habitats in green and non-valuable habitats in brown")
    QMessageBox.information(iface.mainWindow(), "", "Different types of habitats are categorized by a different shade or gradient of color")
    fni = valuableIntersected.fields().indexFromName('ffh_typ_text')
    unique_values = valuableIntersected.dataProvider().uniqueValues(fni)

    categories  = []
    count = 0
    iteration = 1

    for unique_value in unique_values:
        count += 1

    for unique_value in unique_values:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        layer_style = {}
        increase = 256 / count
        layer_style['color'] = '%d, %d, %d' % (0, (256 - (iteration * (increase/2))), 0)
        """layer_style['color'] = '%d, %d, %d' % (randrange(0,256), randrange(0,256), randrange(0,256))"""
        layer_style['outline'] = '#000000'
        symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
    
        if symbol_layer is not None:
            symbol.changeSymbolLayer(0, symbol_layer)
        
        category = QgsRendererCategory(unique_value, symbol, str(unique_value))
        categories.append(category)
    
        iteration += 1
    
    renderer = QgsCategorizedSymbolRenderer('ffh_typ_text', categories)

    if renderer is not None:
        valuableIntersected.setRenderer(renderer)
    valuableIntersected.triggerRepaint()

    """We do  the same for the non-valuable habitats"""

    fni = nValuableIntersected.fields().indexFromName('bfn_biotop_text')
    unique_values = nValuableIntersected.dataProvider().uniqueValues(fni)

    categories  = []
    count = 0
    iteration = 1

    for unique_value in unique_values:
        count += 1
    
    for unique_value in unique_values:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        layer_style = {}
        increase = 256 / count
        layer_style['color'] = '%d, %d, %d' % ((210 - (iteration * (increase/2.5))), (222 - (iteration * (increase/1.25))), 0)
        """layer_style['color'] = '%d, %d, %d' % (randrange(0,256), randrange(0,256), randrange(0,256))"""
        layer_style['outline'] = '#000000'
        symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
    
        if symbol_layer is not None:
            symbol.changeSymbolLayer(0, symbol_layer)
        
        category = QgsRendererCategory(unique_value, symbol, str(unique_value))
        categories.append(category)

        iteration += 1
    
    renderer = QgsCategorizedSymbolRenderer('bfn_biotop_text', categories)

    if renderer is not None:
        nValuableIntersected.setRenderer(renderer)
    nValuableIntersected.triggerRepaint()
    """QgsProject.instance().removeMapLayer(valuable)
    QgsProject.instance().removeMapLayer(impactAreaMinor)
    QgsProject.instance().removeMapLayer(QgsProject.instance().mapLayersByName("Autobahn 20")[0])
    QgsProject.instance().removeMapLayer(QgsProject.instance().mapLayersByName("Autobahn 100")[0])
    QgsProject.instance().removeMapLayer(QgsProject.instance().mapLayersByName("Autobahn 300")[0])"""
    QgsProject.instance().layerTreeRoot().findLayer(impactAreaMinor).setItemVisibilityChecked(False)
    QgsProject.instance().layerTreeRoot().findLayer(valuable).setItemVisibilityChecked(False)
    QgsProject.instance().layerTreeRoot().findLayer(impactAreaMajor).setItemVisibilityChecked(False)

    QMessageBox.information(iface.mainWindow(), "", "Now that the stylization is completed, we rearrange the layers for better visibility")

    root = QgsProject.instance().layerTreeRoot()
    myalayer = root.findLayer(atbn.id())
    myblayer = root.findLayer(atbn20.id())
    myClone2 = myblayer.clone()
    myClone = myalayer.clone()
    parent = myalayer.parent()
    parent.insertChildNode(0, myClone)
    parent.insertChildNode(1, myClone2)
    parent.removeChildNode(myalayer)
    parent.removeChildNode(myblayer)
    iface.mapCanvas().refresh()

    QMessageBox.information(iface.mainWindow(), "", "Lastly, we add a Basemap if it exists")

    reply = QMessageBox.question(iface.mainWindow(), 'Raster Basemap', 'Do you have a raster basemap?', QMessageBox.Yes, QMessageBox.No)

    if reply == QMessageBox.Yes:
        QMessageBox.information(iface.mainWindow(), "File Select", "Select your raster basemap file")
        bmInput = QFileDialog.getOpenFileName(QFileDialog(), "Raster Basemap Selection", "\\svm-c113.hsr.ch\zkang\Desktop\QGIS-Steilkurs_MSE_Maerz_2017\QGIS-Steilkurs_MSE_Maerz_2017\daten_autobahn")
        bmBm = bmInput[0]
        bm = iface.addRasterLayer(bmBm, 'Raster Basemap')
        bm.setName("Basemap")
        bm.renderer().setOpacity(0.25)

        myclayer = root.findLayer(bm.id())
        myClone3 = myclayer.clone()
        parent.insertChildNode(12, myClone3)
        parent.removeChildNode(myclayer)
        iface.mapCanvas().refresh()

    """ Can follow the code here: https://gis.stackexchange.com/questions/175068/apply-symbol-to-each-feature-categorized-symbol

    1. Count the number of different attributes using for loop
    2. 256 divide by number - that will be the increase per attribute
    3. In another attribute for loop, for each attribute, the color = x + increase
    """
else:
    QMessageBox.information(iface.mainWindow(), "End", "Script will not run")

