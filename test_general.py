import bpy
from bpy.props import (
    FloatVectorProperty,
    CollectionProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
)
from bpy.types import PropertyGroup, Panel

# Define the SensorArrayItem class with explicit bl_idname
class SensorArrayItem(PropertyGroup):
    bl_idname = "OBJECT_PT_sensor_array_item"
    bl_label = "Sensor Array Item"
    
    offset: FloatVectorProperty(
        name="Offset",
        size=3,
        subtype='XYZ',
        default=(0.0, 0.0, 0.0)
    )
    direction: FloatVectorProperty(
        name="Direction",
        size=3,
        subtype='XYZ',
        default=(0.0, -1.0, 0.0)
    )

# Define SensorProperties with ambf_sensor_array using SensorArrayItem
class SensorProperties(PropertyGroup):
    bl_idname = "OBJECT_PT_sensor_properties"
    bl_label = "Sensor Properties"

    ambf_sensor_type: EnumProperty(
        items=[
            ('Proximity', 'Proximity', '', '', 0),
            ('Resistance', 'Resistance', '', '', 1),
            ('Contact', 'Contact', '', '', 2),
        ],
        name="Type",
        default='Proximity'
    )
    
    ambf_sensor_enable_frequency: BoolProperty(
        name="Enable Frequency",
        default=False
    )

    ambf_sensor_frequency: FloatProperty(
        name="Frequency", 
        default=1.0, 
        min=0.0
    )
    
    ambf_object_visible: BoolProperty(
        name="Visible",
        default=False
    )
    
    ambf_object_visible_size: FloatProperty(
        name="Visible Size",
        default=1.0,
        min=0.0
    )

    # Proximity Sensor Properties
    ambf_sensor_range: FloatProperty(
        name="Range",
        default=0.1,
        min=0.0
    )
    
    # Sensor Array Collection for Proximity Sensor
    ambf_sensor_array: CollectionProperty(
        type=SensorArrayItem,
        name="Array"
    )

    # Resistance Sensor Properties
    ambf_sensor_friction_static: FloatProperty(
        name="Static Friction",
        default=0.0,
        min=0.0
    )

    ambf_sensor_friction_damping: FloatProperty(
        name="Damping Friction",
        default=0.0,
        min=0.0
    )

    ambf_sensor_friction_dynamic: FloatProperty(
        name="Dynamic Friction",
        default=0.0,
        min=0.0
    )

    ambf_sensor_friction_variable: BoolProperty(
        name="Variable Friction",
        default=False
    )

    ambf_sensor_contact_area: FloatProperty(
        name="Contact Area",
        default=0.0,
        min=0.0
    )

    ambf_sensor_contact_stiffness: FloatProperty(
        name="Contact Stiffness",
        default=0.0,
        min=0.0
    )

    ambf_sensor_contact_damping: FloatProperty(
        name="Contact Damping",
        default=0.0,
        min=0.0
    )

    # Contact Sensor Properties
    ambf_sensor_distance_threshold: FloatProperty(
        name="Distance Threshold",
        default=0.0,
        min=0.0
    )

    ambf_sensor_process_contact_details: BoolProperty(
        name="Process Contact Details",
        default=False
    )


def register():
    bpy.utils.register_class(SensorArrayItem)
    bpy.utils.register_class(SensorProperties)
    bpy.types.Object.ambf_sensor_properties = bpy.props.PointerProperty(type=SensorProperties)

def unregister():
    bpy.utils.unregister_class(SensorProperties)
    bpy.utils.unregister_class(SensorArrayItem)
    del bpy.types.Object.ambf_sensor_properties

if __name__ == "__main__":
    register()
