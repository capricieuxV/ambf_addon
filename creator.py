import bpy

class GeometryCreationPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Geometry Creation"
    bl_idname = "GeometryCreationPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Helper"
    
    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("mesh.add_cube", text="Add Cube")
        col.operator("mesh.add_sphere", text="Add Sphere")
        col.operator("mesh.add_cylinder", text="Add Cylinder")

        col = layout.column()
        col.operator("object.select_all", text="Select All").action = 'SELECT'
        col.operator("object.select_all", text="Deselect All").action = 'DESELECT'
        col.operator("object.delete_all_objects", text="Delete All")

class AddCube(bpy.types.Operator):
    """Add a new cube to the scene"""
    bl_idname = "mesh.add_cube"
    bl_label = "Add Cube"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {'FINISHED'}

class AddSphere(bpy.types.Operator):
    """Add a new sphere to the scene"""
    bl_idname = "mesh.add_sphere"
    bl_label = "Add Sphere"

    def execute(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add()
        return {'FINISHED'}

class AddCylinder(bpy.types.Operator):
    """Add a new cylinder to the scene"""
    bl_idname = "mesh.add_cylinder"
    bl_label = "Add Cylinder"

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add()
        return {'FINISHED'}

class DeleteAllObjects(bpy.types.Operator):
    """Delete all objects in the scene"""
    bl_idname = "object.delete_all_objects"
    bl_label = "Delete All Objects"

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(GeometryCreationPanel)
    bpy.utils.register_class(AddCube)
    bpy.utils.register_class(AddSphere)
    bpy.utils.register_class(AddCylinder)
    bpy.utils.register_class(DeleteAllObjects)

def unregister():
    bpy.utils.unregister_class(GeometryCreationPanel)
    bpy.utils.unregister_class(AddCube)
    bpy.utils.unregister_class(AddSphere)
    bpy.utils.unregister_class(AddCylinder)
    bpy.utils.unregister_class(DeleteAllObjects)

if __name__ == "__main__":
    register()