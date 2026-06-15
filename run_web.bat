@echo off
chcp 65001 > nul
echo ===================================================
echo   AI BeatCraft - Google AI Music Generator 구동기
echo ===================================================
echo.

:: 가상환경 체크
if not exist .venv (
    echo [정보] 가상환경(.venv)이 존재하지 않아 생성합니다...
    python -m venv .venv
    if errorlevel 1 (
        echo [에러] 파이썬이 설치되어 있지 않거나 환경 변수 설정에 문제가 있습니다.
        pause
        exit /b
    )
)

:: 라이브러리 설치
echo [정보] 필요한 패키지를 검사하고 설치합니다...
.venv\Scripts\pip.exe install google-genai fastapi uvicorn python-dotenv

:: .env 파일 체크
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
    echo API 키 설정을 완료한 후, 아무 키나 누르면 웹 서버가 실행됩니다.
    pause
)

:: 웹 서버 실행 및 브라우저 열기
echo.
echo [정보] 웹 서버를 실행합니다...
echo 브라우저에서 http://127.0.0.1:8000 주소로 접속해 주세요.
echo.
start http://127.0.0.1:8000
.venv\Scripts\uvicorn.exe main:app --host 127.0.0.1 --port 8000 --reload
pause
