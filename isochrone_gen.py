# -*- coding: utf-8 -*-
"""
Created by: Ethan Monk
			ethangmonk@gmail.com
			20170515

"""


from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon

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
import json
import requests



class isochrone_gen:
    def __init__(self, dlg):
        self.dlg = dlg

                  
   
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
                  
    #SET API Parameters
	self.url = 'http://matrix.mapzen.com/isochrone?json='
	self.api_key = self.dlg.lineEdit.text()
	self.Latitude = self.dlg.lineEdit_2.text()
	self.Longitude = self.dlg.lineEdit_3.text()
	self.Minutes = self.dlg.spinBox.value()
	self.CostModel = self.dlg.comboBox.currentText
	
	#Define API GET String
	#getString = #'{"locations":[{"lat":{}{},"lon":{}}],"costing":"{}","contours":[{"time":{},"color":"ff0000"}]}&id=MapzenIsochr#one&api_key={}'.format(self.url, self.Latitude, self.Longitude, self.CostModel, self.Minutes, self.api_key)
	
	
	getString = """http://matrix.mapzen.com/isochrone?json={"locations":[{"lat":32.734176,"lon":-97.333325}],"costing":"pedestrian","contours":[{"time":15,"color":"ff0000"}]}&id=Walk_From_Office&api_key=mapzen-bhbvdDT"""
	
	
	
	response = requests.get(getString)
	root = json.loads(response.text)
	
	
	vlayer = QgsVectorLayer("Polygon?crs=EPSG:4326","root","memory")
	QgsMapLayerRegistry.instance().addMapLayer(vlayer)

	

	
	#QgsMessageLog.logMessage("response")
	QMessageBox.information(None, "DEBUG:", str(root)) 
	
	#print root
	
	#self.Fname = “John”
	#self.Lname = “Doe”
	#selfAge = “24”
	#print “{} {} is {} years old.“ format(fname, lname, age)
	
	
