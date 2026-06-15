@echo off
chcp 65001 > nul
echo ===================================================
echo   AI BeatCraft - CLI 음악 생성기
echo ===================================================
echo.

if not exist .venv (
    echo [정보] 가상환경(.venv)이 존재하지 않아 생성합니다...
    python -m venv .venv
)

.venv\Scripts\pip.exe install google-genai python-dotenv

if not exist .env (
    echo [주의] .env 파일이 존재하지 않습니다.
    echo [정보] .env.example 파일을 기반으로 .env 파일을 생성합니다.
    copy .env.example .env > nul
    echo.
    echo ===================================================
    echo  💡 [필수 조치]
    echo  새로 생성된 .env 파일을 메모장 등으로 열고,
    echo  GEMINI_API_KEY= 뒤에 본인의 Gemini API Key를 입력하세요!
    echo ===================================================
    echo.
    notepad .env
    echo API 키 설정을 완료한 후, 아무 키나 누르면 CLI 음악 생성기가 실행됩니다.
    pause
)

echo.
echo [정보] CLI 음악 생성 스크립트를 구동합니다...
echo.
.venv\Scripts\python.exe music_generator.py
pause
