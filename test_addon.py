# Author: Adnan Munawar
# Email: amunawar@wpi.edu
# Lab: aimlab.wpi.edu

# Editor: Vanessa Wang
# Email: swang368@jh.edu
# Lab: LCSR, Johns Hopkins University

bl_info = {
    "name": "Asynchronous Multi-Body Framework (AMBF) Config Creator",
    "author": "Adnan Munawar, Shiyue Vanessa Wang",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Add > Mesh > AMBF",
    "description": "Helps Generate AMBF Config File and Saves both High and Low Resolution(Collision) Meshes",
    "warning": "",
    # "wiki_url": "https://github.com/WPI-AIM/ambf_addon",
    "wiki_url": "https://github.com/capricieuxV/ambf__blender_addon",
    "category": "AMBF",
    }

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatVectorProperty, CollectionProperty, PointerProperty
from bpy.types import PropertyGroup, Operator, Panel

class CollectionProperties(PropertyGroup):
    name: StringProperty(name="Collection Name", default="")
    collection_ref: PointerProperty(name="Collection Reference", type=bpy.types.Collection)

def register_custom_properties():
    bpy.types.Collection.mesh_path = StringProperty(name="Meshes (Save To)", default="", description="Define the path to save mesh files", subtype='DIR_PATH')
    bpy.types.Collection.adf_path = StringProperty(name="Config (Save To)", default="", description="Define the root path of the project", subtype='FILE_PATH')
    bpy.types.Collection.namespace = StringProperty(name="AMBF Namespace", default="/ambf/env/", description="The namespace for all bodies in this scene")
    bpy.types.Collection.meshes_save_type = EnumProperty(
        items=[
            ('STL', 'STL', 'STL'),
            ('OBJ', 'OBJ', 'OBJ'),
            ('3DS', '3DS', '3DS'),
            ('PLY', 'PLY', 'PLY')
        ],
        name="Mesh Type",
        default='STL'
    )
    bpy.types.Collection.save_high_res = BoolProperty(name="Save High Res", default=False)
    bpy.types.Collection.save_low_res = BoolProperty(name="Save Low Res", default=False)
    bpy.types.Collection.save_textures = BoolProperty(name="Save Textures", default=False)
    bpy.types.Collection.save_selection_only = BoolProperty(name="Save Selection Only", default=False)
    bpy.types.Collection.model_override_gravity = BoolProperty(name="Override Gravity", default=False)
    bpy.types.Collection.model_gravity = FloatVectorProperty(
        name='Model Gravity',
        default=(0.0, 0.0, -9.8),
        options={'PROPORTIONAL'},
        subtype='XYZ',
    )    
    bpy.types.Collection.ignore_inter_collision = BoolProperty(name="Ignore Inter Collision", default=False)
    bpy.types.Collection.precision = StringProperty(name="Precision", default="")

def update_collection_enum_items(self, context):
    items = [(coll.name, coll.name, "") for coll in bpy.data.collections if coll.name not in [c.name for c in context.scene.ambf_collection_properties]]
    return items

bpy.types.Scene.collection_enum = bpy.props.EnumProperty(items=update_collection_enum_items, name="Collections")

class AddCollectionOperator(Operator):
    bl_idname = "ambf.add_collection"
    bl_label = "Add Collection"

    def execute(self, context):
        selected_collection_name = context.scene.collection_enum
        if selected_collection_name:
            selected_collection = bpy.data.collections[selected_collection_name]
            
            collection_prop = context.scene.ambf_collection_properties.add()
            collection_prop.name = selected_collection.name
            collection_prop.collection_ref = selected_collection
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No collection selected")
            return {'CANCELLED'}

class RemoveCollectionOperator(Operator):
    bl_idname = "ambf.remove_collection"
    bl_label = "Remove Collection"
    index: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.ambf_collection_properties.remove(self.index)
        return {'FINISHED'}

class AMBF_PT_main_panel(Panel):
    bl_label = "IMPORT, MAKE AND EXPORT ADFs"
    bl_idname = "AMBF_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AMBF"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Dropdown to select a collection
        layout.prop(scene, "collection_enum", text="Select Collection")
        layout.operator("ambf.add_collection", text="Add Collection")

        for index, collection in enumerate(scene.ambf_collection_properties):
            box = layout.box()
            row = box.row()
            row.prop(collection, "name", text="")
            row.operator("ambf.remove_collection", text="", icon='X').index = index

            # Section for saving meshes and textures
            sbox = box.box()
            row = sbox.row()
            row.label(text="C. SAVE MESHES + TEXTURES")
            col = sbox.column()
            col.prop(collection.collection_ref, 'mesh_path')
            col.prop(collection.collection_ref, 'meshes_save_type')
            row = sbox.row()
            row.prop(collection.collection_ref, 'save_high_res')
            row.prop(collection.collection_ref, 'save_low_res')
            row.prop(collection.collection_ref, 'save_textures')
            col = sbox.column()
            col.prop(collection.collection_ref, 'save_selection_only')
            col.operator("ambf.save_meshes")

            # Section for saving ADF
            sbox = box.box()
            row = sbox.row()
            row.label(text="D. SAVE ADF")
            col = sbox.column()
            col.prop(collection.collection_ref, "model_override_gravity")
            col.prop(collection.collection_ref, "model_gravity")
            col.prop(collection.collection_ref, "ignore_inter_collision")
            col.prop(collection.collection_ref, "precision")
            col.prop(collection.collection_ref, 'namespace', text='Global NS')
            col.prop(collection.collection_ref, 'adf_path', text='Save As')
            col.operator("ambf.add_generate_ambf_file")

def register():
    bpy.utils.register_class(CollectionProperties)
    bpy.utils.register_class(AddCollectionOperator)
    bpy.utils.register_class(RemoveCollectionOperator)
    bpy.utils.register_class(AMBF_PT_main_panel)
    bpy.types.Scene.ambf_collection_properties = CollectionProperty(type=CollectionProperties)
    bpy.types.Scene.collection_enum = bpy.props.EnumProperty(items=update_collection_enum_items, name="Collections")
    register_custom_properties()

def unregister():
    bpy.utils.unregister_class(CollectionProperties)
    bpy.utils.unregister_class(AddCollectionOperator)
    bpy.utils.unregister_class(RemoveCollectionOperator)
    bpy.utils.unregister_class(AMBF_PT_main_panel)
    del bpy.types.Scene.ambf_collection_properties
    del bpy.types.Scene.collection_enum
    unregister_custom_properties()

def unregister_custom_properties():
    del bpy.types.Collection.mesh_path
    del bpy.types.Collection.adf_path
    del bpy.types.Collection.namespace
    del bpy.types.Collection.meshes_save_type
    del bpy.types.Collection.save_high_res
    del bpy.types.Collection.save_low_res
    del bpy.types.Collection.save_textures
    del bpy.types.Collection.save_selection_only
    del bpy.types.Collection.model_override_gravity
    del bpy.types.Collection.model_gravity
    del bpy.types.Collection.ignore_inter_collision
    del bpy.types.Collection.precision

if __name__ == "__main__":
    register()
