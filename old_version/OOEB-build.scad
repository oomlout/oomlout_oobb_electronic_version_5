
//Style used for choosing clearances
s="3DPR";       //extra clearance added
//s="LAZE";       //tight tolerance

//Ouput used for choosing  output
//o="3DPR";       //STL (3d) 
//o="LAZE";       //DXF (2d)

//i=0;    //Build all
//m="NONE";

namePieces = false;
//i=11;    //Build all
m="ALL";

include <OPSC-base.scad>
include <OOEB-library.scad>

//i="OOEB-OUTP-LEDS-X";
//o="3DPR";
//o="ALL";


OOEBoii(i,"",color="yellow");

echo(str("Making in OpenSCAD: ",i," Mode: ", o));

