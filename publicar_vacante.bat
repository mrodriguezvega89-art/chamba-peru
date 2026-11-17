@echo off
chcp 65001 > nul
title Publicador de Vacantes Oficiales - Chamba Perú
cls
echo ==========================================================
echo    PORTAL DE EMPLEOS PERU - PUBLICADOR DE VACANTES
echo ==========================================================
echo.
cd /d "D:\Antigravity\chamba-peru"
python backend\add_featured_job.py --interactive
echo.
echo Presiona cualquier tecla para salir...
pause > nul
