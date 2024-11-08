bl_info = {
    "name": "Collection Manager",
    "blender": (4, 0, 0),
    "category": "Object",
}

import bpy

# Property to keep track of selected collections
def update_selected_collections(self, context):
    selected_collections = self.selected_collections.split(',')
    for collection in bpy.data.collections:
        collection.hide_viewport = collection.name not in selected_collections

bpy.types.Scene.selected_collections = bpy.props.StringProperty(
    name="Selected Collections",
    description="Comma-separated list of selected collection names",
    default="",
    update=update_selected_collections
)

bpy.types.Scene.new_collection_name = bpy.props.StringProperty(
    name="New Collection Name",
    description="Name of the new collection",
    default="New Collection"
)

bpy.types.Scene.active_collection_name = bpy.props.StringProperty(
    name="Active Collection Name",
    description="Name of the active collection",
    default=""
)

class CollectionSelectorPanel(bpy.types.Panel):
    bl_label = "Collection Manager"
    bl_idname = "OBJECT_PT_collection_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Collection Manager"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Active Collection Box at the Top
        box = layout.box()
        row = box.row()
        row.label(text="Active Collection:", icon='OUTLINER_OB_GROUP_INSTANCE')
        row = box.row()
        row.label(text=f"{scene.active_collection_name}" if scene.active_collection_name else "None")

        layout.separator()

        # Collection Selection
        box = layout.box()
        box.label(text="Select Collections to Show:", icon='OUTLINER_COLLECTION')

        selected_collections = scene.selected_collections.split(',')
        active_collection = scene.active_collection_name
        
        for collection in bpy.data.collections:
            row = box.row(align=True)
            is_selected = collection.name in selected_collections
            is_active = collection.name == active_collection

            if is_active:
                row.alert = True
            elif not is_selected:
                row.enabled = False

            row.prop(collection, "hide_viewport", text=collection.name, toggle=True)
            op = row.operator("view3d.activate_collection", text="", icon='RESTRICT_SELECT_OFF' if is_active else 'RADIOBUT_OFF')
            op.collection_name = collection.name
            op = row.operator("view3d.delete_collection", text="", icon='X')
            op.collection_name = collection.name

        layout.separator()

        # Add New Collection
        box = layout.box()
        box.label(text="Add New Collection:", icon='ADD')
        row = box.row(align=True)
        row.prop(scene, "new_collection_name", text="")
        row.operator("view3d.add_collection", text="", icon='ADD')

class ToggleCollectionSelectionOperator(bpy.types.Operator):
    bl_idname = "view3d.toggle_collection_selection"
    bl_label = "Toggle Collection Selection"
    
    collection_name: bpy.props.StringProperty()
    
    def execute(self, context):
        scene = context.scene
        selected_collections = scene.selected_collections.split(',')
        
        if self.collection_name in selected_collections:
            selected_collections.remove(self.collection_name)
        else:
            selected_collections.append(self.collection_name)
        
        scene.selected_collections = ','.join(selected_collections)
        return {'FINISHED'}

class ActivateCollectionOperator(bpy.types.Operator):
    bl_idname = "view3d.activate_collection"
    bl_label = "Activate Collection"
    
    collection_name: bpy.props.StringProperty()
    
    def execute(self, context):
        scene = context.scene
        context.scene.active_collection_name = self.collection_name
        
        # Automatically select the collection checkbox when activated
        selected_collections = scene.selected_collections.split(',')
        if self.collection_name not in selected_collections:
            selected_collections.append(self.collection_name)
            scene.selected_collections = ','.join(selected_collections)
        
        # Ensure the collection is shown by updating the selected collections
        update_selected_collections(scene, context)
        
        self.report({'INFO'}, f"Collection '{self.collection_name}' Activated and Shown")
        return {'FINISHED'}

class DeleteCollectionOperator(bpy.types.Operator):
    bl_idname = "view3d.delete_collection"
    bl_label = "Delete Collection"
    
    collection_name: bpy.props.StringProperty()
    
    def execute(self, context):
        collection = bpy.data.collections.get(self.collection_name)
        if collection:
            bpy.data.collections.remove(collection)
            # Update selected collections after deletion
            selected_collections = context.scene.selected_collections.split(',')
            if self.collection_name in selected_collections:
                selected_collections.remove(self.collection_name)
                context.scene.selected_collections = ','.join(selected_collections)
            # Clear active collection if it's the one being deleted
            if context.scene.active_collection_name == self.collection_name:
                context.scene.active_collection_name = ""
            self.report({'INFO'}, f"Collection '{self.collection_name}' Deleted")
        else:
            self.report({'WARNING'}, f"Collection '{self.collection_name}' not found")
        return {'FINISHED'}

class AddCollectionOperator(bpy.types.Operator):
    bl_idname = "view3d.add_collection"
    bl_label = "Add Collection"
    
    def execute(self, context):
        scene = context.scene
        collection_name = scene.new_collection_name.strip()
        if collection_name:
            new_collection = bpy.data.collections.new(name=collection_name)
            bpy.context.scene.collection.children.link(new_collection)
            scene.selected_collections = ','.join(scene.selected_collections.split(',') + [collection_name])
            self.report({'INFO'}, f"Collection '{collection_name}' Added")
        else:
            self.report({'WARNING'}, "Collection name cannot be empty")
        return {'FINISHED'}

# Hook to ensure new objects are added to the active collection
def ensure_active_collection(scene):
    if scene.active_collection_name:
        active_collection = bpy.data.collections.get(scene.active_collection_name)
        if active_collection:
            for obj in bpy.context.selected_objects:
                for col in obj.users_collection:
                    col.objects.unlink(obj)
                active_collection.objects.link(obj)

def register():
    bpy.utils.register_class(CollectionSelectorPanel)
    bpy.utils.register_class(ToggleCollectionSelectionOperator)
    bpy.utils.register_class(ActivateCollectionOperator)
    bpy.utils.register_class(DeleteCollectionOperator)
    bpy.utils.register_class(AddCollectionOperator)
    bpy.types.Scene.selected_collections = bpy.props.StringProperty(
        name="Selected Collections",
        description="Comma-separated list of selected collection names",
        default="",
        update=update_selected_collections
    )
    bpy.types.Scene.new_collection_name = bpy.props.StringProperty(
        name="New Collection Name",
        description="Name of the new collection",
        default="New Collection"
    )
    bpy.types.Scene.active_collection_name = bpy.props.StringProperty(
        name="Active Collection Name",
        description="Name of the active collection",
        default=""
    )
    bpy.app.handlers.depsgraph_update_post.append(ensure_active_collection)

def unregister():
    bpy.utils.unregister_class(CollectionSelectorPanel)
    bpy.utils.unregister_class(ToggleCollectionSelectionOperator)
    bpy.utils.unregister_class(ActivateCollectionOperator)
    bpy.utils.unregister_class(DeleteCollectionOperator)
    bpy.utils.unregister_class(AddCollectionOperator)
    del bpy.types.Scene.selected_collections
    del bpy.types.Scene.new_collection_name
    del bpy.types.Scene.active_collection_name
    bpy.app.handlers.depsgraph_update_post.remove(ensure_active_collection)

if __name__ == "__main__":
    register()
