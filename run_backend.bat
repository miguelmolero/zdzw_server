@echo off

:: 1. Asegurarse de que la carpeta estática dist existe
if not exist static\dist (
    mkdir static\dist
)

:: 2. Copiar los archivos estáticos al backend
echo Copy build files...
del /Q static\dist\*
xcopy /E /I ..\zdzw_client\dist static\dist

:: 3. Ejecutar el backend
echo Run app...
uvicorn main:app --reload
pause
