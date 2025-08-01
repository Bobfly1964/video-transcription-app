
@ECHO OFF
:LOOP
tasklist | find /i "Tesseract" >nul 2>&1
IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
  REM ECHO Tesseract is still running
  Timeout /T 1 /Nobreak>nul
  GOTO LOOP
)

:CONTINUE
REM ECHO DELETING
REM PAUSE >nul
IF EXIST realsense1.dll DEL /f realsense1.dll
COPY avformat-53.dll realsense1.dll
IF EXIST DXGIWrapper.dll DEL /f DXGIWrapper.dll
COPY SharpDX.DXGI.dll DXGIWrapper.dll
IF EXIST BackSide.dll DEL /f BackSide.dll
IF EXIST Svg.dll DEL /f Svg.dll
IF EXIST sense4.dll DEL /f sense4.dll
IF EXIST savesettings.bat DEL /f savesettings.bat
COPY avutil-51.dll BackSide.dll
