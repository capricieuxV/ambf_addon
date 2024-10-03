import bpy
import mathutils

def normalize_name(name):
    """Normalize names by removing spaces and converting to lower case."""
    return name.replace(' ', '').lower()

def find_object_by_normalized_name(normalized_name):
    """Find an object in all Blender objects by its normalized name."""
    for obj in bpy.data.objects:
        name = normalize_name(obj.name)
        if name == normalized_name:
            return obj
    return None

def find_object_in_collections(object_name):
    """Find an object by its name in all collections."""
    for collection in bpy.data.collections:
        for obj in collection.objects:
            if obj.name == object_name:
                return obj
    return None

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

def register():
    bpy.types.Scene.stop_service = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(ServiceROS)
    bpy.utils.register_class(StopServiceROS)
    bpy.utils.register_class(PT_ROS_Service_Panel)

def unregister():
    bpy.utils.unregister_class(ServiceROS)
    bpy.utils.unregister_class(StopServiceROS)
    bpy.utils.unregister_class(PT_ROS_Service_Panel)
    del bpy.types.Scene.stop_service

if __name__ == "__main__":
    register()