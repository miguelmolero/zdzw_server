#!/bin/bash

# 2. Copiar los archivos estáticos al backend
echo "copy build files..."
rm -rf static/dist/*
cp -r ../zdzw_client/dist/* static/dist

echo "set environment"
export ENVIRONMENT=production

# 3. Ejecutar el backend
echo "run app"
#uvicorn main:app --port 4000 --reload
python main.py
