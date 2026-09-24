include <OOEB-working.scad>


module OOEBinsert(item,x=0,y=0,z=0,ex=0,length=0,rotX=0,rotY=0,rotZ=0,width=0,height=0,depth=0,rad=0,color="gray",alpha=1,clearance=0,offset=0){
    color(color,alpha){
            translate([x,y,z]){
                rotate([rotX,rotY,rotZ]){    
                    if(item=="OPSCtest"){
                }
            }
        }
    }
}

module OOEBoiii(type,name,color){
   OOEBoii(type,x=OOEBgvv(str(name,"X")),y=OOEBgvv(str(name,"Y")),z=OOEBgvv(str(name,"Z")),rotX=OOEBgvv(str(name,"RotX")),rotY=OOEBgvv(str(name,"RotY")),rotZ=OOEBgvv(str(name,"RotZ")),color=color); 
}

module OOEBoii(type,name,color="gray",x=0,y=0,z=0,ex=0,length=0,rotX=0,rotY=0,rotZ=0,width=0,height=0,depth=100,rad=0,rad2=0,alpha=1,OOwidth=0,OOheight=0,holes=true,negative=true){
    color(color,alpha){
        translate([x,y,z]){
                rotate([rotX,rotY,rotZ]){
                    if(type=="TEST"){
                        t = 0;
                    }else if(type=="TEST2"){
                        t = 0;
                    }                            
//@@@@@@OOEB-INPU-BUTA-X Asembly                    
                    else if(type=="OOEB-INPU-BUTA-X"){
                        draw_OOEB_INPU_BUTA_X(color);
                    }                            
//@@@@@@OOEB-INPU-POTE-X Asembly                    
                    else if(type=="OOEB-INPU-POTE-X"){
                        draw_OOEB_INPU_POTE_X(color);
                    }                        
//@@@@@@OOEB-OUTP-LEDS-X Asembly                    
                    else if(type=="OOEB-OUTP-LEDS-X"){
                        draw_OOEB_OUTP_LEDS_X(color);
                    }                                            
      //////  OOEB-WI
//@@@@@@OOEB-WIRE-BA Asembly                    
                    else if(type=="OOEB-WIRE-BA"){
                        draw_OOEB_WIRE_BA(color);
                    }        

      //////  OOMP
//@@@@@@BUTA-06-X-STAN-01 Asembly                    
                    else if(type=="OOMP-BUTA-06-X-STAN-01"){
                        draw_OOMP_BUTA_06_X_STAN_01(color);
                    }
//@@@@@@BUTA-12-X-STAN-01 Asembly                    
                    else if(type=="OOMP-BUTA-12-X-STAN-01"){
                        draw_OOMP_BUTA_12_X_STAN_01(color);
                    }
//@@@@@@LEDS-10-X-X-X-01 Asembly                    
                    else if(type=="OOMP-LEDS-10-X-X-01"){
                        draw_OOMP_LEDS_10_X_X_01(color);
                    }      
//@@@@@@POTE-95D-L-X-01-01 Asembly                    
                    else if(type=="OOMP-POTE-95D-L-X-X"){
                        draw_OOMP_POTE_95D_L_X_X(color);
                    }      
//@@@@@@RESE-W04-X-X-X Asembly                    
                    else if(type=="OOMP-RESE-W04-X-X-X"){
                        draw_OOMP_RESE_W04_X_X_X(color);
                    }                        
                    else{    
                        oi(type,x=OOEBgvv(str(name,"X")),y=OOEBgvv(str(name,"Y")),z=OOEBgvv(str(name,"Z")),width=OOEBgvv(str(name,"W")),height=OOEBgvv(str(name,"H")),depth=OOEBgvv(str(name,"D")),rad=OOEBgvv(str(name,"Radius")),rotX=OOEBgvv(str(name,"RotX")),rotY=OOEBgvv(str(name,"RotY")),rotZ=OOEBgvv(str(name,"RotZ")),color=color,name=name);
                    }
                }
        }
    }
}

//////////// OOEB MODULES


      //////////// INPU MODULES

module draw_OOEB_INPU_BUTA_X(color){
    draw_split06(color) draw_OOEB_INPU_BUTA_X_ALL(color);
}

module draw_OOEB_INPU_BUTA_X_ALL(color){
    difference(){
        //postive portion
        union(){            
            draw_OOEB_BASE_MODULE_3X2(color);
        }
        //negative portion
        union(){ 
//////OOEB-INPU-BUTA-X-but06pos oi
            OOEBoiii("OOMP-BUTA-06-X-STAN-01","OOEB-INPU-BUTA-X-but06pos",color);
            OOEBoiii("OOMP-BUTA-12-X-STAN-01","OOEB-INPU-BUTA-X-but12pos",color);
//////OOEB-INPU-BUTA-X-resPos oi
            OOEBoiii("OOMP-RESE-W04-X-X-X","OOEB-INPU-BUTA-X-resPos",color);
        }
    }
}

module draw_OOEB_INPU_POTE_X(color){
    draw_split06(color) draw_OOEB_INPU_POTE_X_ALL(color);
}

module draw_OOEB_INPU_POTE_X_ALL(color){
    difference(){
        //postive portion
        union(){            
            draw_OOEB_BASE_MODULE_3X2(color);
        }
        //negative portion
        union(){ 
            OOEBoiii("OOMP-POTE-95D-L-X-X","OOEB-INPU-POTE-X-potePos",color=color);
        }
    }
}


      //////////// OUTP MODULES

module draw_OOEB_OUTP_LEDS_X(color){
    draw_split06(color) draw_OOEB_OUTP_LEDS_X_ALL(color);
}

module draw_OOEB_OUTP_LEDS_X_ALL(color){
    difference(){
        //postive portion
        union(){
            draw_OOEB_BASE_MODULE_3X2(color);
        }
        //negative portion
        union(){            
//////LED Position
            OOEBoiii("OOMP-LEDS-10-X-X-01","OOEB-OUTP-LED-X-ledPos",color);
//////Resistor Position
            OOEBoiii("OOMP-RESE-W04-X-X-X","OOEB-OUTP-LED-X-resPos",color);
//////ID
            //oi("text",x=-10,y=-10,z=0,ex=str("OUTP-LEDS"),height=2,depth=0.2,color=color);
        }
    }
}



      /////////// BASE MODULE

