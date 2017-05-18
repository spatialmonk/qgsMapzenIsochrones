# -*- coding: utf-8 -*-
"""
Created by: Ethan Monk
			ethangmonk@gmail.com
			20170515

"""


from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from PyQt4 import QtCore
from qgis.core import *
import qgis.utils

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from mapzen_isochrones_dialog import MapzenIsochronesDialog
import os.path
import urllib2
from PyQt4.QtGui import QMessageBox
import requests
from osgeo import ogr
import json





class isochrone_gen:
    def __init__(self, dlg):
        self.dlg = dlg
        #self.dlg = MapzenIsochronesDialog()
        #self.iface = iface

        global getString
        global getConcat




        #Clear comboBox and comboBox_2
        self.dlg.comboBox.clear()
        self.dlg.comboBox_2.clear()
        
        #Add Costing Model Parameters to comboBox
        self.dlg.comboBox.addItem('auto')
        self.dlg.comboBox.addItem('bicycle')
        self.dlg.comboBox.addItem('pedestrian')
        self.dlg.comboBox.addItem('multimodal')
           
        

    
    
    
	#Populate comboBox_2 with all point file layers
        for layer in qgis.utils.iface.legendInterface().layers():
                layerType = layer.type()
                if layerType == QgsMapLayer.VectorLayer and layer.wkbType() == QGis.WKBPoint:
                    self.dlg.comboBox_2.addItem(layer.name())
        
		
		
        self.enableOne()
        self.enableTwo()
        self.enableThree()
        #Connect Form Events to Functions
        QtCore.QObject.connect(self.dlg.radioButton, QtCore.SIGNAL('toggled()'), self.enableOne)
        self.dlg.radioButton.toggled.connect(self.enableOne)
        self.dlg.radioButton_2.toggled.connect(self.enableTwo) 
        self.dlg.radioButton_3.toggled.connect(self.enableThree) 
                          


    #SET API Parameters
        self.url = 'http://matrix.mapzen.com/isochrone?json='
        #self.api_key = self.dlg.lineEdit.text()
        #self.Latitude = self.dlg.lineEdit_2.text()
        #self.Longitude = self.dlg.lineEdit_3.text()
        #self.Minutes = self.dlg.spinBox.value()
        #self.CostModel = self.dlg.comboBox.currentText
        
        self.api_key = 'mapzen-bhbvdDT'
        self.Latitude = '32.734176'
        self.Longitude = '-97.333325'
        self.Minutes = '5'
        self.CostModel = 'auto'


        #Define API GET String
        #getString = '{}{"locations":[{"lat":{}{},"lon":{}}],"costing":"{}","contours":[{"time":{},"color":"ff0000"}]}&id=MapzenIsochr#one&api_key={}'.format(self.url, self.Latitude, self.Longitude, self.CostModel, self.Minutes, self.api_key)
     
 
        getConcat = ''.join([self.url,'{"locations":[{"lat":', self.Latitude, ',"lon":', self.Longitude, '}],"costing":"', self.CostModel, '","contours":[{"time":', self.Minutes, ',"color":"ff0000"}]}&id=isochroneTest&api_key=', self.api_key])
        
        getString = """http://matrix.mapzen.com/isochrone?json={"locations":[{"lat":32.734176,"lon":-97.333325}],"costing":"pedestrian","contours":[{"time":15,"color":"ff0000"}]}&id=Walk_From_Office&api_key=mapzen-bhbvdDT"""
        
        
        
        response = requests.get(getConcat)
        root = json.loads(response.text);
        
        QgsMessageLog.logMessage(getConcat)
        #QgsMessageLog.logMessage("response")
        QMessageBox.information(None, "DEBUG:", str(root)) 
        #QgsMessageLog.logMessage(str(root)) 
        geojson = root

    #geom = QgsGeometry.fromPolygon([[QgsPoint(pt[0],pt[1])  for pt in geojson['features'][0] [0]]])

	#error = QgsVectorFileWriter.writeAsVectorFormat("geojson", geojson, "utf-8", None, "GeoJSON")
        ##Select point-of-origin on map
    def enableOne(self):
        if self.dlg.radioButton.isChecked() == True:
            QgsMessageLog.logMessage("it is checked")
            self.dlg.pointButton.setEnabled(True)
        else:
                self.dlg.pointButton.setEnabled(False)	
	    ##Use point later as point(s)-of-origin
    def enableTwo(self):
        if self.dlg.radioButton_2.isChecked():
            self.dlg.comboBox_2.setEnabled(True)
        else:
            self.dlg.comboBox_2.setEnabled(False)
            QgsMessageLog.logMessage("it annoying")
	##Input Latitude and Longitude
    def enableThree(self):	
        if self.dlg.radioButton_3.isChecked():
            self.dlg.lineEdit_2.setEnabled(True)
            self.dlg.lineEdit_3.setEnabled(True)
        else:
            self.dlg.lineEdit_2.setEnabled(False)
            self.dlg.lineEdit_3.setEnabled(False)

	
	
	#string = json.dumps(root)
	#geom = ogr.CreateGeometryFromJson(string)
	#geom = QgsGeometry.fromWkt(point.ExportToWkt())
    #
	#
	#
	#layer = QgsVectorLayer(str(geojson),"rooty","ogr")
	#QgsMapLayerRegistry.instance().addMapLayer(layer)

	

	

	
	#print root
	
	#self.Fname = “John”
	#self.Lname = “Doe”
	#selfAge = “24”
	#print “{} {} is {} years old.“ format(fname, lname, age)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
