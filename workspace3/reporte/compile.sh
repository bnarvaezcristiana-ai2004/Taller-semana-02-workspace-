#!/bin/bash

# Script de compilación de LaTeX
# Genera reporte.pdf desde reporte.tex

echo "Compilando reporte LaTeX..."

# Compilar con pdflatex (2 veces para resolver referencias)
pdflatex -interaction=nonstopmode reporte.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode reporte.tex > /dev/null 2>&1

# Limpiar archivos auxiliares
rm -f *.aux *.log *.out *.toc

if [ -f "reporte.pdf" ]; then
    echo "✓ reporte.pdf generado correctamente"
    echo "  Ubicación: $(pwd)/reporte.pdf"
else
    echo "✗ Error al compilar LaTeX"
    exit 1
fi