module draw_OOEB_BASE_MODULE_3X2(color){
    difference(){
        //postive portion
        union(){
            OOEBoii("cubeRounded","OOEB-OUTP-LEDX-X-main",color)    ;
        }
        //negative portion
        union(){            
//////holeA oi
            OOEBoii("holeM6","holeA",color);
            OOEBoii("holeM6","holeB",color);
            //OOEBoii("holeM6","holeC",color);
//////OOEB-OUTP-LED-X-joinHoleA oi
            OOEBoii("holeM3","OOEB-OUTP-LED-X-joinHoleA",color);            
            OOEBoii("nutM3","OOEB-OUTP-LED-X-joinHoleA",color);
            OOEBoii("countersunkM3","OOEB-OUTP-LED-X-joinHoleCounterA",color);
//////OOEB-OUTP-LED-X-joinHoleB oi            
            OOEBoii("holeM3","OOEB-OUTP-LED-X-joinHoleB",color);
            OOEBoii("nutM3","OOEB-OUTP-LED-X-joinHoleB",color); 
            OOEBoii("countersunkM3","OOEB-OUTP-LED-X-joinHoleCounterB",color);           
//////Connector Cutout
            OOEBoiii("OOEB-WIRE-BA","OOEB-OUTPLED-X-wire",color);
//////OOEB-OUTPLED-X-clearanceHole oi
            OOEBoii("cubeRounded","OOEB-OUTPLED-X-clearanceHole",color);
//////ID
            //oi("text",x=-10,y=-10,z=0,ex=str("OUTP-LEDS"),height=2,depth=0.2,color=color);
        }
    }



}


module draw_split06(color){
    split = 6;
    //top
    if(o=="3DPR"){    
            translate([0,0,-split-6]){
                rotate([180,0,0]){
                intersection(){
                    oi("plane",depth=split,z=0);
                    children();
                    //draw_OOEB_OUTP_LEDS_X_ALL(color);
                }
            }
        }
        //bottom
        
            translate([45,0,0]){
                intersection(){
                    oi("plane",depth=12-split,z=-split);
                    children();
                    //draw_OOEB_OUTP_LEDS_X_ALL(color);
                }
            }
    }else if(o=="LAZE"){
            drawLaser(start=-0.2,layers=4, tileDif=45) children();
    }else{
       children() ;
    }
    
    
}



////////////  OOEB WIRE MODULES

module draw_OOEB_WIRE_BA(color){
    difference(){                    
    //postive portion                        
        union(){             
//////OOEB-WIRE-BA-frontBox oi
    OOEBoii("cube","OOEB-WIRE-BA-frontBox",color);
//////OOEB-WIRE-BA-backBox oi
    OOEBoii("cube","OOEB-WIRE-BA-backBox",color); 
//////OOEB-WIRE-BA-wireBox oi
    OOEBoii("cubeRounded","OOEB-WIRE-BA-wireBox",color);      
//////OOEB-WIRE-BA-key oi
    OOEBoii("cube","OOEB-WIRE-BA-key",color);
//////OOEB-WI-BA-dot oi
    OOEBoii("cylinder","OOEB-WI-BA-dot",color);                                
        }                            
    //negative portion                            
        union(){                            
        }                            
    }                            
}

            //////////// OOMP Modules

module draw_OOMP_BUTA_06_X_STAN_01(color){
    difference(){
        //postive portion
        union(){
//////OOMP-BUTA-06-X-STAN-01-underClearance oi
            OOEBoii("cubeRounded","OOMP-BUTA-06-X-STAN-01-underClearance",color);            
//////OOMP-BUTA-06-X-STAN-01-legA oi
            OOEBoii("cube","OOMP-BUTA-06-X-STAN-01-legA",color);            
            OOEBoii("cube","OOMP-BUTA-06-X-STAN-01-legB",color);            
            OOEBoii("cube","OOMP-BUTA-06-X-STAN-01-legC",color);            
            OOEBoii("cube","OOMP-BUTA-06-X-STAN-01-legD",color);            
        }
        //negative portion
        union(){
        }
    }
}

module draw_OOMP_BUTA_12_X_STAN_01(color){
    difference(){
        //postive portion
        union(){
//////OOMP-BUTA-06-X-STAN-01-underClearance oi
            OOEBoii("cubeRounded","OOMP-BUTA-12-X-STAN-01-underClearance",color);            
//////OOMP-BUTA-06-X-STAN-01-legA oi
            OOEBoii("cube","OOMP-BUTA-12-X-STAN-01-legA",color);            
            OOEBoii("cube","OOMP-BUTA-12-X-STAN-01-legB",color);            
            OOEBoii("cube","OOMP-BUTA-12-X-STAN-01-legC",color);            
            OOEBoii("cube","OOMP-BUTA-12-X-STAN-01-legD",color);            
        }
        //negative portion
        union(){
        }
    }
}

module draw_OOMP_LEDS_10_X_X_01(color){            
    difference(){                    
        //postive portion                        
        union(){                     
//////OOMP-LEDS-10-X-X-X-legA oi
            OOEBoii("cube","OOMP-LEDS-10-X-X-X-legA",color); 
            OOEBoii("cube","OOMP-LEDS-10-X-X-X-legB",color);     
            //oi("text",ex=str("+"),x=OOEBgvv("OOMP-LEDS-10-X-X-X-legAX"),y=2,depth=0.2,height=3,color=color);    
            //oi("cube",x=OOEBgvv("OOMP-LEDS-10-X-X-X-legAX"),y=-3,width=0.5,height=3,depth=0.2,color=color);          
            //oi("cube",x=-OOEBgvv("OOMP-LEDS-10-X-X-X-legAX"),y=-2.25,width=0.5,height=1.5,depth=0.2,color=color);          
        }                            
        //negative portion                            
        union(){                            
        }                            
    }              
}


module draw_OOMP_POTE_95D_L_X_X(color){          ;
    difference(){                    
        //postive portion                        
        union(){                     
            
            OOEBoii("cube","OOMP-POTE-95D-L-X-X-main",color);
//////OOMP-POTE-95D-L-X-X-legA oi
            OOEBoii("cube","OOMP-POTE-95D-L-X-X-legA",color);
            OOEBoii("cube","OOMP-POTE-95D-L-X-X-legB",color);
            OOEBoii("cube","OOMP-POTE-95D-L-X-X-legC",color);
        }                            
        //negative portion                            
        union(){                            
        }                            
    }              
}

