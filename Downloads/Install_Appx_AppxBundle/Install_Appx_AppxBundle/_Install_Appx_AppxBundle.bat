::&cls&:: сделал: westlife -- ru-board.com -- Эта строчка должна быть первой. Скрывает ошибку из-за метки BOM, если батник "UTF-8 c BOM"
@echo off
chcp 65001 >nul
cd /d "%~dp0"

:: Если этот батник запущен без прав администратора, то перезапуск этого батника с запросом прав администратора.
reg query "HKU\S-1-5-19\Environment" >nul 2>&1 & cls
if "%Errorlevel%" NEQ "0" (PowerShell.exe -WindowStyle Hidden -NoProfile -NoLogo -Command "Start-Process -Verb RunAS -FilePath '%0'"&cls&exit)

:: Используется PowerShell.

echo.
echo.---------------------------------------------------------------------------------------------------
echo.  ^> Установка всех .AppX VCLibs и .NET.Native из папки \Files
echo.
setlocal EnableDelayedExpansion


   echo       Установка: 
   chcp 866 >nul
   PowerShell.exe Add-AppxPackage -Path 'C:\Users\user\Downloads\Install_Appx_AppxBundle\Install_Appx_AppxBundle\Files\NVIDIACorp.NVIDIAControlPanel_8.1.956.0_x64__56jybvy8sckqj.Appx' -ErrorAction Continue
   chcp 65001 >nul





echo.
echo.---------------------------------------------------------------------------------------------------
echo.  ^> Установка всех .AppX ^(кроме VCLibs и .NET.Native^) из папки \Files 
echo.

   echo       Установка: 
   chcp 866 >nul
   PowerShell.exe try { Add-AppxProvisionedPackage -Online -PackagePath 'C:\Users\user\Downloads\Install_Appx_AppxBundle\Install_Appx_AppxBundle\Files\NVIDIACorp.NVIDIAControlPanel_8.1.956.0_x64__56jybvy8sckqj.Appx' -SkipLicense -ErrorAction Stop } catch { Add-AppxPackage -Path 'C:\Users\user\Downloads\Install_Appx_AppxBundle\Install_Appx_AppxBundle\Files\NVIDIACorp.NVIDIAControlPanel_8.1.956.0_x64__56jybvy8sckqj.Appx' -ErrorAction Continue }
   chcp 65001 >nul





echo.---------------------------------------------------------------------------------------------------
echo.  ^> Установка всех .AppxBundle из папки \Files
echo.
   echo       Установка: 
   chcp 866 >nul
   PowerShell.exe try { Add-AppxProvisionedPackage -Online -PackagePath 'C:\Users\user\Downloads\Install_Appx_AppxBundle\Install_Appx_AppxBundle\Files\NVIDIACorp.NVIDIAControlPanel_8.1.956.0_x64__56jybvy8sckqj.Appx' -SkipLicense -ErrorAction Stop } catch { Add-AppxPackage -Path 'C:\Users\user\Downloads\Install_Appx_AppxBundle\Install_Appx_AppxBundle\Files\NVIDIACorp.NVIDIAControlPanel_8.1.956.0_x64__56jybvy8sckqj.Appx' -ErrorAction Continue }
   chcp 65001 >nul



echo.---------------------------------------------------------------------------------------------------
echo.
echo.    Завершено
echo.
echo.Для выхода нажмите любую клавишу ...
TIMEOUT /T -1 >nul
exit

