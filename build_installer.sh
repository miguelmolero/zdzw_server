# 2. Copiar los archivos estáticos al backend
echo "copy build files..."
rm -rf static/dist/*
cp -r ../zdzw_client/dist/* static/dist

# 3. Generar el ejecutable con PyInstaller
echo "Generate PyInstaller executable package..."
pyinstaller --onefile --add-data "static/dist:static/dist" --hidden-import=main main.py