module draw_OOMP_RESE_W04_X_X_X(color){            
    difference(){                    
        //postive portion                        
        union(){                     
//////OOMP-RESE-W04-X-X-X-legA oi
            OOEBoii("cube","OOMP-RESE-W04-X-X-X-legA",color);
            OOEBoii("cube","OOMP-RESE-W04-X-X-X-legB",color);
        }                            
        //negative portion                            
        union(){                            
        }                            
    }              
}


function OOEBgvv(name) =
name=="TEST" ? "TEST":

      ////////////OOEB-INPU-BUTA   
//////OOEB-INPU-BUTA-X-but06pos dimensions'
name=="OOEB-INPU-BUTA-X-but06posW"      ? 0 :
name=="OOEB-INPU-BUTA-X-but06posH"      ? 0 :
name=="OOEB-INPU-BUTA-X-but06posD"      ? 0 :
name=="OOEB-INPU-BUTA-X-but06posX"      ? 0 :
name=="OOEB-INPU-BUTA-X-but06posY"      ? -5 :
name=="OOEB-INPU-BUTA-X-but06posZ"      ? 0 :
name=="OOEB-INPU-BUTA-X-but06posRadius"     ? 2 :name=="OOEB-INPU-BUTA-X-but06posRotX"       ? 0 :
name=="OOEB-INPU-BUTA-X-but06posRotY"       ? 0 :
name=="OOEB-INPU-BUTA-X-but06posRotZ"       ? 0 :  
//////OOEB-INPU-BUTA-X-but12pos dimensions'
name=="OOEB-INPU-BUTA-X-but12posW"      ? OOEBgvv("OOEB-INPU-BUTA-X-but06posW") :
name=="OOEB-INPU-BUTA-X-but12posH"      ? OOEBgvv("OOEB-INPU-BUTA-X-but06posH") :
name=="OOEB-INPU-BUTA-X-but12posD"      ? OOEBgvv("OOEB-INPU-BUTA-X-but06posD") :
name=="OOEB-INPU-BUTA-X-but12posX"      ? OOEBgvv("OOEB-INPU-BUTA-X-but06posX") :
name=="OOEB-INPU-BUTA-X-but12posY"      ? OOEBgvv("OOEB-INPU-BUTA-X-but06posY") :
name=="OOEB-INPU-BUTA-X-but12posZ"      ? OOEBgvv("OOEB-INPU-BUTA-X-but06posZ") :
name=="OOEB-INPU-BUTA-X-but12posRadius"     ? OOEBgvv("OOEB-INPU-BUTA-X-but06posRadius") :
name=="OOEB-INPU-BUTA-X-but12posRotX"       ? OOEBgvv("OOEB-INPU-BUTA-X-but06posRotX") :
name=="OOEB-INPU-BUTA-X-but12posRotY"       ? OOEBgvv("OOEB-INPU-BUTA-X-but06posRotY") :
name=="OOEB-INPU-BUTA-X-but12posRotZ"       ? OOEBgvv("OOEB-INPU-BUTA-X-but06posRotZ") :
//////OOEB-INPU-BUTA-X-resPos dimensions'
name=="OOEB-INPU-BUTA-X-resPosW"        ? 0 :
name=="OOEB-INPU-BUTA-X-resPosH"        ? 0 :
name=="OOEB-INPU-BUTA-X-resPosD"        ? 0 :
name=="OOEB-INPU-BUTA-X-resPosX"        ? -10 :
name=="OOEB-INPU-BUTA-X-resPosY"        ? -5 :
name=="OOEB-INPU-BUTA-X-resPosZ"        ? 0 :
name=="OOEB-INPU-BUTA-X-resPosRadius"       ? 0 :
name=="OOEB-INPU-BUTA-X-resPosRotX"     ? 0 :
name=="OOEB-INPU-BUTA-X-resPosRotY"     ? 0 :
name=="OOEB-INPU-BUTA-X-resPosRotZ"     ? 90 :
      ////////////  OOEB-INPU-POTE-X
//////OOEB-INPU-POTE-X-potePos dimensions'      
name=="OOEB-INPU-POTE-X-potePosW"       ? 0 :
name=="OOEB-INPU-POTE-X-potePosH"       ? 0 :
name=="OOEB-INPU-POTE-X-potePosD"       ? 0 :
name=="OOEB-INPU-POTE-X-potePosX"       ? 0 :
name=="OOEB-INPU-POTE-X-potePosY"       ? -5 :
name=="OOEB-INPU-POTE-X-potePosZ"       ? 0 :
name=="OOEB-INPU-POTE-X-potePosRadius"      ? 0 :
name=="OOEB-INPU-POTE-X-potePosRotX"        ? 0 :
name=="OOEB-INPU-POTE-X-potePosRotY"        ? 0 :
name=="OOEB-INPU-POTE-X-potePosRotZ"        ? -90 :
      ////////////OOEB-OUTP-LED
