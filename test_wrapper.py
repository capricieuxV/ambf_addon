import bpy
import subprocess
import os

class RunAMBFOperator(bpy.types.Operator):
    bl_idname = "wm.run_ambf"
    bl_label = "Run AMBF"
    
    def execute(self, context):
        # Get the file path from the scene properties
        file_path = bpy.path.abspath(context.scene.ambf_file_path)  # Convert to absolute path if necessary

        # Ensure file path is provided and valid
        if file_path and os.path.isfile(file_path):
            # Update the command to include the file path
            command = f"~/ambf/bin/lin-x86_64/ambf_simulator -a \"{file_path}\""
            subprocess.Popen(command, shell=True, executable="/bin/bash")  # Ensure it's executed with bash
            self.report({'INFO'}, f"Running command: {command}")
        else:
            self.report({'ERROR'}, "No valid file path provided.")
        
        return {'FINISHED'}

class AMBF_PT_Panel(bpy.types.Panel):
    bl_label = "AMBF Simulator"
    bl_idname = "AMBF_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AMBF'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add a file path picker to the UI
        layout.prop(scene, "ambf_file_path")  # Display the file path input in the panel
        layout.operator("wm.run_ambf")  # Add the "Run AMBF" button

def register():
    bpy.utils.register_class(RunAMBFOperator)
    bpy.utils.register_class(AMBF_PT_Panel)
    
    # Add a file path property to the scene to store the selected file
    bpy.types.Scene.ambf_file_path = bpy.props.StringProperty(
        name="File Path",
        description="Path to the AMBF simulation file",
        subtype='FILE_PATH'
    )

def unregister():
    bpy.utils.unregister_class(RunAMBFOperator)
    bpy.utils.unregister_class(AMBF_PT_Panel)

    # Remove the file path property when unregistering
    del bpy.types.Scene.ambf_file_path

if __name__ == "__main__":
    register()
