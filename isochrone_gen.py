# -*- coding: utf-8 -*-
"""
Created by: Ethan Monk
			ethangmonk@gmail.com
			20170515

"""


from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from mapzen_isochrones_dialog import MapzenIsochronesDialog
import os.path



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
	
	
	# Populate comboBox_2 with all point file layers
	#for layer in qgis.utils.iface.legendInterface().layers():
    #        layerType = layer.type()
    #        if layerType == QgsMapLayer.VectorLayer and layer.wkbType() == QGis.WKBPoint:
    #            self.dlg.comboBox_2.addItem(layer.name())
    #              
    