//////OOEB-OUTP-LEDX-X-main dimensions'
name=="OOEB-OUTP-LEDX-X-mainW"      ? 15 * 3 - 3 :
name=="OOEB-OUTP-LEDX-X-mainH"      ? 15 * 2 - 3 :
name=="OOEB-OUTP-LEDX-X-mainD"      ? 12 :
name=="OOEB-OUTP-LEDX-X-mainX"      ? 0 :
name=="OOEB-OUTP-LEDX-X-mainY"      ? 0 :
name=="OOEB-OUTP-LEDX-X-mainZ"      ? 0 :
name=="OOEB-OUTP-LEDX-X-mainRadius"     ? 5 :
name=="OOEB-OUTP-LEDX-X-mainRotX"       ? 0 :
name=="OOEB-OUTP-LEDX-X-mainRotY"       ? 0 :
name=="OOEB-OUTP-LEDX-X-mainRotZ"       ? 0 :
//////OOEB-OUTPLED-X-wire dimensions'
name=="OOEB-OUTPLED-X-wireW"        ? 0 :
name=="OOEB-OUTPLED-X-wireH"        ? 0 :
name=="OOEB-OUTPLED-X-wireD"        ? 0 :
name=="OOEB-OUTPLED-X-wireX"        ? -OOEBgvv("OOEB-OUTP-LEDX-X-mainW")/2 :
name=="OOEB-OUTPLED-X-wireY"        ? -3 :
name=="OOEB-OUTPLED-X-wireZ"        ? -OOEBgvv("OOEB-OUTP-LEDX-X-mainD") + 6 :
name=="OOEB-OUTPLED-X-wireRadius"       ? 0 :
name=="OOEB-OUTPLED-X-wireRotX"     ? 0 :
name=="OOEB-OUTPLED-X-wireRotY"     ? 0 :
name=="OOEB-OUTPLED-X-wireRotZ"     ? 180 :
//////OOEB-OUTPLED-X-clearanceHole dimensions'
name=="OOEB-OUTPLED-X-clearanceHoleW"       ? 24 :
name=="OOEB-OUTPLED-X-clearanceHoleH"       ? 13 :
name=="OOEB-OUTPLED-X-clearanceHoleD"       ? 3 :
name=="OOEB-OUTPLED-X-clearanceHoleX"       ? -1 :
name=="OOEB-OUTPLED-X-clearanceHoleY"       ? -4.0 :
name=="OOEB-OUTPLED-X-clearanceHoleZ"       ? -OOEBgvv("OOEB-OUTP-LEDX-X-mainD") + 9 :
name=="OOEB-OUTPLED-X-clearanceHoleRadius"      ? 2 :
name=="OOEB-OUTPLED-X-clearanceHoleRotX"        ? 0 :
name=="OOEB-OUTPLED-X-clearanceHoleRotY"        ? 0 :
name=="OOEB-OUTPLED-X-clearanceHoleRotZ"        ? 0 :
//////OOEB-OUTP-LED-X-ledPos dimensions'
name=="OOEB-OUTP-LED-X-ledPosW"     ? 0 :
name=="OOEB-OUTP-LED-X-ledPosH"     ? 0 :
name=="OOEB-OUTP-LED-X-ledPosD"     ? 0 :
name=="OOEB-OUTP-LED-X-ledPosX"     ? 0 :
name=="OOEB-OUTP-LED-X-ledPosY"     ? -5 :
name=="OOEB-OUTP-LED-X-ledPosZ"     ? 0 :
name=="OOEB-OUTP-LED-X-ledPosRadius"        ? 0 :
name=="OOEB-OUTP-LED-X-ledPosRotX"      ? 0 :
name=="OOEB-OUTP-LED-X-ledPosRotY"      ? 0 :
name=="OOEB-OUTP-LED-X-ledPosRotZ"      ? 45 :
//////OOEB-OUTP-LED-X-resPos dimensions'
name=="OOEB-OUTP-LED-X-resPosW"     ? 0 :
name=="OOEB-OUTP-LED-X-resPosH"     ? 0 :
name=="OOEB-OUTP-LED-X-resPosD"     ? 0 :
name=="OOEB-OUTP-LED-X-resPosX"     ? -9 :
name=="OOEB-OUTP-LED-X-resPosY"     ? -5 :
name=="OOEB-OUTP-LED-X-resPosZ"     ? 0 :
name=="OOEB-OUTP-LED-X-resPosRadius"        ? 0 :
name=="OOEB-OUTP-LED-X-resPosRotX"      ? 0 :
name=="OOEB-OUTP-LED-X-resPosRotY"      ? 0 :
name=="OOEB-OUTP-LED-X-resPosRotZ"      ? -90 :
//////OOEB-OUTP-LED-X-joinHoleA dimensions'
name=="OOEB-OUTP-LED-X-joinHoleAW"      ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleAH"      ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleAD"      ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleAX"      ? -15 :
name=="OOEB-OUTP-LED-X-joinHoleAY"      ? 7.5 :
name=="OOEB-OUTP-LED-X-joinHoleAZ"      ? -OOEBgvv("OOEB-OUTP-LEDX-X-mainD")  + gv("NUT-M3-DEPTH"):
name=="OOEB-OUTP-LED-X-joinHoleARadius"     ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleARotX"       ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleARotY"       ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleARotZ"       ? 0 :
//////OOEB-OUTP-LED-X-joinHoleB dimensions'
name=="OOEB-OUTP-LED-X-joinHoleBW"      ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAW") :
name=="OOEB-OUTP-LED-X-joinHoleBH"      ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAH") :
name=="OOEB-OUTP-LED-X-joinHoleBD"      ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAD") :
name=="OOEB-OUTP-LED-X-joinHoleBX"      ? 15 :
name=="OOEB-OUTP-LED-X-joinHoleBY"      ? -7.5 :
name=="OOEB-OUTP-LED-X-joinHoleBZ"      ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAZ") :
name=="OOEB-OUTP-LED-X-joinHoleBRadius"     ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARadius") :
name=="OOEB-OUTP-LED-X-joinHoleBRotX"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARotX") :
name=="OOEB-OUTP-LED-X-joinHoleBRotY"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARotY") :
name=="OOEB-OUTP-LED-X-joinHoleBRotZ"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARotZ") :
//////OOEB-OUTP-LED-X-joinHoleCounterA dimensions'
name=="OOEB-OUTP-LED-X-joinHoleCounterAW"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAW") :
name=="OOEB-OUTP-LED-X-joinHoleCounterAH"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAH") :
name=="OOEB-OUTP-LED-X-joinHoleCounterAD"       ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleCounterAX"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAX") :
name=="OOEB-OUTP-LED-X-joinHoleCounterAY"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleAY") :
name=="OOEB-OUTP-LED-X-joinHoleCounterAZ"       ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleCounterARadius"      ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARadius") :
name=="OOEB-OUTP-LED-X-joinHoleCounterARotX"        ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARotX") :
name=="OOEB-OUTP-LED-X-joinHoleCounterARotY"        ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARotY") :
name=="OOEB-OUTP-LED-X-joinHoleCounterARotZ"        ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleARotZ") :
//////OOEB-OUTP-LED-X-joinHoleCounterB dimensions'
name=="OOEB-OUTP-LED-X-joinHoleCounterBW"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBW") :
name=="OOEB-OUTP-LED-X-joinHoleCounterBH"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBH") :
name=="OOEB-OUTP-LED-X-joinHoleCounterBD"       ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleCounterBX"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBX") :
name=="OOEB-OUTP-LED-X-joinHoleCounterBY"       ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBY") :
name=="OOEB-OUTP-LED-X-joinHoleCounterBZ"       ? 0 :
name=="OOEB-OUTP-LED-X-joinHoleCounterBRadius"      ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBRadius") :
name=="OOEB-OUTP-LED-X-joinHoleCounterBRotX"        ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBRotX") :
name=="OOEB-OUTP-LED-X-joinHoleCounterBRotY"        ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBRotY") :
name=="OOEB-OUTP-LED-X-joinHoleCounterBRotZ"        ? OOEBgvv("OOEB-OUTP-LED-X-joinHoleBRotZ") :
//////holeA dimensions'
name=="holeAW"      ? 0 :
name=="holeAH"      ? 0 :
name=="holeAD"      ? 0 :
name=="holeAX"      ? 15 :
name=="holeAY"      ? 15/2 :
name=="holeAZ"      ? 0 :
name=="holeARadius"     ? 0 :
name=="holeARotX"       ? 0 :
name=="holeARotY"       ? 0 :
name=="holeARotZ"       ? 0 :
//////holeB dimensions'
name=="holeBW"      ? 0 :
name=="holeBH"      ? 0 :
name=="holeBD"      ? 0 :
name=="holeBX"      ? OOEBgvv("holeAX") - 15 :
name=="holeBY"      ? OOEBgvv("holeAY") :
name=="holeBZ"      ? 0 :
name=="holeBRadius"     ? 0 :
name=="holeBRotX"       ? 0 :
name=="holeBRotY"       ? 0 :
name=="holeBRotZ"       ? 0 :
//////holeC dimensions'
name=="holeCW"      ? 0 :
name=="holeCH"      ? 0 :
name=="holeCD"      ? 0 :
name=="holeCX"      ? OOEBgvv("holeBX") - 15:
name=="holeCY"      ? OOEBgvv("holeAY") :
name=="holeCZ"      ? 0 :
name=="holeCRadius"     ? 0 :
name=="holeCRotX"       ? 0 :
name=="holeCRotY"       ? 0 :
name=="holeCRotZ"       ? 0 :
    ////////////OOEB-WIRE
        ////////////OOEB-WIRE-BA
