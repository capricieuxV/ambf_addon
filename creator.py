import bpy

'''
WORKSPACE OPERATIONS
'''
class CleanWorkspace(bpy.types.Operator):
    """Clean all objects not in any scene"""
    bl_idname = "object.clean_workspace"
    bl_label = "Clean Workspace"

    def execute(self, context):
        # Get all objects that are part of the current scene
        scene_objects = set(context.scene.objects)
        # Get all objects in the data
        all_objects = set(bpy.data.objects)
        # Calculate the difference
        orphan_objects = all_objects - scene_objects

        # Remove objects that are not part of any scene
        for obj in orphan_objects:
            # Data-blocks users counter doesn't update in the undo/redo stack, hence obj.users > 0 condition is added
            if obj.users == 0:
                bpy.data.objects.remove(obj, do_unlink=True)

        return {'FINISHED'}

class OBJECT_PT_Workspace_Main_Panel(bpy.types.Panel):
    """Panel for Workspace Operations"""
    bl_label = "Workspace Operations"
    bl_idname = "OBJECT_PT_workspace_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Helper"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Perform Workspace Operations Here")

        col = layout.column()
        col.separator()
        col.operator("object.clean_workspace", text="Clean Workspace")


'''
GEOMETRY OPERATIONS
'''
class OBJECT_PT_Geometry_Main_Panel(bpy.types.Panel):
    """Panel for Geometry Operations"""
    bl_label = "Geometry Operations"
    bl_idname = "OBJECT_PT_geometry_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Helper"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Perform Geometry Operations Here")

        col = layout.column()
        col.operator("mesh.add_cube", text="Add Cube")
        col.operator("mesh.add_sphere", text="Add Sphere")
        col.operator("mesh.add_cylinder", text="Add Cylinder")

        col = layout.column()
        col.separator()
        col.operator("object.select_all", text="Select All").action = 'SELECT'
        col.operator("object.select_all", text="Deselect All").action = 'DESELECT'
        
        col = layout.column()
        # add layout divider
        col.separator()
        col.operator("object.delete_all_objects", text="Delete All")
        col.operator("object.delete_selected_objects", text="Delete Selected")

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
    
class DeleteSelectedObjects(bpy.types.Operator):
    """Delete selected objects in the scene"""
    bl_idname = "object.delete_selected_objects"
    bl_label = "Delete Selected Objects"

    def execute(self, context):
        bpy.ops.object.delete(use_global=False)
        return {'FINISHED'}

'''
CAMERA OPERATIONS
'''
class SetActiveCamera(bpy.types.Operator):
    """Set a camera as the active camera"""
    bl_idname = "scene.set_active_camera"
    bl_label = "Set Active Camera"

    camera_name: bpy.props.StringProperty() 

    def execute(self, context):
        camera = bpy.data.objects.get(self.camera_name)
        if camera and camera.type == 'CAMERA':
            context.scene.camera = camera
            self.report({'INFO'}, f"Active camera set to: {camera.name}")
        else:
            self.report({'ERROR'}, "No camera found with the given name")
        return {'FINISHED'}

class OBJECT_PT_Camera_Panel(bpy.types.Panel):
    """Panel for Camera Operations"""
    bl_label = "Camera Operations"
    bl_idname = "OBJECT_PT_camera_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Set Active Camera")
        # Iterate through all cameras in the scene and create a button for each
        for obj in scene.objects:
            if obj.type == 'CAMERA':
                op = layout.operator("scene.set_active_camera", text=obj.name)
                op.camera_name = obj.name  # Pass the camera name to the operator

def register():
    print("\nStart Helper Panel...")
    bpy.utils.register_class(OBJECT_PT_Geometry_Main_Panel)
    bpy.utils.register_class(OBJECT_PT_Camera_Panel)
    bpy.utils.register_class(OBJECT_PT_Workspace_Main_Panel)
    bpy.utils.register_class(AddCube)
    bpy.utils.register_class(AddSphere)
    bpy.utils.register_class(AddCylinder)
    bpy.utils.register_class(DeleteAllObjects)
    bpy.utils.register_class(DeleteSelectedObjects)
    bpy.utils.register_class(SetActiveCamera)
    bpy.utils.register_class(CleanWorkspace)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_Geometry_Main_Panel)
    bpy.utils.unregister_class(OBJECT_PT_Camera_Panel)
    bpy.utils.unregister_class(OBJECT_PT_Workspace_Main_Panel)
    bpy.utils.unregister_class(AddCube)
    bpy.utils.unregister_class(AddSphere)
    bpy.utils.unregister_class(AddCylinder)
    bpy.utils.unregister_class(DeleteAllObjects)
    bpy.utils.unregister_class(DeleteSelectedObjects)
    bpy.utils.register_class(SetActiveCamera)
    bpy.utils.unregister_class(CleanWorkspace)

if __name__ == "__main__":
    register()