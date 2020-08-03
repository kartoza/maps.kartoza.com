"""
Define new functions using @qgsfunction. feature and parent must always be the
last args. Use args=-1 to pass a list of values as arguments
"""

from qgis.core import Qgis, QgsProject
from qgis.gui import *
from qgis.utils import qgsfunction, iface

def map_bounds(composer_title):
    projectInstance = QgsProject.instance()
    projectLayoutManager = projectInstance.layoutManager()
    layout = projectLayoutManager.layoutByName(composer_title)
    layout_ref=layout.referenceMap()
    extent= layout_ref.extent()
    return extent

@qgsfunction(args='auto', group='Custom')
def map_x_min(composer_title, feature, parent):
    map_extent = map_bounds(composer_title)
    x_min = map_extent.xMinimum()
    return x_min
    
@qgsfunction(args='auto', group='Custom')
def map_x_max(composer_title, feature, parent):
    map_extent = map_bounds(composer_title)
    x_max = map_extent.xMaximum()
    return x_max
    
@qgsfunction(args='auto', group='Custom')
def map_y_min(composer_title, feature, parent):
    map_extent = map_bounds(composer_title)
    y_min = map_extent.yMinimum()
    return y_min
    
@qgsfunction(args='auto', group='Custom')
def map_y_max(composer_title, feature, parent):
    map_extent = map_bounds(composer_title)
    y_max = map_extent.yMaximum()
    return y_max