import bpy
import os
import subprocess

class RunAMBFOperator(bpy.types.Operator):
    bl_idname = "wm.run_ambf"
    bl_label = "Run AMBF"
    
    file_path: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')

    def execute(self, context):
        if self.file_path:
            command = f"ambf_simulator -a \"{self.file_path}\""
            subprocess.Popen(command, shell=True)
            self.report({'INFO'}, f"Running command: {command}")
        else:
            self.report({'ERROR'}, "No file path provided.")
        return {'FINISHED'}

class AMBFPanel(bpy.types.Panel):
    bl_label = "AMBF Simulator"
    bl_idname = "PT_AMBF_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AMBF'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "ambf_file_path")
        layout.operator("wm.run_ambf")

def register():
    bpy.utils.register_class(RunAMBFOperator)
    bpy.utils.register_class(AMBFPanel)
    bpy.types.Scene.ambf_file_path = bpy.props.StringProperty(
        name="File Path", 
        description="Path to the AMBF file",
        subtype='FILE_PATH'
    )

def unregister():
    bpy.utils.unregister_class(RunAMBFOperator)
    bpy.utils.unregister_class(AMBFPanel)
    del bpy.types.Scene.ambf_file_path

if __name__ == "__main__":
    register()
