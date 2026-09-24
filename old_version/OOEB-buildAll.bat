@echo off

REM #####################################
REM ######  BUILDING OOEB MODULES  ######
REM #####################################

REM       ###### OOEB-INPU

SET ITEM=OOEB-INPU-BUTA-X
CALL OOEB-buildItem.bat

SET ITEM=OOEB-INPU-POTE-X
CALL OOEB-buildItem.bat

REM      ###### OOEB-OUTP

SET ITEM=OOEB-OUTP-LEDS-X
CALL OOEB-buildItem.bat

PAUSE