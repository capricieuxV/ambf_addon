import bpy
import subprocess
import os
import platform

class RunAMBFOperator(bpy.types.Operator):
    bl_idname = "wm.run_ambf"
    bl_label = "Run AMBF"

    command: bpy.props.StringProperty(name="Command", default="")

    def execute(self, context):
        # Get the file path from the scene properties and convert to absolute path
        file_path = bpy.path.abspath(context.scene.ambf_file_path)

        # Check if the file path is valid
        if file_path and os.path.isfile(file_path):
            # Determine GUI mode based on checkbox state
            gui_option = "" if context.scene.with_gui else " -g 0 "

            # Additional options based on checkbox states
            physics_freq_option = f" -p {context.scene.physics_frequency} " if context.scene.enable_physics_freq else ""
            haptics_freq_option = f" -d {context.scene.haptics_frequency} " if context.scene.enable_haptics_freq else ""
            file_option = f" -a \"{file_path}\""

            # Form the full command
            command = f"ambf_simulator{gui_option}{physics_freq_option}{haptics_freq_option}{file_option}"

            # Platform-specific handling
            system = platform.system()
            machine = platform.machine()

            if system == "Darwin" and machine == "arm64":
                # macOS on ARM (Apple M1/M2 or later)
                command = f"source ~/.zshrc && {command}"
                subprocess.Popen(command, shell=True, executable="/bin/zsh")
            elif system == "Linux":
                # Linux (could be x86_64 or ARM64)
                subprocess.Popen(command, shell=True, executable="/bin/bash")
            elif system == "Windows":
                # Windows (run using cmd or PowerShell)
                subprocess.Popen(command, shell=True, executable="cmd.exe")
            else:
                self.report({'ERROR'}, "Unsupported operating system")
                return {'CANCELLED'}

            self.report({'INFO'}, f"Running command: {command}")
        else:
            self.report({'ERROR'}, "No valid file path provided.")
        
        return {'FINISHED'}

def update_commands(scene, context):
    """ Update command templates with the selected file path """
    file_path = bpy.path.abspath(scene.ambf_file_path)
    if file_path:
        scene.regular_cmd = f'ambf_simulator -a "{file_path}"'

class AMBF_PT_Panel(bpy.types.Panel):
    bl_label = "AMBF Simulator"
    bl_idname = "AMBF_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AMBF'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add markdown-like label with clickable link
        row = layout.row()
        row.label(text="AMBF Command-line Guide:")
        row.operator("wm.url_open", text="Command-Line-Arguments").url = "https://github.com/WPI-AIM/ambf/wiki/Command-Line-Arguments"

        # File picker for the ADF file
        layout.prop(scene, "ambf_file_path")

        # Checkbox for GUI option
        layout.prop(scene, "with_gui")

        # Additional options with checkboxes
        layout.prop(scene, "enable_physics_freq", text="Set Physics Update Frequency")
        if scene.enable_physics_freq:
            layout.prop(scene, "physics_frequency")

        layout.prop(scene, "enable_haptics_freq", text="Set Haptics Update Frequency")
        if scene.enable_haptics_freq:
            layout.prop(scene, "haptics_frequency")

        # Run button
        layout.operator("wm.run_ambf", text="Run AMBF Simulator")

def register():
    bpy.utils.register_class(RunAMBFOperator)
    bpy.utils.register_class(AMBF_PT_Panel)

    # Registering properties to store file paths and options
    bpy.types.Scene.ambf_file_path = bpy.props.StringProperty(
        name="File Path",
        description="Path to the AMBF simulation file",
        subtype='FILE_PATH',
        update=update_commands  # Automatically update commands when the file path changes
    )

    bpy.types.Scene.with_gui = bpy.props.BoolProperty(
        name="With GUI",
        description="Run with GUI enabled",
        default=True
    )

    bpy.types.Scene.enable_physics_freq = bpy.props.BoolProperty(
        name="Enable Physics Frequency",
        description="Enable setting physics update frequency",
        default=False
    )

    bpy.types.Scene.physics_frequency = bpy.props.IntProperty(
        name="Physics Frequency",
        description="Set the physics update frequency",
        default=1000,
        min=1
    )

    bpy.types.Scene.enable_haptics_freq = bpy.props.BoolProperty(
        name="Enable Haptics Frequency",
        description="Enable setting haptics update frequency",
        default=False
    )

    bpy.types.Scene.haptics_frequency = bpy.props.IntProperty(
        name="Haptics Frequency",
        description="Set the haptics update frequency",
        default=1000,
        min=1
    )

def unregister():
    bpy.utils.unregister_class(RunAMBFOperator)
    bpy.utils.unregister_class(AMBF_PT_Panel)

    # Unregistering properties
    del bpy.types.Scene.ambf_file_path
    del bpy.types.Scene.with_gui
    del bpy.types.Scene.enable_physics_freq
    del bpy.types.Scene.physics_frequency
    del bpy.types.Scene.enable_haptics_freq
    del bpy.types.Scene.haptics_frequency

if __name__ == "__main__":
    register()
