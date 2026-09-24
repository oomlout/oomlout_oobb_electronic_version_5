REM ######  GENERATING %ITEM%  ######
REM 
REM 
@echo off
setlocal enabledelayedexpansion 

SET STYLE=3DPR
SET FILEFULL=parts\%ITEM%\

del %FILEFULL%.stl

echo Making Index: %ITEM%	
del %FILEFULL%-ITEM-3DPR.stl   
openscad -o %FILEFULL%%ITEM%-3DPR.stl -D "i="""%ITEM%%""";o=\"3DPR"" OOEB-3DPR.scad
del %FILEFULL%-ITEM-3DPR.png   
openscad -o %FILEFULL%%ITEM%-3DPR.png -D "i="""%ITEM%""";o=\"3DPR"" OOEB-3DPR.scad	
del %FILEFULL%-ITEM-LAZE.dxf
openscad -o %FILEFULL%%ITEM%-LAZE.dxf -D "i="""%ITEM%""";o=\"LAZE"" OOEB-LAZE.scad
del %FILEFULL%-%ITEM%-LAZE.svg
openscad -o %FILEFULL%-ITEM-LAZE.svg -D "i="""%ITEM%""";o=\"LAZE"" OOEB-LAZE.scad
del %FILEFULL%-ITEM-LAZE.pdf
inkscape.exe --export-filename="%FILEFULL%-%ITEM%-LAZE.pdf" "%FILEFULL%-%ITEM%-LAZE.svg"	



REM       DONE!

