import bpy
import mathutils

def normalize_name(name):
    """Normalize names by removing spaces and converting to lower case."""
    return name.replace(' ', '').lower()

def find_object_by_normalized_name(normalized_name):
    """Find an object in all Blender objects by its normalized name."""
    for obj in bpy.data.objects:
        name = obj.name.split('/')[-1].replace(' ', '').lower()
        if normalize_name(name) == normalized_name:
            return obj
    return None

class SelectObjectForVelocityControl(bpy.types.Operator):
    bl_idname = "wm.select_object_velocity_control"
    bl_label = "Select Object for Velocity Control"
    object_name: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.selected_object_velocity_control = self.object_name
        return {'FINISHED'}

class ServiceROS(bpy.types.Operator):
    bl_idname = "wm.ros_service"
    bl_label = "ROS Background Service"
    _timer = None
    _client = None
    is_running = False

    def start_ambf_client(self):
        from ambf_client import Client
        self._client = Client()
        self._client.connect()
        print('--> Connected to AMBF Client')

    def modal(self, context, event):
        if event.type == 'TIMER' and self.is_running:
            self.update_objects(context)
        if context.scene.stop_service:
            return self.cancel(context)
        return {'PASS_THROUGH'}

    def execute(self, context):
        if self.is_running:
            self.report({'WARNING'}, "Service already running")
            return {'CANCELLED'}
        self.start_ambf_client()
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        self.is_running = True
        context.scene.stop_service = False
        return {'RUNNING_MODAL'}
    
    def find_object_in_collections(object_name):
        """Find an object by its name in all collections."""
        for collection in bpy.data.collections:
            for obj in collection.objects:
                if obj.name == object_name:
                    return obj
        return None
        
    # def update_objects(self, context):
    #     obj_names = self._client.get_obj_names()
    #     print(f"Found {len(obj_names)} objects in AMBF")
    #     obj_names = ["/ambf/env/base_link", "/ambf/env/yaw_link"]
    #     for ambf_name in obj_names:
    #         normalized_name = normalize_name(ambf_name.split('/')[-1])
    #         obj = find_object_by_normalized_name(normalized_name)
    #         print(f"Found object {obj} for {ambf_name}")
    #         handle = self._client.get_obj_handle(ambf_name)
    #         if handle is not None and obj is not None:
    #             pose = handle.get_pose()
    #             obj.location = mathutils.Vector(pose[:3])
    #             obj.rotation_euler = mathutils.Euler(pose[3:], 'XYZ')
    #             print(f"Updated object {obj} with pose {pose}")
    #         else:
    #             print(f"Failed to get AMBF handle for {ambf_name}")

    def update_objects(self, context):
        obj_names = self._client.get_obj_names()
        print(f"Found {len(obj_names)} objects in AMBF")
        
        for ambf_name in obj_names:
            normalized_name = normalize_name(ambf_name.split('/')[-1])
            obj = find_object_by_normalized_name(normalized_name)
            print(f"Looking for object matching: {normalized_name}")
            handle = self._client.get_obj_handle(ambf_name)
            
            if handle and obj:
                pose = handle.get_pose()
                obj.location = mathutils.Vector(pose[:3])
                obj.rotation_euler = mathutils.Euler(pose[3:], 'XYZ')
                print(f"Updated {obj.name} to location {pose[:3]} and rotation {pose[3:]}")
            else:
                if not handle:
                    print(f"Failed to get AMBF handle for {ambf_name}")
                if not obj:
                    print(f"No matching object found in Blender for {normalized_name}")


    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        self.is_running = False
        if self._client:
            self._client.clean_up()
        print("--> ROS Service Stopped")
        return {'CANCELLED'}

    def __del__(self):
        self.cancel(bpy.context)

class PT_ROS_Service_Panel(bpy.types.Panel):
    bl_idname = "PT_ROS_Service_Panel"
    bl_label = "ROS Background Service Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ROS Service"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text='ROS Service Control')
        col.operator("wm.ros_service", text="Start ROS Service")
        col.operator("wm.stop_ros_service", text="Stop ROS Service", icon='CANCEL')

class StopServiceROS(bpy.types.Operator):
    bl_idname = "wm.stop_ros_service"
    bl_label = "Stop ROS Background Service"

    def execute(self, context):
        context.scene.stop_service = True
        return {'FINISHED'}
    
