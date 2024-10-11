#!/bin/bash

# 2. Copiar los archivos estáticos al backend
echo "copy build files..."
rm -rf static/dist
cp -r ../zdzw_client/dist static/

# 3. Ejecutar el backend
echo "run app..."
uvicorn main:app --reload