//////OOEB-WIRE-extra variable
    name=="OOEB-WIRE-extra"     ? 0.5 :        
//////OOEB-WIRE-BA-frontBox dimensions'        
name=="OOEB-WIRE-BA-frontBoxW"      ? 8.73 + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-frontBoxH"      ? 10.16 + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-frontBoxD"      ? 3 :
name=="OOEB-WIRE-BA-frontBoxX"      ? -1.615 :
name=="OOEB-WIRE-BA-frontBoxY"      ? 0 :
name=="OOEB-WIRE-BA-frontBoxZ"      ? 0 :
name=="OOEB-WIRE-BA-frontBoxRadius"     ? 0 :
name=="OOEB-WIRE-BA-frontBoxRotX"       ? 0 :
name=="OOEB-WIRE-BA-frontBoxRotY"       ? 0 :
name=="OOEB-WIRE-BA-frontBoxRotZ"       ? 0 :
//////OOEB-WIRE-BA-backBox dimensions'
name=="OOEB-WIRE-BA-backBoxW"       ? 14  + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-backBoxH"       ? 7.62  + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-backBoxD"       ? OOEBgvv("OOEB-WIRE-BA-frontBoxD") :
name=="OOEB-WIRE-BA-backBoxX"       ? -15.52 :
name=="OOEB-WIRE-BA-backBoxY"       ? 1.27 :
name=="OOEB-WIRE-BA-backBoxZ"       ? 0 :
name=="OOEB-WIRE-BA-backBoxRadius"      ? 0 :
name=="OOEB-WIRE-BA-backBoxRotX"        ? 0 :
name=="OOEB-WIRE-BA-backBoxRotY"        ? 0 :
name=="OOEB-WIRE-BA-backBoxRotZ"        ? 0 :
//////OOEB-WIRE-BA-wireBox dimensions'
name=="OOEB-WIRE-BA-wireBoxW"       ? 9.23  + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-wireBoxH"       ? 5.62  + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-wireBoxD"       ? OOEBgvv("OOEB-WIRE-BA-frontBoxD") :
name=="OOEB-WIRE-BA-wireBoxX"       ? -25.135 :
name=="OOEB-WIRE-BA-wireBoxY"       ? 1.27 :
name=="OOEB-WIRE-BA-wireBoxZ"       ? 0 :
name=="OOEB-WIRE-BA-wireBoxRadius"      ? 2 :
name=="OOEB-WIRE-BA-wireBoxRotX"        ? 0 :
name=="OOEB-WIRE-BA-wireBoxRotY"        ? 0 :
name=="OOEB-WIRE-BA-wireBoxRotZ"        ? 0 :
//////OOEB-WIRE-BA-key dimensions'
name=="OOEB-WIRE-BA-keyW"       ? 2.54 + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-keyH"       ? 15.24 + OOEBgvv("OOEB-WIRE-extra") :
name=="OOEB-WIRE-BA-keyD"       ? OOEBgvv("OOEB-WIRE-BA-frontBoxD") :
name=="OOEB-WIRE-BA-keyX"       ? -7.25 :
name=="OOEB-WIRE-BA-keyY"       ? 0 :
name=="OOEB-WIRE-BA-keyZ"       ? 0 :
name=="OOEB-WIRE-BA-keyRadius"      ? 0 :
name=="OOEB-WIRE-BA-keyRotX"        ? 0 :
name=="OOEB-WIRE-BA-keyRotY"        ? 0 :
name=="OOEB-WIRE-BA-keyRotZ"        ? 0 :
//////OOEB-WI-BA-dot dimensions'
name=="OOEB-WI-BA-dotW"     ? 0 :
name=="OOEB-WI-BA-dotH"     ? 0 :
name=="OOEB-WI-BA-dotD"     ? OOEBgvv("OOEB-WIRE-BA-frontBoxD") :
name=="OOEB-WI-BA-dotX"     ? 0 :
name=="OOEB-WI-BA-dotY"     ? -10 :
name=="OOEB-WI-BA-dotZ"     ? 0 :
name=="OOEB-WI-BA-dotRadius"        ? 1.5 :
name=="OOEB-WI-BA-dotRotX"      ? 0 :
name=="OOEB-WI-BA-dotRotY"      ? 0 :
name=="OOEB-WI-BA-dotRotZ"      ? 0 :
            //////////// OOMP 
