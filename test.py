import bpy
import mathutils

class AMBFConnectBaseLinkOperator(bpy.types.Operator):
    """Operator to connect to AMBF and send commands to 'base_link'"""
    bl_idname = "object.connect_ambf_base_link"
    bl_label = "Connect and Command Base Link"

    def execute(self, context):
        from ambf_client import Client
        client = Client()
        client.connect()

        base_link = client.get_obj_handle("base_link")
        
        if base_link:
            # Example command: set angular velocity
            # Set to zero angular velocity for demonstration
            # You can modify the parameters (0, 0, -1) as needed
            base_link.set_angular_vel(0, 0, -1)
            self.report({'INFO'}, "Command sent to base_link")
        else:
            self.report({'ERROR'}, "Failed to get handle for base_link")
        
        return {'FINISHED'}

class AMBFPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "AMBF Base Link Command Panel"
    bl_idname = "OBJECT_PT_ambf"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AMBF_Commands'

    def draw(self, context):
        layout = self.layout
        layout.operator(AMBFConnectBaseLinkOperator.bl_idname)

def register():
    bpy.utils.register_class(AMBFConnectBaseLinkOperator)
    bpy.utils.register_class(AMBFPanel)

def unregister():
    bpy.utils.unregister_class(AMBFConnectBaseLinkOperator)
    bpy.utils.unregister_class(AMBFPanel)

if __name__ == "__main__":
    register()
