from qgis.core import *
from qgis.gui import *



    
@qgsfunction(args='auto', group='Custom')

# Function will be used as map_index( 'index1in50k',map_get(item_variables('main_map'), 'map_extent'),"sh_no")
# ie map_index( index_layer_name,map_get(item_variables(id_of_the_map), 'map_extent'),"attribute_of_the_index_layer")
def map_index(source_layer, map_extent, source_attribute, feature, parent):

    map_layer = QgsProject.instance().mapLayersByName(source_layer)[0]
    map_extent_bounds = map_extent.boundingBox()
    

    records = []
    for f in map_layer.getFeatures():
        f_bounds = f.geometry().boundingBox()
        if map_extent_bounds.intersects(f_bounds):
            field_name_idx = f.fieldNameIndex(source_attribute)
            field_value = f.attributes()[field_name_idx]
            records.append(field_value)
    result = ','.join(records) 
    
            
    return result