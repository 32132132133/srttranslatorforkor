@echo off
:: CP949(ANSI) 인코딩 .srt 파일을 UTF-8로 변환하는 배치 스크립트

echo =====================================
echo   SRT to UTF-8 Converter Batch
echo =====================================

:: 입력 파일 이름 받기
set /p inputFile=Enter SRT file name (cp949 encoded, with .srt):

:: 출력 파일 이름 설정 (.utf8.srt 자동 지정)
set outputFile=%inputFile:.srt=.utf8.srt%

echo.
echo Converting "%inputFile%" to UTF-8 as "%outputFile%"...

:: PowerShell 사용하여 변환
powershell -Command "Get-Content -Encoding Default '%inputFile%' | Set-Content -Encoding utf8 '%outputFile%'"

echo.
echo Conversion completed: %outputFile%
pause

