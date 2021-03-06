# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapzenIsochrones
                                 A QGIS plugin
 This plugin generates travel-time isochrones via the Mapzen Isochrone service API
                              -------------------
        begin                : 2017-05-22
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Ethan Monk
        email                : ethangmonk@gmail.com
        email                : emonk@trademarkproperty.com
		
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
import isochrone_gen
#import mapzen_isochrones
from mapzen_isochrones_dialog import MapzenIsochronesDialog

import os.path



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




class MapzenIsochrones:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.dlg = MapzenIsochronesDialog()
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MapzenIsochrones_{}.qm'.format(locale))

			
        #Populate comboBox_2 with all point file layers
        for layer in qgis.utils.iface.legendInterface().layers():
                layerType = layer.type()
                if layerType == QgsMapLayer.VectorLayer and layer.wkbType() == QGis.WKBPoint:
                    self.dlg.comboBox_2.addItem(layer.name())

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Mapzen Isochrones')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MapzenIsochrones')
        self.toolbar.setObjectName(u'MapzenIsochrones')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MapzenIsochrones', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = MapzenIsochronesDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/MapzenIsochrones/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Mapzen Isochrones'),
            callback=self.run,
            parent=self.iface.mainWindow())
         
         #Open Links on UserForm 
        self.dlg.label_6.linkActivated.connect(self.OpenURL)
        self.dlg.label_9.linkActivated.connect(self.OpenURL)
        self.dlg.label_10.linkActivated.connect(self.OpenURL)
        self.dlg.label_11.linkActivated.connect(self.OpenURL)
        
    def OpenURL(self, URL): 
        QDesktopServices().openUrl(QUrl(URL))
		 
		 

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&Mapzen Isochrones'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        self.isochrone_gen = isochrone_gen.isochrone_gen(self.dlg)
        #self.mapzen_isochrones = mapzen_isochrones.MapzenIsochrones(self.dlg)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            self.isochrone_gen.apiCall()
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
