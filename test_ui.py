import bpy
import os

class StartCubeAdderOperator(bpy.types.Operator):
    bl_idname = "wm.start_cube_adder"
    bl_label = "Start Cube Adder"

    def execute(self, context):
        script_path = "/Users/capricieuxv/Desktop/JHU/Core/CIS/CIS2/ambf_addon/add_cube_ui.py"
        
        # Ensure the script file exists
        if not os.path.exists(script_path):
            self.report({'ERROR'}, f"Script not found: {script_path}")
            return {'CANCELLED'}
        
        # Start the external script using Blender's Python
        bpy.ops.wm.console_toggle()  # Open the system console to see print statements
        exec(compile(open(script_path).read(), script_path, 'exec'))
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(StartCubeAdderOperator.bl_idname)

def register():
    bpy.utils.register_class(StartCubeAdderOperator)
    bpy.types.TOPBAR_MT_file.append(menu_func)

def unregister():
    bpy.utils.unregister_class(StartCubeAdderOperator)
    bpy.types.TOPBAR_MT_file.remove(menu_func)

if __name__ == "__main__":
    register()