//////OOMP-pinClearance variable
    name=="OOMP-pinClearance"       ? 0.8 :            
      ////// OOMP-BUTA-06-X-STAN-01
//////OOMP-BUTA-06-X-STAN-01-underClearance dimensions'       
name=="OOMP-BUTA-06-X-STAN-01-underClearanceW"      ? 10 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceH"      ? 10 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceD"      ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAD") -1.6 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceX"      ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceY"      ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceZ"      ? -1.6 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceRadius"     ? 2 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceRotX"       ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceRotY"       ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-underClearanceRotZ"       ? 0 :
//////OOMP-BUTA-06-X-STAN-01-legA dimensions'                 
name=="OOMP-BUTA-06-X-STAN-01-legAW"        ? 0.8 +  OOEBgvv("OOMP-LEDS-clearance") :
name=="OOMP-BUTA-06-X-STAN-01-legAH"        ? 1.4 +  OOEBgvv("OOMP-LEDS-clearance")  :
name=="OOMP-BUTA-06-X-STAN-01-legAD"        ? 5 :
name=="OOMP-BUTA-06-X-STAN-01-legAX"        ? -3.25 :
name=="OOMP-BUTA-06-X-STAN-01-legAY"        ? 2.5 :
name=="OOMP-BUTA-06-X-STAN-01-legAZ"        ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-legARadius"       ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-legARotX"     ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-legARotY"     ? 0 :
name=="OOMP-BUTA-06-X-STAN-01-legARotZ"     ? 0 :
//////OOMP-BUTA-06-X-STAN-01-legB dimensions'
name=="OOMP-BUTA-06-X-STAN-01-legBW"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAW") :
name=="OOMP-BUTA-06-X-STAN-01-legBH"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAH") :
name=="OOMP-BUTA-06-X-STAN-01-legBD"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAD") :
name=="OOMP-BUTA-06-X-STAN-01-legBX"        ? -OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAX") :
name=="OOMP-BUTA-06-X-STAN-01-legBY"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAY") :
name=="OOMP-BUTA-06-X-STAN-01-legBZ"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAZ") :
name=="OOMP-BUTA-06-X-STAN-01-legBRadius"       ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARadius") :
name=="OOMP-BUTA-06-X-STAN-01-legBRotX"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotX") :
name=="OOMP-BUTA-06-X-STAN-01-legBRotY"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotY") :
name=="OOMP-BUTA-06-X-STAN-01-legBRotZ"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotZ") :
//////OOMP-BUTA-06-X-STAN-01-legC dimensions'
name=="OOMP-BUTA-06-X-STAN-01-legCW"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAW") :
name=="OOMP-BUTA-06-X-STAN-01-legCH"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAH") :
name=="OOMP-BUTA-06-X-STAN-01-legCD"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAD") :
name=="OOMP-BUTA-06-X-STAN-01-legCX"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAX") :
name=="OOMP-BUTA-06-X-STAN-01-legCY"        ? -OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAY") :
name=="OOMP-BUTA-06-X-STAN-01-legCZ"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAZ") :
name=="OOMP-BUTA-06-X-STAN-01-legCRadius"       ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARadius") :
name=="OOMP-BUTA-06-X-STAN-01-legCRotX"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotX") :
name=="OOMP-BUTA-06-X-STAN-01-legCRotY"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotY") :
name=="OOMP-BUTA-06-X-STAN-01-legCRotZ"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotZ") :
//////OOMP-BUTA-06-X-STAN-01-legD dimensions'
name=="OOMP-BUTA-06-X-STAN-01-legDW"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAW") :
name=="OOMP-BUTA-06-X-STAN-01-legDH"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAH") :
name=="OOMP-BUTA-06-X-STAN-01-legDD"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAD") :
name=="OOMP-BUTA-06-X-STAN-01-legDX"        ? -OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAX") :
name=="OOMP-BUTA-06-X-STAN-01-legDY"        ? -OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAY") :
name=="OOMP-BUTA-06-X-STAN-01-legDZ"        ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAZ") :
name=="OOMP-BUTA-06-X-STAN-01-legDRadius"       ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARadius") :
name=="OOMP-BUTA-06-X-STAN-01-legDRotX"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotX") :
name=="OOMP-BUTA-06-X-STAN-01-legDRotY"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotY") :
name=="OOMP-BUTA-06-X-STAN-01-legDRotZ"     ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legARotZ") :
      ////// OOMP-BUTA-12-X-STAN-01
