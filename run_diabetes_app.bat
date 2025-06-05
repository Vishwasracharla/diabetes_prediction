@echo off
cd /d "%~dp0"
start "" "http://localhost:8505"
streamlit run app.py --server.address=127.0.0.1 --server.port=8505
