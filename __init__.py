# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapzenIsochrones
                                 A QGIS plugin
 This plugin generates travel-time isocrhones via the Mapzen Isochrone service API
                             -------------------
        begin                : 2017-05-15
        copyright            : (C) 2017 by Ethan Monk
        email                : ethangmonk@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MapzenIsochrones class from file MapzenIsochrones.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mapzen_isochrones import MapzenIsochrones
    return MapzenIsochrones(iface)
