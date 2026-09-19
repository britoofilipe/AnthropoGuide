@echo off
title AnthropoGuide - Prof. Filipe Brito
echo ===================================================
echo   Iniciando AnthropoGuide (Tutor Cineantropometria)
echo   Coordenação: Prof. Filipe Brito (ISAK Nível 3)
echo ===================================================
echo.
cd /d "%~dp0"
python -m streamlit run app.py
pause
