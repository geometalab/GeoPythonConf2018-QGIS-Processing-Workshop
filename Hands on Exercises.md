# GeoPython Conference 2018
**Processing Framework: Automating Tasks with Python**
\
A QGIS workshop for the GeoPython Conference 2018
 
## Getting started
1. [Download and install QGIS 3.x](https://www.qgis.org/en/site/forusers/download.html) (Only QGIS 3.0 and above is supported because of changes in the update from 2.18 to 3.0
2. Get the sample data that we will be using from this repository
3. Fire up QGIS and we're ready! 
 
Downloading the standalone or OSGeo4W installer will automatically install the correct version of Python as well as Qt and PyQt.

## Setting up your development environment
To try out our hands on examples, the following is required:
* QGIS 3.x (We will be using QGIS 3.0)
* Python 3.x (We will be using Python 3.6)
* Qt
* PyQt
 
**Notes:**
* This repository contains the hands-on problem sets and tasks that we will try out during the workshop. It also contains the suggested solutions, master scripts, and graphic models for the tasks, and problem as a whole.
* For QGIS <2.99 users, these problem sets are still workable, but do take note that as QGIS upgraded from QGIS 2.18 to QGIS 3.0.0, there are a lot of changes, including the Python syntax to be upgrade from Python 2.6 to Python 3.6
* It is still possible to follow this workshop in QGIS 2.18, but do make sure that you are aware of the backwards incompatible changes as many methods and functions were made obsolete or renamed. You can see the [version changelog here](https://qgis.org/api/api_break.html#qgis_api_break_3_0_QgsGeometryAnalyzer)
* To be more specific and as a disclaimer, it is rather redundant if you are following this workshop using QGIS 2.18, as the LTR version of QGIS would soon be updated to QGIS 3.x, and the workshop here would still be very likely to work in the LTR
   
## Getting more sample data
If you want more sample data or resources to further try out QGIS on your own, look no further:
 
* [The PyQGIS Programmer's Guide](http://locatepress.com/ppg3)
* [The QGIS website also has some sample data](http://www.qgis.org)
* For raster layers to play around with, we can download one of the [Natural Earth rasters](http://www.naturalearthdata.com/downloads/)
* You can also check out [our Geometa Lab Blog](geometa.tumblr.com) for some posts on QGIS tips and tricks and other tidbits on GIS
 
## Using the QGIS Python Console
* With QGIS running, open the console by going to `Plugins -> Python Console`, clicking on the `Python Console` button from the `Plugin toolbar`, or simply press `Alt + Ctrl + P` on the keyboard
* The toolbar contains the tools **Clear console, Import Class, Run Command, Show Editor, Settings,** and **Help**
* The built-in code editor can be used alongside the console
* The QGIS API offers a large number of [Python classes](http://labs.webgeodatavore.com/partage/diagramme_principal.html) that we can use. See [Searchable documentation of PyQGIS classes](http://geoapis.sourcepole.com/qgispyapi/qgsnetworkaccessmanager)
* For the convenience of the user, the following statements are executed when the consoles is started
```python
from qgis.core import *
import qgis.utils
```
   
## Introduction to Processing Framework
* More information can be found in the slides also available in this repository

## About PyQGIS
* QGIS 0.9.0 introduced Python to its client
* PyQGIS or Python Console in QGIS client
* Features of PyQGIS:
    * Automatically run Python code when QGIS starts
    * Create custom applications with Python API
    * Run Python code and commands on the Python Console
    * Create and use Python plugins

\
\
\
# **Task: Perform Geospatial Analysis on Protected Habitats in an Environment**
* Problem: The construction of an autobahn/expressway will lead to detrimental impact onto the habitats on its environment. Analyze the protected habitats that would be affected by the construction.
* Source: This task is based on Task 6 of the course _Introduction to GIS and Digital Cartography_ by Claas Leiner, University of Kassel, 2010.
* Adapted to a class for Vector Analysis by Stefan Keller, FS 2017
* Translated and adapted for QGIS 3.0 and the GeoPython Conference by Kang Zi Jing, 2018
* The workflow can be found in the repository, here [link to the tutorial course]

**As you can already tell, doing this over and over again on different files is very tedious, boring and repetitive. Is there a way to automate this? Yes! With the help of scripting and PyQGIS, we can!**\
\
With the click of a button to run a script, we can automate this task in mere seconds.\
This problem will be broken down into smaller problem sets and tasks to break the problem apart. The tasks will be progressive, from getting familiar with the QGIS client to using its Processing toolbox tools, like the Graphical Modeler before moving on to creating your own custom script.


## **Task 1.** Adding Geopackage as Layers into QGIS
- **Dataset used:** Umgebung.gpkg, Autobahn.gpkg
- **Tools used:** QGIS GUI, PyQGIS
- **Description:** To load .gpkg files into QGIS client
- **Objective:** Manually load vector layers on QGIS, and then using the Python console

#### Task 1.1. Manually adding the Geopackage files into QGIS
1. Run QGIS 3.0 on your machine
2. The first step is to set the Project CRS to 31467, DHDN/Gauss-Kruger Zone 3
3. You can do this manually by clicking on the CRS at the bottom-right of the window, or by clicking `Project -> Project Properties -> CRS` or you can press `Ctrl + Shift + P` to open up Project Properties and then clicking CRS
4. From there, change the CRS to DHDN/Gauss-Kruger zone 3, EPSG: 31467
5. Once you're done, check that it says 31467 at the bottom of the window on the CRS tab
6. Now on the browser panel, look for GeoPackage, right click it and select **New Connection**
7. Navigate to the folder you saved environment/umgebung.gpkg in and add it
8. On the browser panel, show the child items of environment/umgebung.gpkg and drag the vector layer onto the map canvas
9. As we are going to focus on scripting in Python, let's remove this layer: right click the layer under Layers, and click on remove

#### Task 1.2. Creating a Dialog Box to ask for User Input on File to Add\
We want to write a script to automate tasks, so let us explore asking for user input for file path
1. On the Menu Toolbar, click `Plugins -> Python Console` or press `Ctrl + Alt + P` on your keyboard to open up the Python Console
2. You can run Python code on the console to perform various tasks, try creating a file dialog box that asks for user input on the file path
3. `envPath = QFileDialog.getOpenFileName(QFileDialog(), "Environment Layer Select", "setDefaultPath")[0]`
4. The `[0]` is because the above returns a list, and we only need the first value of it, which is the file path

#### Task 1.3. Adding Vector Layers into QGIS
Now we can add the user input layer into QGIS
1. `env = iface.addVectorLayer(envPath, 'nameIt', 'ogr')`
2. If the layer name is saved as something else, you can change it with `env.setName("newName")`
3. Practice and do the same for the Autobahn layer using the Python console

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Workflow%20Example%20Images/Task%201.png)

## Task 2. Adding Buffers to Autobahn Layer
- **Dataset used:** Autobhan.gpkg
- **Tools used:** Processing Graphic Modeler, Python Console
- **Description:** To create buffer layers for the Autobahn to simulate the actual physical space of it
- **Objective:** Running Processing algorithms on the Graphic Modeler, and then with Pythonic code

#### Task 2.1. Introduction and Running the Graphic Modeler
The Graphic Modeler is a good introduction to scripting in PyQGIS because the coding and scripting is displayed for the user as something visual, which is easy on the beginners
1. To start off, you need to open up your Processing Toolbox, on the menu toolbar, click `Processing -> Toolbox` or press `Ctrl + Alt + T` and see that the Processing Toolbox window now appears on the right side of the QGIS window
2. On the Toolbox's menu toolbar, click `Models -> Create New Model`
3. First, we need to visualize and get an idea of what we want to achieve (this helps us to form pseudo code before creating actual code in the future): Run through the Autobahn layer with a Buffer algorithm to create a new Autobahn layer that is 40m wide in diameter

#### Task 2.2. Create a 20m buffer file for the Autobahn layer using the Graphic Modeler
With the Processing Graphic Modeler open, we can now visualize and build Task 2.1.3
1. Name the Model `Autobahn Buffer` and the Group `vector`
2. On the bottom left, click on Input if it is not already selected, and drag Vector Layer into the blank canvas
3. Name the parameter name `Autobahn` and under Geometry type, select Line as we only want it to exclusively deal with line geometries
4. Drag a Number under Input into the canvas, and name it `Buffer Distance`, you may choose to fill in the other fields
5. On the bottom left, click on Algorithms, and in the searchbar, type 'Buffer', and drag the Algorithm called Buffer into the canvas, making sure it is under *Vector Geometry* and not any other algorithm provider
6. In the Input Layer field, select `Autobahn` from the dropdown menu, in the Distance field, type `@bufferdistance`, and in the Buffered field, type *Output Layer Name*
7. On your canvas, you should see that **Buffer Distance** and **Autobahn** are connected as inputs to **Buffer** which gives an output named **Output Layer Name**
8. On the menu toolbar, click on the green arrow Run Model or press F5 to run the model
9. Under Autobahn, select your Autobahn vector layer from the drop down menu, under Buffer Distance, type in **20** and under Output Layer Name, type **Autobahn 20** and run it
10. Let the Model run and after processing, you should see the output vector on your main QGIS window

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Slide%20Images/Graphic%20Modeler%20Example.png)

#### Task 2.3. Recreating the same function using a standalone script
Now that you visualized your steps, you can now try to translate them into actual Pythonic code on the Python Console\
1. On the main QGIS window, at the Processing Toolbox, search for **Buffer**, this is the algorithm that we utilized in the Modeler
2. Double click on it and you can do essentially the same thing as we did in the modeler, except with a few extra fields that we set to default in the Modeler
3. Enter the fields for **Input Layer, Distance and Buffered** and run it
4. At the top of the window, click on Log, you will see a bunch of code, we will be needing this for our script
5. Study the Input parameters and copy its entire line of code
6. On the PyQGIS console, type `atbn = QgsProject.instance().mapLayersByName('%NAMEOFYOURAUTOBAHNLAYER%')[0]`, this assigns the vector layer of your autobahn to the variable `atbn`
7. On the PyQGIS console, type `param =` and paste the copied code, and edit some fields, it should look something like this:\
``
param = { 'INPUT' : atbn, 'DISTANCE' : 20, 'SEGMENTS' : 5, 'END_CAP_STYLE' : 0, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'DISSOLVE' : False, 'OUTPUT' : 'memory:' }
``
   We changed the file paths or assigned them to variables to make it easier for us because the Python console cannot read Unicode characters like `\` 
8. Now to add the output as a map layer, type:
```
algoOutput = processing.run("qgis:buffer", param)
autobahn20 = QgsProject.instance().addMapLayer(algoOutput['OUTPUT'])
autobahn20.setName("Autobahn 20")
```

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Slide%20Images/Buffer%20Log%20Example.png)

#### Task 2.4. Creating 2 more buffers
Often times, the actual physical space that a highway construction takes up, is smaller than the actual impact that it causes to the environment.\
Create 2 more buffers to depict 2 more impact zones that the construction of the Autobahn would cause\
Bonus: You may also create a script that interactively asks for user input before running the Buffer algorithm 
1. On the Processing Toolbox, press the Scripts button and select **Create New Script**
2. It will open up a text editor where you can write your Pythonic scripts
3. Add the following as the header of your script:
```
from qgis.core import QgsProject
import processing
```
4. Write a script that does the following:
```
1. Using Autobahn 20 and 100m as inputs, create a new buffer naemd Autobahn 100
2. Using Autobahn 100 and 200m as inputs, create a new buffer named Autobahn 300

Hint: You might need to assign the variable `autobahn20` in the script, do this with: `autobahn20 = QgsProject.instance().mapLayersByName("%name_of_layer%)[0]
```
5. Save the script

## Task 3. Performing Union on the Buffer Areas
- **Dataset used:** Autobahn.gpkg, and the 3 buffer results from previous task
- **Tools used:** Python Console, Script Editor
- **Description:** Now that we have 3 separate buffer layers to showcase the impact areas, we should perform an Union on them to create an overall area of impact from constructing the highway
- **Objective:** Get more familiar with using Pythonic code to run Processing algorithms

#### Task 3.1. Union-ing the Inner Impact Zone
Now that we have tried to run Processing algorithms on the Python Console, let us try it on a standalone script
1. Open a new script and include the same headers from the previous script here
2. Now, we are going to run a different algorithm, the Union
3. Back on the main QGIS window, in the Processing Toolbox search bar, search **Union** and you can try running the Union algorithm under **Vector Overlay**
4. The inputs will be **Autobahn 20** and **Autobahn 100**, and name the output **Inner Impact Area**
5. Using the input parameters under Log of the algorithm window, write a script similar to Task 2 
6. If you have trouble doing it, you can try using the Modeler to visualize your script

#### Task 3.2. Union-ing the Overall Impact Area
Next, we perform the Union algorithm on the result of the previous task, the Inner Impact Zone, with the Outer Impact Zone to aggregate the total Area of Impact
1. Do the same for the resulting layer, Inner Impact Area and Autobahn 300 and name the output **Impact Area**
2. You will now have a layer that is the union of all 3 Autobahn buffers
3. You can see a screenshot of what your project should roughly look like below:

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Slide%20Images/Task%203%20Example.png)

## Task 4. Refining Code
- **Dataset used:** Umgebung.gpkg, union result from previous task
- **Tools used:** Script Editor
- **Description:** Now that we have an overall impact area, we run an Intersection algorithm on it and the Environment layer to highlight the habitats that would be affected
- **Objectives:** More scripting with Processing algorithms, also introduction to function declarations

#### Task 4.1. Performing Intersection on Environment and Impact Area
You have already created your own script! Now that we are more familiar with scripting, we shall now cover the rest of the tasks using scripts \
Now, as mentioned, run an Intersection algorithm on the Environment layer as well as the Impact Zone layer
1. Similar to Task 3, we shall now run an Intersection algorithm on the **Impact Area** layer and the **Environment** layer
2. However, let's make our script cleaner and friendlier, we can do this by defining functions, which are reusable blocks of code
3. Start by creating a new script with the same headers as previous and then change the following pseudo code into actual Python code:
```
from dataSources import dataLibraries

def intersect_layers(layer1, layer2, outputName):
    param = { 'INPUT' : layer1, 'OVERLAY' : layer2, 'INPUT_FIELDS' : [], 'OVERLAY_FIELDS' : [], 'OUTPUT' : 'memory:' }
    intxnOp = QgsProject.instance().addMapLayer(processing.run("qgis:intersection", param)['OUTPUT'])
    intxnOp.setName(outputName)
    
```
4. Save the script, and on the Python Console select Open Script and open the script you just saved, after that, select Run Script on the Python Console. What happened is that you created a function in the script such that when the script is run, a function named **intersect_layers** is available to be called, which takes 3 variable inputs **layer1, layer2** and **outputName**
5. When you call the function with the correct inputs, it will create and output, with the name of outputName, which is the intersection of the first 2 input vector layers
6. For this to work for us, we have to assign the **Environment** layer and **Impact Area** layer
7. Hint:
```
layerA = QgsProject.instance().mapLayersByName('Environment')
layerB...
opName = ' xxx '

intersect_layers(layerA, layerB, opName)
```
8. Your result should look something like this: 

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Slide%20Images/Task%204%20Example.png)

#### Task 4.2. Doing the Same for Previous Tasks
Now that you have learned how to define a function in a script, do it for:
1. Adding a vector layer with user input from a dialog box
2. Adding a buffer
3. Performing an union
4. Performing an intersection
5. Hint: It should look something like this:
```
import libraries

def add_layer(inputs):
    """your code here"""
    
def set_CRS(input):
    """your code here"""
    
def more_functions(inputs):
    """"your code here""""
````
7. Once you have finished the script, run it, then on the Python console, declare and assign your variables, then try running the functions you have defined, you should be able to recreate the project thus far
8. Due to time constraint during the actual workshop, we might not have time to do this for every task, so here is a script that works and already have these function declarations [link]
9. We shall now continue writing the script by declaring functions to allow easy reusability and calling

## Task 5. Selecting Features from Queries
- **Dataset used:** Umgebung.gpkg
- **Tools used:** Query Features and Script Editor
- **Description:** Now, we have to sieve out, from the impacted and affected habitats, those that are protected species from the others
- **Objectives:** Feature query on QGIS, feature query in PyQGIS, adding layers in PyQGIS

#### Task 5.1. Running a Query on the Environment Vector Layer Attributes
Query the attributes of the Environment Shapefile to determine the features that are protected by law\
1. To do this, right click on the Environment layer in the Layers panel, and select Open Attribute Table
2. On the top menu bar, click the button that says `Select features with an expression`
3. Write the expression for which you want to select queries with, for our case, we are looking for habitats where `"ffh_typ_nr" = 1`, `"geschuetzt_biotop" = 1`, or `"bedeutend_gruendland_type" = 1`
4. Once you have written the expression, click on `Select Features`, you should have 43 features highlighted

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Workflow%20Example%20Images/Task%206.1.png)

#### Task 5.2. Translating Query Feature into Pythonic Code
Now we do what we did in 5.1 using Pythonic code in our script

1. Remember, we are looking for habitats where `"ffh_typ_nr" = 1`, `"geschuetzt_biotop" = 1`, or `"bedeutend_gruendland_type" = 1`
2. In your script, type:
```
expr = QgsExpression("\"ffh_typ_nr\"=1 or \"geschuetzt_biotop\" = 1 or \"bedeutend_gruenland_typ\" = 1")
```
3. Next, we need to select all features that meet this query:
```
it = env.getFeatures(QgsFeatureRequest(expr))
```

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Workflow%20Example%20Images/Task%206.2.png)


#### Task 5.3. Adding Vector Layer of Selected Features
Now we have to create new layers with just the selected features to show which features are actually affected by the Autobahn construction
1. Now that we have a layer with highlighted features, go back to the QGIS window, right click the Environment layer and select `Save As...`
2. On the new window, fill in the relevant fills, and make sure that `Save only selected features` is checked

#### Task 5.4. Translating Vector Layer Adding into Pythonic Code
1. And then, we want to create a new layer made from the selected features:
```
ids = [i.id() for i in it]
intersectedHabs.selectByIds(ids)
valuable = env.materialize(QgsFeatureRequest().setFilterFids(intersectedHabs.selectedFeatureIds()))
QgsProject.instance().addMapLayer(valuable)
```
5. Lastly, we can set the name and deselect the highlighted features with `%LAYERNAME%.selectByIds([])`

## Task 6. Stylizing and Cleaning Up
- **Dataset used:**
- **Tools used:** Script Editor
- **Description:** Stylize the map layers to make results more obvious and clean up the project to make it more readable
- **Objectives:** Various styling tools and functions on QGIS, and then on PyQGIS

#### Task 6.1. Deleting Intermediate Layers
Some of the intermediate layers can be deleted because they serve no actual analytical purpose
1. Look at your project and determine which ones are inconsequent to your overall analysis, and you may want to delete them from the project to make it more readable and less cluttered
2. Psuedocode for doing this:
```
- find the id of the map layers you want to delete, you may find it through mapLayersByName()
- make sure that you have the pointer to the vector map layer object of the layer you want to delete
- call removeMapLayer() from QgsProject instance
```

#### Task 6.2. Hiding Layers
Some of the result layers can be useful, but too many layers visible on the project makes it hard to read\
Uncheck their visibility using a script so that they are still available, but not visible on the Map Canvas\
1. Pseudocode:
```
- get a pointer to your layer under layerTreeRoot()
- setItemVisibilityChecked(False) for that data object
```

#### Task 6.3. Stylizing Map Layers
There are many styles that can be utilized on the layers so that you can get information at a glance\
For today, we try to stylize them by categorizing different data in different colors and similar data in different shades
1. First we have to choose the attributes we want to categorize our vector layer in, for this example, say we want to make all the valuable habitats that are impacted to be green, and we want to categorize it by the type of FFH classification it falls into
2. To do that, we have to find out how many unique FFH classifications we have in the layer:
```
classNames = valuableIntersected.fields().indexFromName('ffh_typ_text')
uniqueClass = valuableIntersected.dataProvider().uniqueValues(classNames)

categories = []
count = 0

for class in uniqueClass:
    count += 1
```
3. Now, we categorize the different types of attibutes with a different shade of color:
```
for classes in uniqueClass:
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    layerStyle = {}
    layerStyle['color'] = '%d, %d, %d' % ( your desired RGB values )
    layerStyle['outline'] = '#000000'
    symbolLayer = QgsSimpleFillSymbolLayer.create(layerStyle)
    if symbolLayer is not None:
        symbol.changeSymbolLayer(0, symbolLayer)
    
    category = QgsRendererCategory(uniqueClass, symbol, str(classes)
    categories.append(category)
```
4. Run the renderer and repaint:
```
renderer = QgsCategorizedSymbolRenderer('ffh_typ_text', categories)
if renderer is not None:
    valuableIntersected.setRenderer(renderer)
valuableIntersected.triggerRepaint()
```

#### Task 6.4. Adding a Basemap
We can add a raster basemap as a reference for your geospatial data analysis
1. Get an input for the path which the raster map is stored
2. Use addRasterLayer() to add the raster layer
3. You may want to player with the renderer() and symbol() to adjust the basemap stylization settings

#### Task 6.5. Rearranging the Layers
Let's rearrange the layers for better visibility by putting the original Autobahn 20 and Autobahn vector files at the top of the order 
1. Get the layerTreeRoot() of the QgsProject
2. Find the layers you want to reslot using findLayer()
3. clone them using clone()
4. Get a pointer to the parent object of the layer using parent()
5. Insert the clones into the parent node and remove the original layers using insertChildNode(position, layer) and removeChildNode()
6. Refresh the map canvas

![Reference](https://github.com/bigzijing/Geopython-Conference-2018/blob/master/Workshop%20Presentation%20Slides/Workflow%20Example%20Images/Task%207.png)

## Task 7. Finishing Up
- **Dataset used:**
- **Tools used:** Script Editor
- **Description:** Finish up and make sure that all your code is in a single script and everything works when you run it!
- **Objectives:** Finishing touches, making sure all is good

#### Task 7.1. Finishing Touches
For the last touch, make sure that all your functions and code are all properly ordered and functions properly
1. Clear the QGIS canvas by typing `QgsProject.instance().clear()`
2. Run your script once again and make sure that the workflow progresses as intended
3. If your final results look like the end result, you just created an automated script that helps automate a workflow!

# Bonus: Interactive and Independent Script
We have created many different functions to help us achieve our tasks\
Can we do better to join them all into just 1 script entity?\
Can we do even better and create a script that is interactive and uses the user inputs to automate our tasks?\
Can we publish these scripts or create something that others can use?
\
There are many ways to customize your scripts and workflow processing in QGIS! You may create a Processing Script that is accessible on the Toolbox (not shown here), make it a plugin, run it with Script Runner plugin, or just run it in the Python console. The great thing about flexibility is you have the freedom to do as you please to suit your needs, so practice away!

#### Bonus: Creating a Main Script
1. For the more advanced coders, you might want to create a Class and declare methods instead of just defining functions, as in this workshop, we did not go in-depth into classes
2. Otherwise, finish this script that does everything with just being called once
3. Make the script interactive, and get the user inputs on file paths, algorithm parameters, etc.
4. Once you are satisfied with that script, you might even want to consider converting it into a plugin so that it can be published and used by others


## Notes and Disclaimer
Note that there is no 'perfect' or 'only' solution when it comes to scripting, and as such, the scripts that were demonstrated and available in this workshop/repository are only for references and to guide you. With that said, always try to maintain good programming practices so that your code is clean, readable and easy to maintain. 

## References, Resources and Additional Help
* [Processing: A Python Framework for the Seamless Integration of Geoprocessing Tools in QGIS by Anita Graser](http://www.mdpi.com/2220-9964/4/4/2219/htm)
    * In-depth development history on Processing Framework
* [Anita Graser's blog](http://anitagraser.com)
* [Processing GitHub repository by Victor Olaya (developer of Processing)](https://github.com/qgis/QGIS-Processing)
* [QGIS Testing Documentation](https://docs.qgis.org/testing/en/docs/)
    * Contains a lot of resources and documentations
    * Links to tutorials and textbooks like the PyQGIS Cookbook, QGIS Developers Guide
* [QGIS Tutorials by Ujaval Gandhi](http://www.qgistutorials.com/en/)
    * Helpful step by step tutorials on many aspects of QGIS
* Vast amount of resources, forums and an active and helpful community online
* Special thanks to helpful developers like Anita Graser and other users on GIS Stack Exchange for answering my questions
* And of course, the wonderful people at Geometa Lab, HSR

## Contact
Kang Zi Jing, author and owner of this GitHub repository: zkang[at]hsr[dot]ch 
