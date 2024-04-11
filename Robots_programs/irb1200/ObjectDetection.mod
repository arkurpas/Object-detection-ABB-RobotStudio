MODULE ObjectDetection
    
    CONST robtarget Target_180:=[[-131.64297473,-283.621536816,-240.767569601],[0.711267119,-0.00761223,-0.017691812,-0.70265791],[1,0,-2,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_290:=[[-571.733538331,-338.65207396,-197.875161393],[0.372859444,-0.007501473,-0.101338714,-0.922306906],[0,-1,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_320:=[[42.464807415,-175.538984443,1121.374554773],[0.091525412,-0.723436618,0.676024737,-0.106080696],[0,-1,-2,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_340:=[[78.563050851,179.514272967,442.159724124],[0.01965041,0.076548983,-0.996708076,0.01808664],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget Target_350:=[[130.608720088,437.006994744,803.612423382],[0.089535397,0.726690817,-0.676133851,-0.08213942],[0,-1,-2,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_420:=[[88.251186637,233.066154838,1034.530562172],[0.346165446,-0.070056859,0.91682846,0.186244718],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_430:=[[277.782055492,144.77923044,761.754703116],[0.120814114,-0.352398042,0.926787094,-0.047804312],[0,-1,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_440:=[[90.267614139,218.375856223,84.939999213],[-0.000000029,-0.003551746,0.999993693,-0.000000023],[0,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_450:=[[73.327117593,215.606404988,35.206074396],[0.00004357,0.000104746,0.999999812,0.000602143],[-1,0,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_460:=[[-140.639849379,-281.9733899,-71.786640738],[0.000445163,-0.000008741,0.000000014,0.999999901],[1,-1,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    !======================================================

    PERS tooldata tGripper:=[TRUE,[[0,0,0],[1,0,0,0]],[0,[0,0,0],[1,0,0,0],0,0,0]];
    PERS wobjdata wPick:=[FALSE,TRUE,"",[[139.217,422.219,510.331],[0.000008727,-0.000445059,-1,-0.000000004]],[[552,411,0],[1,0,0,0]]];
    PERS wobjdata wCamera:=[FALSE,TRUE,"",[[780.539,-650.858,143.999],[-0.000000004,1,-0.000445059,-0.000008727]],[[552,411,0],[1,0,0,0]]];
    PERS wobjdata wPlace02:=[FALSE,TRUE,"",[[354.212,-438.641,-239.608],[1,-0.000602143,4.357E-5,0.000104746]],[[0,0,0],[1,0,0,0]]];
    PERS wobjdata wPlace03:=[FALSE,TRUE,"",[[354.212,128.132,-239.609],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
    CONST jointtarget pHome:=[[0,-34.207038779,0,0,41.102941176,-91.176470588],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pPick:=[[-311.684212736,-1070.391654567,-390.563066296],[0.000306128,-0.725866082,0.000323053,0.687835905],[-1,-1,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];

    !======================================================
    !Socket communication
    VAR socketdev socket1;
    VAR string received_string;
    VAR string x_string;
    VAR num x_num;
    VAR bool okx;

    VAR string y_string;
    VAR num y_num;
    VAR bool oky;

    VAR num len_received_string;
    VAR num found;

    VAR string schips_type;
    VAR num nchips_type;
    VAR bool oktype;
    !======================================================
    !======================================================
    !Pick variables
    VAR num nToTwoCounter:=0;
    VAR num xOffset_Pick:=-120;
    VAR num yOffset_Pick:=0;
    VAR num zOffset_Pick:=0;
    VAR num nToFourteenCounter:=0;
    
    !======================================================
    !======================================================
    !Lays variable
    VAR num nToFourCounter_Lays:=0;
    VAR num nLayersCounter_Lays:=0;
    VAR num DropPos_lays:=0;
    VAR num xOffs_Lays:=0;
    VAR num yOffs_Lays:=0;
    VAR num zOffs_Lays:=0;
    VAR num nToTwentyCounter_Lays:=0;
    !======================================================
    !======================================================
    !Crunchips variable
    VAR num nToFourCounter_Crunch:=0;
    VAR num nLayersCounter_Crunch:=0;
    VAR num DropPos_Crunch:=0;
    VAR num xOffs_Crunch:=0;
    VAR num yOffs_Crunch:=0;
    VAR num zOffs_Crunch:=0;
    VAR num nToTwentyCounter_Crunch:=0;
    !======================================================

    PROC main()
        PulseDO\high\PLength:=1,DO_Rest_counter;
        WaitTime 1;
        SocketCreate socket1;
        SocketConnect socket1,"127.0.0.1",8000\Time:=WAIT_MAX;
        ! Communication
        
        MoveAbsJ pHome,v1000,fine,tVaccum;
        
        WHILE TRUE DO

            Pick;

            IF nchips_type=1 THEN
                PlaceCrunchips;

            ELSEIF nchips_type=2 THEN
                PlaceLays;

            ENDIF
        ENDWHILE
        
        MoveAbsJ pHome,v1000,fine,tVaccum;

    ENDPROC

    PROC Pick()
        
        IF nToFourteenCounter = 15 THEN
            
            MoveAbsJ pHome,v1000,fine,tVaccum;
            nToFourteenCounter := 0;
            SetDo DO_R2PickFromConv, 1;
            WaitDI DI_WaitForConv,1;
            SetDo DO_R2PickFromConv, 0;
            zOffset_Pick := 0;
                       
        ENDIF
        
        
        
        IF nToTwentyCounter_Lays = 12 THEN
            
            MoveAbsJ pHome,v1000,fine,tVaccum;
            nToTwentyCounter_Lays := 0;
            SetDO DO_R2PickLays, 1;
            WaitDI DI_WaitForLaysReady,1;
            SetDO DO_R2PickLays, 0;  
            
        ENDIF
        
        
        
        IF nToTwentyCounter_Crunch = 12 THEN
            
            MoveAbsJ pHome,v1000,fine,tVaccum;
            nToTwentyCounter_Crunch := 0;
            SetDO DO_R2PickCrunch, 1;
            WaitDI DI_WaitForConv,1;
            SetDO DO_R2PickCrunch, 0;
  
            
        ENDIF


        MoveJ offs(Target_180,nToTwoCounter*xOffset_Pick,0,0),v1000,fine,Camera\WObj:=wPick;

        SocketSend socket1\Str:="send_to_robot";
        SocketReceive socket1\Str:=received_string\Time:=WAIT_MAX;
        SocketSend socket1\Str:="coordinates_recived";

        found:=StrMatch(received_string,1,"-");
        len_received_string:=StrLen(received_string);

        schips_type:=StrPart(received_string,1,1);
        oktype:=StrToVal(schips_type,nchips_type);

        x_string:=StrPart(received_string,2,found-1);
        okX:=StrToVal(x_string,x_num);

        y_string:=StrPart(received_string,found+1,len_received_string-found);
        okX:=StrToVal(x_string,y_num);


        MoveJ offs(Target_460,nToTwoCounter*xOffset_Pick,0,-100),v1000,fine,tVaccum\WObj:=wPick;
        MoveL offs(Target_460,nToTwoCounter*xOffset_Pick,0,zOffset_Pick),v500,fine,tVaccum\WObj:=wPick;
        PulseDO\high\PLength:=1,DO_PICK;
        WaitTime 1;
        MoveL offs(Target_460,nToTwoCounter*xOffset_Pick,0,-100),v500,fine,tVaccum\WObj:=wPick;
        

        nToFourteenCounter := nToFourteenCounter +1;


        IF nToTwoCounter=2 THEN
            zOffset_Pick:=zOffset_Pick+30;
            nToTwoCounter:=0;
        ELSE
            nToTwoCounter:=nToTwoCounter+1;
        ENDIF
        
        

        
        MoveJ Target_290,v1000,z100,tVaccum\WObj:=wPick;
        
        


    ENDPROC

    PROC PlaceLays()

        MoveJ Target_480,v1000,z100,tVaccum\WObj:=wPlace03;

        TEST DropPos_lays

        CASE 0:
            xOffs_Lays:=0;
            yOffs_Lays:=0;
        CASE 1:
            xOffs_Lays:=0;
            yOffs_Lays:=-120;
        CASE 2:
            xOffs_Lays:=143;
            yOffs_Lays:=0;
        CASE 3:
            xOffs_Lays:=143;
            yOffs_Lays:=-120;

        ENDTEST
       
        MoveJ Offs(Target_440,xOffs_Lays,yOffs_Lays,200),v1000,fine,tVaccum\WObj:=wPlace03;
        MoveJ Offs(Target_440,xOffs_Lays,yOffs_Lays,zOffs_Lays),v500,fine,tVaccum\WObj:=wPlace03;

        PulseDO\high\PLength:=1,DO_Drop;
        WaitTime 1;
        
        IF nToTwentyCounter_Lays <= 11 THEN
           SocketSend socket1\Str:="send_to_robot"; 
        ENDIF
        
        MoveJ Offs(Target_440,xOffs_Lays,yOffs_Lays,300),v1000,fine,tVaccum\WObj:=wPlace03;

        nToFourCounter_Lays:=nToFourCounter_Lays+1;
        DropPos_lays:=DropPos_lays+1;


        IF nToFourCounter_Lays=4 THEN
            nToFourCounter_Lays:=0;
            DropPos_lays:=0;
            nLayersCounter_Lays:=nLayersCounter_Lays+1;
            zOffs_Lays:=zOffs_Lays+30;
            IF nLayersCounter_Lays=5 THEN
                zOffs_Lays:=0;
                nLayersCounter_Lays:=0;
                nToFourCounter_Lays:=0;
            ENDIF
        ENDIF
        


        MoveJ Target_340,v1000,z100,tVaccum\WObj:=wPlace03;
        
        
        nToTwentyCounter_Lays := nToTwentyCounter_Lays +1;
        
        
        MoveJ Target_420,v1000,fine,tVaccum\WObj:=wPlace03;
        

        


    ENDPROC

    PROC PlaceCrunchips()


        MoveJ Target_350,v1000,z50,tVaccum\WObj:=wPlace02;
        MoveJ Target_470,v1000,fine,tVaccum\WObj:=wPlace02;
        !MoveJ Target_470,v1000,fine,tVaccum\WObj:=wPlace02;
        
        TEST DropPos_Crunch

        CASE 0:
            xOffs_Crunch:=0;
            yOffs_Crunch:=0;
        CASE 1:
            xOffs_Crunch:=0;
            yOffs_Crunch:=-120;
        CASE 2:
            xOffs_Crunch:=143;
            yOffs_Crunch:=0;
        CASE 3:
            xOffs_Crunch:=143;
            yOffs_Crunch:=-120;

        ENDTEST
        
        
        
        MoveJ Offs(Target_450,xOffs_Crunch,yOffs_Crunch,200),v1000,fine,tVaccum\WObj:=wPlace02;
        MoveJ Offs(Target_450,xOffs_Crunch,yOffs_Crunch,zOffs_Crunch),v500,fine,tVaccum\WObj:=wPlace02;
        
        PulseDO\high\PLength:=1,DO_Drop;
        WaitTime 1;
        MoveJ Offs(Target_450,xOffs_Crunch,yOffs_Crunch,300),v1000,fine,tVaccum\WObj:=wPlace02;

        nToFourCounter_Crunch:=nToFourCounter_Crunch+1;
        DropPos_Crunch:=DropPos_Crunch+1;


        IF nToFourCounter_Crunch=4 THEN
            nToFourCounter_Crunch:=0;
            DropPos_Crunch:=0;
            nLayersCounter_Crunch:=nLayersCounter_Crunch+1;
            zOffs_Crunch:=zOffs_Crunch+30;
            IF nLayersCounter_Crunch=5 THEN
                zOffs_Crunch:=0;
                nLayersCounter_Crunch:=0;
                nToFourCounter_Crunch:=0;
            ENDIF
        ENDIF
        

        MoveJ Target_430,v1000,z100,tVaccum\WObj:=wPlace02;
        
        IF nToTwentyCounter_Crunch <= 11 THEN
           SocketSend socket1\Str:="send_to_robot"; 
        ENDIF

        nToTwentyCounter_Crunch := nToTwentyCounter_Crunch +1;
                
        MoveJ Target_350,v1000,fine,tVaccum\WObj:=wPlace02;
       
    ENDPROC



ENDMODULE