//////OOMP-BUTA-12-X-STAN-01-underClearance dimensions'       
name=="OOMP-BUTA-12-X-STAN-01-underClearanceW"      ? 18 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceH"      ? 10 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceD"      ? OOEBgvv("OOMP-BUTA-06-X-STAN-01-legAD") -1.6 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceX"      ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceY"      ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceZ"      ? -1.6 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceRadius"     ? 2 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceRotX"       ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceRotY"       ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-underClearanceRotZ"       ? 0 :
//////OOMP-BUTA-12-X-STAN-01-legA dimensions'                 
name=="OOMP-BUTA-12-X-STAN-01-legAW"        ? 0.8 +  OOEBgvv("OOMP-LEDS-clearance") :
name=="OOMP-BUTA-12-X-STAN-01-legAH"        ? 1.4 +  OOEBgvv("OOMP-LEDS-clearance")  :
name=="OOMP-BUTA-12-X-STAN-01-legAD"        ? 5 :
name=="OOMP-BUTA-12-X-STAN-01-legAX"        ? -6.75 :
name=="OOMP-BUTA-12-X-STAN-01-legAY"        ? 2.5 :
name=="OOMP-BUTA-12-X-STAN-01-legAZ"        ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-legARadius"       ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-legARotX"     ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-legARotY"     ? 0 :
name=="OOMP-BUTA-12-X-STAN-01-legARotZ"     ? 0 :
//////OOMP-BUTA-12-X-STAN-01-legB dimensions'
name=="OOMP-BUTA-12-X-STAN-01-legBW"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAW") :
name=="OOMP-BUTA-12-X-STAN-01-legBH"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAH") :
name=="OOMP-BUTA-12-X-STAN-01-legBD"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAD") :
name=="OOMP-BUTA-12-X-STAN-01-legBX"        ? -OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAX") :
name=="OOMP-BUTA-12-X-STAN-01-legBY"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAY") :
name=="OOMP-BUTA-12-X-STAN-01-legBZ"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAZ") :
name=="OOMP-BUTA-12-X-STAN-01-legBRadius"       ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARadius") :
name=="OOMP-BUTA-12-X-STAN-01-legBRotX"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotX") :
name=="OOMP-BUTA-12-X-STAN-01-legBRotY"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotY") :
name=="OOMP-BUTA-12-X-STAN-01-legBRotZ"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotZ") :
//////OOMP-BUTA-12-X-STAN-01-legC dimensions'
name=="OOMP-BUTA-12-X-STAN-01-legCW"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAW") :
name=="OOMP-BUTA-12-X-STAN-01-legCH"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAH") :
name=="OOMP-BUTA-12-X-STAN-01-legCD"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAD") :
name=="OOMP-BUTA-12-X-STAN-01-legCX"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAX") :
name=="OOMP-BUTA-12-X-STAN-01-legCY"        ? -OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAY") :
name=="OOMP-BUTA-12-X-STAN-01-legCZ"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAZ") :
name=="OOMP-BUTA-12-X-STAN-01-legCRadius"       ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARadius") :
name=="OOMP-BUTA-12-X-STAN-01-legCRotX"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotX") :
name=="OOMP-BUTA-12-X-STAN-01-legCRotY"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotY") :
name=="OOMP-BUTA-12-X-STAN-01-legCRotZ"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotZ") :
//////OOMP-BUTA-12-X-STAN-01-legD dimensions'
name=="OOMP-BUTA-12-X-STAN-01-legDW"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAW") :
name=="OOMP-BUTA-12-X-STAN-01-legDH"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAH") :
name=="OOMP-BUTA-12-X-STAN-01-legDD"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAD") :
name=="OOMP-BUTA-12-X-STAN-01-legDX"        ? -OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAX") :
name=="OOMP-BUTA-12-X-STAN-01-legDY"        ? -OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAY") :
name=="OOMP-BUTA-12-X-STAN-01-legDZ"        ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legAZ") :
name=="OOMP-BUTA-12-X-STAN-01-legDRadius"       ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARadius") :
name=="OOMP-BUTA-12-X-STAN-01-legDRotX"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotX") :
name=="OOMP-BUTA-12-X-STAN-01-legDRotY"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotY") :
name=="OOMP-BUTA-12-X-STAN-01-legDRotZ"     ? OOEBgvv("OOMP-BUTA-12-X-STAN-01-legARotZ") :

      //////OOMP-LEDS-10-X-X-X
//////OMP-LEDS-clearance variable
name=="OOMP-LEDS-clearance"      ? OOEBgvv("OOMP-pinClearance") :   
//////OOMP-leadWidthDefault variable
    name=="OOMP-leadWidthDefault"       ? 0.6 :   
//////OOMP-LEDS-10-X-X-X-legA dimensions'
name=="OOMP-LEDS-10-X-X-X-legAW"        ? OOEBgvv("OOMP-leadWidthDefault") + OOEBgvv("OOMP-LEDS-clearance") :
name=="OOMP-LEDS-10-X-X-X-legAH"        ? OOEBgvv("OOMP-LEDS-10-X-X-X-legAW") :
name=="OOMP-LEDS-10-X-X-X-legAD"        ? 5 :
name=="OOMP-LEDS-10-X-X-X-legAX"        ? 1.27 :
name=="OOMP-LEDS-10-X-X-X-legAY"        ? 0 :
name=="OOMP-LEDS-10-X-X-X-legAZ"        ? 0 :
name=="OOMP-LEDS-10-X-X-X-legARadius"       ? 0 :
name=="OOMP-LEDS-10-X-X-X-legARotX"     ? 0 :
name=="OOMP-LEDS-10-X-X-X-legARotY"     ? 0 :
name=="OOMP-LEDS-10-X-X-X-legARotZ"     ? 0 :
//////OOMP-LEDS-10-X-X-X-legB dimensions'
name=="OOMP-LEDS-10-X-X-X-legBW"        ? OOEBgvv("OOMP-LEDS-10-X-X-X-legAW") :
name=="OOMP-LEDS-10-X-X-X-legBH"        ? OOEBgvv("OOMP-LEDS-10-X-X-X-legAH") :
name=="OOMP-LEDS-10-X-X-X-legBD"        ? OOEBgvv("OOMP-LEDS-10-X-X-X-legAD") :
name=="OOMP-LEDS-10-X-X-X-legBX"        ? -OOEBgvv("OOMP-LEDS-10-X-X-X-legAX") :
name=="OOMP-LEDS-10-X-X-X-legBY"        ? OOEBgvv("OOMP-LEDS-10-X-X-X-legAY") :
name=="OOMP-LEDS-10-X-X-X-legBZ"        ? OOEBgvv("OOMP-LEDS-10-X-X-X-legAZ") :
name=="OOMP-LEDS-10-X-X-X-legBRadius"       ? OOEBgvv("OOMP-LEDS-10-X-X-X-legARadius") :
name=="OOMP-LEDS-10-X-X-X-legBRotX"     ? OOEBgvv("OOMP-LEDS-10-X-X-X-legARotX") :
name=="OOMP-LEDS-10-X-X-X-legBRotY"     ? OOEBgvv("OOMP-LEDS-10-X-X-X-legARotY") :
name=="OOMP-LEDS-10-X-X-X-legBRotZ"     ? OOEBgvv("OOMP-LEDS-10-X-X-X-legARotZ") :
      ////// OOMPE-POTE-10-X-O103-01
//////OOMP-POTE-95D-L-X-X-extra variable
    name=="OOMP-POTE-95D-L-X-X-extra"       ? 1 :      
