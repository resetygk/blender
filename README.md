# blender

玩ue5没有合适的资源，所以为了用rigify直接做根骨骼动画，写了简单的插件。


使用方法：  
菜单在属性栏的视图选项里  
0：备份动画  
1：选择所有控制身体的骨骼（rigify里的人形模板有：手脚的IK和torso）  
2：再选上根运动来源作为活动物体（直接用torso也行）  
3：在菜单选择需要的根运动（l是位移，r是旋转）  
4：按执行按钮   

ui appear in scene option  
0: copy the animation  
1: select all body control bones(in rigify human bone they are hand&footik and torso)  
2: also select rootmotion resouce bone make it active(it could be torso)  
3: use UI choose which kind of movement is needed(l=location r=rotation)  
4: hit make root motion button  

注意： 
确保选择所有骨骼后按g移动可以正常的移动整个身体。  
比如：在没取消rigify自带的root和ik骨骼的父级关联时同时选择他们并移动，会造成部份骨骼移动多倍距离。 

warning:  
make sure you can move hole body correctly with press g after choose bones.  
for example: using rigify,without cancel ik parent to root but choose both ikbone and root, ikbone will move double distance, that may cause trouble.  
