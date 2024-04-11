MODULE Module1
	CONST robtarget Target_10:=[[-529.003035207,80.303076295,365.435851011],[0.146950786,-0.733062687,0.650744536,-0.132499482],[0,-1,-2,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_20:=[[-260.808047737,257.453703802,-13.53784441],[0,0.733479209,-0.679711888,0],[0,0,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_30:=[[-1337.23233355,-7.764594105,858.139152089],[0.485099882,-0.57054828,0.503015768,-0.431425431],[0,0,-2,4],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_40:=[[-1414.741666216,-16.217949066,858.139152089],[0.45768972,-0.533913197,-0.541744313,0.460401909],[2,0,-2,4],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_50:=[[-2450.993614867,-16.217949066,145.985453172],[0.004848444,0.997894757,0.003333472,-0.064586641],[2,0,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_60:=[[-2497.148999582,-12.114412909,-23.223616786],[0,0.99999959,-0.000905828,-0.000000014],[1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST jointtarget pHome:=[[0,-50,-20,0,15,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_70:=[[289.225078504,-1318.424228036,1757.95985414],[0.697977726,-0.256026482,0.298622929,0.598416143],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_80:=[[571.278584042,-772.764314059,564.768982562],[0.050287119,-0.770185744,-0.00923679,-0.635767101],[0,-2,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST jointtarget JointTarget_3:=[[81.216738927,-10.486469953,49.932487235,-90.413450522,72.424213307,-47.977898505],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_90:=[[538.232129582,-927.287307458,135.775838719],[0.000000032,0.707106771,0.000000014,0.707106791],[0,-2,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_100:=[[-332.060874467,-1287.311735915,900.274980848],[0.49932969,-0.500669456,-0.499329669,-0.500669391],[1,-1,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_110:=[[-865.487052643,-1061.399276372,801.2],[0.5,-0.5,-0.5,-0.5],[1,-2,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_120:=[[53.161781285,-1281.48576097,1785.536711273],[0.706342334,-0.707604089,0.000020078,-0.019415434],[1,-1,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_130:=[[-260.808032761,257.453701858,-13.537868172],[-0.000000025,0.709310778,-0.704895893,-0.000000015],[0,0,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    !***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: arkur
    !
    ! Version: 1.0
    !
    !***********************************************************
    
    
    !***********************************************************
    !
    ! Procedure main
    !
    !   This is the entry point of your program
    !
    !***********************************************************
    PROC main()
        
        MoveAbsJ pHome,v1000,z100,Gripper\WObj:=wPick;
        PickFromConv;
        PickLays;
        
        
        
    ENDPROC
    
    
    
    
	PROC PickFromConv()
        
        
        !waitDI DI_PickFromConv, 1;
        
	    WaitDI DI_PickFromConv,1;
	    MoveAbsJ pHome,v1000,z100,Gripper\WObj:=wPick;
	    MoveJ Target_10,v1000,z100,Gripper\WObj:=wPick;
        
        MoveJ Offs(Target_130,0,0,200),v1000,fine,Gripper\WObj:=wPick;
        
        WaitTime 0.5;
        MoveJ Target_130,v200,fine,Gripper\WObj:=wPick;
        PulseDO\High\PLength:=1,DO_TakeBox;
        WaitTime 1;
        
        MoveL Offs(Target_130,0,0,200),v100,fine,Gripper\WObj:=wPick;   
    
	    MoveJ Target_10,v1000,z100,Gripper\WObj:=wPick;
	    MoveJ Target_30,v1000,z100,Gripper\WObj:=wPick;
	    MoveJ Target_40,v1000,z100,Gripper\WObj:=wPick;
	    MoveJ Target_50,v1000,z100,Gripper\WObj:=wPick;
        
        MoveJ Offs(Target_60,0,0,200),v1000,fine,Gripper\WObj:=wPick;
	    MoveL Offs(Target_60,0,0,0),v100,fine,Gripper\WObj:=wPick;
        
        WaitTime 1;
        PulseDO\high\PLength:=1,DO_LeaveBox;
        WaitTime 1;
        MoveL Offs(Target_60,0,0,200),v100,fine,Gripper\WObj:=wPick;
        
        
        MoveJ Target_40,v1000,z100,Gripper\WObj:=wPick;
        
        
        MoveAbsJ pHome,v1000,fine,Gripper\WObj:=wPick;
        
        PulseDO\high\PLength:=1,DO_PickFromConvReady;

        
        
        
	ENDPROC
    
    
	PROC PickLays()
        
        waitDI DI_PickLays,1;
        
        
        MoveAbsJ pHome,v1000,fine,Gripper\WObj:=wPallet;
        
        MoveJ Target_70,v1000,z100,Gripper\WObj:=wPallet;
        
        MoveJ Offs(Target_90,-300,0,300),v1000,fine,Gripper\WObj:=wPallet;
        MoveJ Offs(Target_90,-300,0,0),v1000,fine,Gripper\WObj:=wPallet;
        MoveJ Target_90,v1000,z100,Gripper\WObj:=wPallet;       
        
        WaitTime 1;
        SetDO DO_AttachLays, 1;
        
        MoveJ Offs(Target_90,0,0,600),v1000,fine,Gripper\WObj:=wPallet;
        MoveJ Target_100,v1000,z100,Gripper\WObj:=wPallet;
        
        MoveJ Offs(Target_110,0,0,200),v1000,fine,Gripper\WObj:=wPallet;
        MoveJ Target_110,v1000,fine,Gripper\WObj:=wPallet;
        
        waittime 1;
        SetDO DO_AttachLays, 0;
        
        MoveJ Offs(Target_110,0,-200,0),v1000,fine,Gripper\WObj:=wPallet;
        MoveJ Offs(Target_110,0,-200,200),v1000,fine,Gripper\WObj:=wPallet;
        MoveJ Target_120,v1000,z100,Gripper\WObj:=wPallet;
        MoveAbsJ pHome,v1000,fine,Gripper\WObj:=wPallet;
        
        PulseDO\high\PLength:=1,DO_PickLaysReady;
        
        
        

	ENDPROC
	PROC PlaceLays()

	ENDPROC
	PROC PickCrunch()

	ENDPROC
	PROC PlaceCrunch()

	ENDPROC
ENDMODULE