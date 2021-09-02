bl_info = {
    "name": "RigifyRootmotion",
    "author": "sga",
    "version": (0, 1),
    "blender": (2, 93, 0),
    "description": "Transfer location&rotation from ControlRig to object. in order to make rootmotion animation for unreal5.",
    "warning": "have many unexpect situation",
    "wiki_url": "",
    "category": "Animation",
}
import bpy

def bakeSelected():
    #   bake the animation
    bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start, frame_end=bpy.context.scene.frame_end, only_selected=True, visual_keying=True, use_current_action=True, bake_types={'POSE'})
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    while bpy.context.scene.frame_current <= bpy.context.scene.frame_end :
    
        bpy.ops.transform.translate(value=(0, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=4.59497, use_proportional_connected=False, use_proportional_projected=False)
        
        bpy.context.scene.frame_current += 1
        
def reflash():
# reflash posebone information
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')
        
        
        
def setOffset(torso,origin):
    #    set offsetsL
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    tempvector = [0,0,0]
    #   bool setting
    LX=bpy.context.scene.LX
    LY=bpy.context.scene.LY
    LZP=bpy.context.scene.LZP
    LZN=bpy.context.scene.LZN
    offset = []
    
    while bpy.context.scene.frame_current <= bpy.context.scene.frame_end :
        reflash()
        tempvector = [0,0,0]
        if LX:
            tempvector[0] = torso.location[0] - origin[0]
        if LY:
            tempvector[1] = torso.location[1] - origin[1]
        if LZP:
            if torso.location[2] > origin[2]:
                tempvector[2] = torso.location[2] - origin[2]
        if LZN:
            if torso.location[2] < origin[2]:
                tempvector[2] = torso.location[2] - origin[2]
        offset.append(tempvector) 
        bpy.context.scene.frame_current += 1
    print(LX,LY,LZP,LZN)
    print(offset)
    return offset
        
def setRotation(torso,originR):
    torso.rotation_mode = 'QUATERNION'
#    torso.rotation_mode = 'XYZ'
#    RX=bpy.context.scene.RX
#    RY=bpy.context.scene.RY
    RZ=bpy.context.scene.RZ
    rotation = []
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    while bpy.context.scene.frame_current <= bpy.context.scene.frame_end :
        reflash()
        torso.rotation_mode = 'XYZ'
        temp = torso.rotation_euler[2] - originR
        if not RZ:
            temp = 0
        rotation.append(temp)
        torso.rotation_mode = 'QUATERNION'
        bpy.context.scene.frame_current += 1
        
    print(rotation)
    return rotation


def setOrigin():
    bpy.context.scene.frame_current = bpy.context.scene.frame_start - 1
    reflash()
    origin = bpy.context.active_pose_bone.location.copy()
    return origin

def setOriginR(torso):
    bpy.context.scene.frame_current = bpy.context.scene.frame_start - 1
    reflash()
    torso.rotation_mode = 'XYZ'
    originR = torso.rotation_euler[2]
    torso.rotation_mode = 'QUATERNION'
    return originR
    
def applyOffset(offset):
    #   move keyframes
    bpy.ops.object.mode_set(mode='POSE') 
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    
    while bpy.context.scene.frame_current <= bpy.context.scene.frame_end :
        i=bpy.context.scene.frame_current-bpy.context.scene.frame_start
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.transform.translate(value=(offset[i][0], offset[i][1], offset[i][2]), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=4.59497, use_proportional_connected=False, use_proportional_projected=False)
        
        bpy.ops.object.mode_set(mode='POSE')

        bpy.ops.transform.translate(value=(-offset[i][0], -offset[i][1], -offset[i][2]), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=4.59497, use_proportional_connected=False, use_proportional_projected=False)
        
        bpy.context.scene.frame_current += 1
        
def applyRotation(rotation):
    # rotate
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    
    while bpy.context.scene.frame_current <= bpy.context.scene.frame_end :
        i=bpy.context.scene.frame_current-bpy.context.scene.frame_start
        reflash()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.transform.rotate(value=rotation[i] , orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=4.59497, use_proportional_connected=False, use_proportional_projected=False, center_override=bpy.context.selected_objects[0].location)
        
        bpy.ops.object.mode_set(mode='POSE')
        
        bpy.ops.transform.rotate(value=-rotation[i] , orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=4.59497, use_proportional_connected=False, use_proportional_projected=False, center_override=bpy.context.selected_objects[0].location)
    
        bpy.context.scene.frame_current += 1
        
        
def main(context):
    
#   get three main kind of bone
    ikbones = bpy.context.selected_pose_bones
    torso = bpy.context.active_pose_bone
    root = bpy.context.selected_objects
    ikbones.remove(torso)
#   set basic value
    basicAI = bpy.context.scene.tool_settings.use_keyframe_insert_auto
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    origin = setOrigin()
    originR = setOriginR(torso)
    offset = []
    rotation = []
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = True
    
#   bake the animation    
    bakeSelected()
        
#   set offset&rotation
    offset = setOffset(torso,origin)
    rotation = setRotation(torso,originR)
    
#   move keyframes
    applyOffset(offset)
    applyRotation(rotation)
    
    #finish reset value
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = basicAI
        
    
        
def bool(): 
    origin = setOriginR(bpy.context.active_pose_bone)
    setRotation(bpy.context.active_pose_bone , origin)
    
#    bpy.context.active_pose_bone.rotation_mode = 'XYZ'
#    print(bpy.context.active_pose_bone.rotation_euler[2])
#    bpy.context.active_pose_bone.rotation_mode = 'QUATERNION'

    
class RigifyRootmotion(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "make rootmotion"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
#        add code here

#        bool()
        main(context)
        
        return {'FINISHED'}
    
    

class RigifyRootmotionLayout(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Rigify to UE rootmotion"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Big render button
        layout.label(text="select all ik , make root resource active")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.simple_operator")
        
        layout.label(text="rootmotion include setting:")
        
        row = layout.row()
        row.prop(context.scene, 'LX')
        row.prop(context.scene, 'LY')
        row.prop(context.scene, 'LZP')
        row.prop(context.scene, 'LZN')
        
        row = layout.row()
#        row.prop(context.scene, 'RX')
#        row.prop(context.scene, 'RY')
        row.prop(context.scene, 'RZ')
        
        







def register():
    bpy.utils.register_class(RigifyRootmotionLayout)
    bpy.utils.register_class(RigifyRootmotion)
    
    bpy.types.Scene.LX = bpy.props.BoolProperty(name="LX" , description="include X-axis" , default=True)
    bpy.types.Scene.LY = bpy.props.BoolProperty(name="LY" , description="include Y-axis" , default=True)
    bpy.types.Scene.LZP = bpy.props.BoolProperty(name="+LZ" , description="include +Z-axis" , default=False)
    bpy.types.Scene.LZN = bpy.props.BoolProperty(name="-LZ" , description="include -Z-axis" , default=False)
#    bpy.types.Scene.RX = bpy.props.BoolProperty(name="RX" , description="include X rotation" , default=False)
#    bpy.types.Scene.RY = bpy.props.BoolProperty(name="RY" , description="include Y rotation" , default=False)
    bpy.types.Scene.RZ = bpy.props.BoolProperty(name="RZ" , description="include Z rotation" , default=False)
    



def unregister():
    bpy.utils.unregister_class(RigifyRootmotionLayout)
    bpy.utils.unregister_class(RigifyRootmotion)
    



if __name__ == "__main__":
    register()



    