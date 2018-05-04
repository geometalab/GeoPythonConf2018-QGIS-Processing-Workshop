Included are two datasets necessary for the workflow to be completed.
\
**Credits go to Claas Leiner of the University of Kassel, 2010 as this workflow was based on Task 6 of the course "Introduction to GIS and Digital Cartography"**  
**Note: This workflow has been adapted by Stefan Keller, Geometa Lab, Hochschule fur Technik Rapperswil for use as course material.**  
**Note 2: Subsequently, it was translated into English by Kang Zi Jing into English and updated for QGIS 3.0, for use in the GeoPython Conference 2018.**  

This folder contains 3 files:
* umgebung.gpkg
* autobahn.gpkg
* heli.tif 

The **_umgebung.gpkg_** file is a GeoPackage file which contains a multi-polygonal vector layer with a database containing attributes like
the use of habitats, the laws that protects the specific habitat, etc.\
The **_autobahn.gpkg_** file is a GeoPackage file which contains a line vector layer which shows the propsed route of the autobahn to be
constructed without showing the physical space (of 20m) that it would take up.\
The **_heli.tif_** file is generally inconsequent for the majority of the workshop and the main workshop tutorial. It is basically a raster file to be added as a reference basemap at the end of the entire workflow, for user reference and some aesthetic value.\
\
These files, along with its attributes, have been kept in its original language, German, so as to avoid introducing any possible errors
or other ambiguities when performing geoanalytical tasks on them in the course of the workshop. For your reference, below is a
glossary of the translations of some of the attributes that would be used in the workshop. 
\
It is entirely possible to finish the workflow without knowing what the German words mean, but for non native speakers, the terms that would be used and
we are interested in are bolded in the table below, for convenience.

# Glossary
|German|English|Meaning of Attribute|
|:---:|:---:|:---:|
|**umgebung**|environment|See above|
|**autobahn**|highway/expressway|See above|
|||
|||
|fid|Habitat ID|ID of Habitat/Attribute|
|nutzung|(Land) Use|What the habitat is used for|
|nutzungs_nr|(Land) Use no.|Different uses ordered by a number|
|bfn_gesetz|Law number under BFN|The associated BFN law|
|bfn_biotop_nr|Biotope no. under BFN|BFN Biotope number|
|bfn_biotop_text|Biotope text under BFN|BFN Biotope description|
|**ffh_typ_nr**|FFH Type|Boolean: Protected by FFH|
|ffh_typ_text|FFH Type Text|Reference Text for Associated FFH|
|**geschuetzt_biotop**|Protected Biotope|Boolean: Protected Species|
|gruenland_typ|Open Field Type|Type of Open Field|
|eutend_gruenland_|Open Field|Boolean: Open Field|
|**bedeutend_gruendland_typ**|Significant Open Field|Boolean: Significance|
* Note: The cells with "Boolean" in front means that the attributes is Booleanic, a 0 means false while a 1 means true for the attribute associated.