//////OOMP-POTE-95D-L-X-01-main dimensions'      
name=="OOMP-POTE-95D-L-X-X-mainW"      ? 9.5 + OOEBgvv("OOMP-POTE-95D-L-X-X-extra") :
name=="OOMP-POTE-95D-L-X-X-mainH"      ? 9.5 + OOEBgvv("OOMP-POTE-95D-L-X-X-extra") :
name=="OOMP-POTE-95D-L-X-X-mainD"      ? 1.5 :
name=="OOMP-POTE-95D-L-X-X-mainX"      ? 0 :
name=="OOMP-POTE-95D-L-X-X-mainY"      ? 0 :
name=="OOMP-POTE-95D-L-X-X-mainZ"      ? - 1.5 :
name=="OOMP-POTE-95D-L-X-X-mainRadius"     ? 0 :
name=="OOMP-POTE-95D-L-X-X-mainRotX"       ? 0 :
name=="OOMP-POTE-95D-L-X-X-mainRotY"       ? 0 :
name=="OOMP-POTE-95D-L-X-X-mainRotZ"       ? 0 :
//////OOMP-POTE-95D-L-X-01-legA dimensions'
name=="OOMP-POTE-95D-L-X-X-legAW"      ? 0.6 +  OOEBgvv("OOMP-LEDS-clearance") : 
name=="OOMP-POTE-95D-L-X-X-legAH"      ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAW") :
name=="OOMP-POTE-95D-L-X-X-legAD"      ? 5 :
name=="OOMP-POTE-95D-L-X-X-legAX"      ? 2.54 :
name=="OOMP-POTE-95D-L-X-X-legAY"      ? -2 :
name=="OOMP-POTE-95D-L-X-X-legAZ"      ? 0 :
name=="OOMP-POTE-95D-L-X-X-legARadius"     ? 0 :
name=="OOMP-POTE-95D-L-X-X-legARotX"       ? 0 :
name=="OOMP-POTE-95D-L-X-X-legARotY"       ? 0 :
name=="OOMP-POTE-95D-L-X-X-legARotZ"       ? 0 :
//////OOMP-POTE-95D-L-X-X-legB dimensions'
name=="OOMP-POTE-95D-L-X-X-legBW"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAW") :
name=="OOMP-POTE-95D-L-X-X-legBH"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAH") :
name=="OOMP-POTE-95D-L-X-X-legBD"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAD") :
name=="OOMP-POTE-95D-L-X-X-legBX"       ? 0 :
name=="OOMP-POTE-95D-L-X-X-legBY"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAY") :
name=="OOMP-POTE-95D-L-X-X-legBZ"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAZ") :
name=="OOMP-POTE-95D-L-X-X-legBRadius"      ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARadius") :
name=="OOMP-POTE-95D-L-X-X-legBRotX"        ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARotX") :
name=="OOMP-POTE-95D-L-X-X-legBRotY"        ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARotY") :
name=="OOMP-POTE-95D-L-X-X-legBRotZ"        ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARotZ") :
//////OOMP-POTE-95D-L-X-X-legC dimensions'
name=="OOMP-POTE-95D-L-X-X-legCW"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAW") :
name=="OOMP-POTE-95D-L-X-X-legCH"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAH") :
name=="OOMP-POTE-95D-L-X-X-legCD"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAD") :
name=="OOMP-POTE-95D-L-X-X-legCX"       ? -2.54 :
name=="OOMP-POTE-95D-L-X-X-legCY"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAY") :
name=="OOMP-POTE-95D-L-X-X-legCZ"       ? OOEBgvv("OOMP-POTE-95D-L-X-X-legAZ") :
name=="OOMP-POTE-95D-L-X-X-legCRadius"      ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARadius") :
name=="OOMP-POTE-95D-L-X-X-legCRotX"        ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARotX") :
name=="OOMP-POTE-95D-L-X-X-legCRotY"        ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARotY") :
name=="OOMP-POTE-95D-L-X-X-legCRotZ"        ? OOEBgvv("OOMP-POTE-95D-L-X-X-legARotZ") :

      ////// OOMP-RESE-W04-X-X-X
//////OOMP-RESE-W04-X-X-X-legA dimensions'      
name=="OOMP-RESE-W04-X-X-X-legAW"       ? OOEBgvv("OOMP-leadWidthDefault") + OOEBgvv("OOMP-LEDS-clearance")  :
name=="OOMP-RESE-W04-X-X-X-legAH"       ? OOEBgvv("OOMP-RESE-W04-X-X-X-legAW") :
name=="OOMP-RESE-W04-X-X-X-legAD"       ? 5 :
name=="OOMP-RESE-W04-X-X-X-legAX"       ? 3.81 :
name=="OOMP-RESE-W04-X-X-X-legAY"       ? 0 :
name=="OOMP-RESE-W04-X-X-X-legAZ"       ? 0 :
name=="OOMP-RESE-W04-X-X-X-legARadius"      ? 0 :
name=="OOMP-RESE-W04-X-X-X-legARotX"        ? 0 :
name=="OOMP-RESE-W04-X-X-X-legARotY"        ? 0 :
name=="OOMP-RESE-W04-X-X-X-legARotZ"        ? 0 :
//////OOMP-RESE-W04-X-X-X-legB dimensions'
name=="OOMP-RESE-W04-X-X-X-legBW"       ? OOEBgvv("OOMP-RESE-W04-X-X-X-legAW") :
name=="OOMP-RESE-W04-X-X-X-legBH"       ? OOEBgvv("OOMP-RESE-W04-X-X-X-legAH") :
name=="OOMP-RESE-W04-X-X-X-legBD"       ? OOEBgvv("OOMP-RESE-W04-X-X-X-legAD") :
name=="OOMP-RESE-W04-X-X-X-legBX"       ? -OOEBgvv("OOMP-RESE-W04-X-X-X-legAX") :
name=="OOMP-RESE-W04-X-X-X-legBY"       ? OOEBgvv("OOMP-RESE-W04-X-X-X-legAY") :
name=="OOMP-RESE-W04-X-X-X-legBZ"       ? OOEBgvv("OOMP-RESE-W04-X-X-X-legAZ") :
name=="OOMP-RESE-W04-X-X-X-legBRadius"      ? OOEBgvv("OOMP-RESE-W04-X-X-X-legARadius") :
name=="OOMP-RESE-W04-X-X-X-legBRotX"        ? OOEBgvv("OOMP-RESE-W04-X-X-X-legARotX") :
name=="OOMP-RESE-W04-X-X-X-legBRotY"        ? OOEBgvv("OOMP-RESE-W04-X-X-X-legARotY") :
name=="OOMP-RESE-W04-X-X-X-legBRotZ"        ? OOEBgvv("OOMP-RESE-W04-X-X-X-legARotZ") :

0;