class AngularVelocityPanel(bpy.types.Panel):
    bl_idname = "PT_Angular_Velocity_Panel"
    bl_label = "Angular Velocity Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ROS Service"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text='Angular Velocity Control')

        col.prop_search(context.scene, "selected_object_velocity_control", bpy.data, "objects", text="Select Object")

        row = col.row()
        row.prop(context.scene, "angular_velocity_x", text="X")
        row.prop(context.scene, "angular_velocity_y", text="Y")
        row.prop(context.scene, "angular_velocity_z", text="Z")

        col.operator("wm.send_angular_velocity", text="Send Angular Velocity")

class LinearVelocityPanel(bpy.types.Panel):
    bl_idname = "PT_Linear_Velocity_Panel"
    bl_label = "Linear Velocity Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ROS Service"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text='Linear Velocity Control')
        
        col.prop_search(context.scene, "selected_object_velocity_control", bpy.data, "objects", text="Select Object")

        row = col.row()
        row.prop(context.scene, "linear_velocity_x", text="X")
        row.prop(context.scene, "linear_velocity_y", text="Y")
        row.prop(context.scene, "linear_velocity_z", text="Z")

        col.operator("wm.send_linear_velocity", text="Send Linear Velocity")

class SendAngularVelocity(bpy.types.Operator):
    bl_idname = "wm.send_angular_velocity"
    bl_label = "Send Angular Velocity"

    def execute(self, context):
        obj_name = context.scene.selected_object_velocity_control
        x = context.scene.angular_velocity_x
        y = context.scene.angular_velocity_y
        z = context.scene.angular_velocity_z
        if obj_name:
            handler = bpy.context.blend_data.objects[obj_name]._client.get_obj_handle(obj_name) 
            handler.set_angular_velocity(x, y, z)
        return {'FINISHED'}
    
class SendLinearVelocity(bpy.types.Operator):
    bl_idname = "wm.send_linear_velocity"
    bl_label = "Send Linear Velocity"

    def execute(self, context):
        obj_name = context.scene.selected_object_velocity_control
        x = context.scene.linear_velocity_x
        y = context.scene.linear_velocity_y
        z = context.scene.linear_velocity_z
        if obj_name:
            handler = bpy.context.blend_data.objects[obj_name]._client.get_obj_handle(obj_name) 
            handler.set_linear_velocity(x, y, z)

        return {'FINISHED'}

def register():
    bpy.types.Scene.stop_service = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(ServiceROS)
    bpy.utils.register_class(StopServiceROS)
    bpy.utils.register_class(PT_ROS_Service_Panel)

    bpy.types.Scene.selected_object_velocity_control = bpy.props.StringProperty()

    bpy.types.Scene.angular_velocity_x = bpy.props.FloatProperty(default=0.0)
    bpy.types.Scene.angular_velocity_y = bpy.props.FloatProperty(default=0.0)
    bpy.types.Scene.angular_velocity_z = bpy.props.FloatProperty(default=0.0)

    bpy.types.Scene.linear_velocity_x = bpy.props.FloatProperty(default=0.0)
    bpy.types.Scene.linear_velocity_y = bpy.props.FloatProperty(default=0.0)
    bpy.types.Scene.linear_velocity_z = bpy.props.FloatProperty(default=0.0)

    bpy.utils.register_class(LinearVelocityPanel)
    bpy.utils.register_class(SendLinearVelocity)

    bpy.utils.register_class(AngularVelocityPanel)
    bpy.utils.register_class(SendAngularVelocity)

def unregister():
    bpy.utils.unregister_class(ServiceROS)
    bpy.utils.unregister_class(StopServiceROS)
    bpy.utils.unregister_class(PT_ROS_Service_Panel)
    del bpy.types.Scene.stop_service

    del bpy.types.Scene.selected_object_velocity_control
    bpy.utils.unregister_class(LinearVelocityPanel)
    bpy.utils.unregister_class(SendLinearVelocity)

    bpy.utils.unregister_class(AngularVelocityPanel)
    bpy.utils.unregister_class(SendAngularVelocity)

    del bpy.types.Scene.linear_velocity_x
    del bpy.types.Scene.linear_velocity_y
    del bpy.types.Scene.linear_velocity_z

    del bpy.types.Scene.angular_velocity_x
    del bpy.types.Scene.angular_velocity_y
    del bpy.types.Scene.angular_velocity_z

if __name__ == "__main__":
    register()
