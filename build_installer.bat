@echo off

:: 1. Asegurarse de que la carpeta estática dist existe
if not exist static\dist (
    mkdir static\dist
)

:: 2. Copiar los archivos estáticos al backend
echo Copy build files...
del /Q static\dist\*
xcopy /E /I ..\zdzw_client\dist static\dist

:: 3. Generar el ejecutable con PyInstaller
echo Generate PyInstaller executable package...
pyinstaller --onefile --add-data "static\dist;static\dist" --hidden-import=main main.py
pause

