@echo off
::==================================================================
:: translate_srt_gpu.bat  –  3080 Ti 전용, 프리셋(1/2/3) 대화식 실행
::==================================================================
chcp 65001 >nul & setlocal EnableDelayedExpansion
set "PYTHONUTF8=1"

echo ==================================================
echo  RTX 3080 Ti  GPU-Offline  SRT  Translator
echo ==================================================
echo  ① 고급(1) – 줄당, 최고 품질
echo  ② 중급(2) – 배치4, 2× 속도
echo  ③ 저급(3) – 8-bit, 속도↑ VRAM↓
echo ==================================================
echo.

REM ────────── 1) 파일 입력 ──────────
:ASK_SRC
set /P "SRC_RAW=원본 SRT (드래그): "
for %%A in (%SRC_RAW%) do set "SRC=%%~A"
if not exist "!SRC!" (
    echo [ERROR] 파일 없음. 다시 입력!
    goto ASK_SRC
)
for %%F in ("!SRC!") do set "BASE=%%~nF"

REM ────────── 2) 출력 ──────────
set "DEF_DST=!BASE!_ko.srt"
set /P "DST_RAW=출력 SRT [!DEF_DST!]: "
if "!DST_RAW!"=="" (set "DST=!DEF_DST!") else for %%A in ("!DST_RAW!") do set "DST=%%~A"

REM ────────── 3) 언어 ──────────
set /P "SRC_LG=원본 언어[ja]: "
if "!SRC_LG!"=="" set "SRC_LG=ja"
set /P "TGT_LG=목표 언어[ko]: "
if "!TGT_LG!"=="" set "TGT_LG=ko"

REM ────────── 4) 프리셋 ──────────
:ASK_PRE
set /P "PN=프리셋 번호(1/2/3)[1]: "
if "!PN!"=="" set "PN=1"
if "!PN!"=="1" (set "PRE=hi") else if "!PN!"=="2" (set "PRE=mid") else if "!PN!"=="3" (set "PRE=low") else (
    echo 1,2,3 중 선택!
    goto ASK_PRE
)
echo.

echo [GPU 0 – !PRE! preset 번역 중…]
python "%~dp0translate_srt.py" "!SRC!" "!DST!" -i !SRC_LG! -o !TGT_LG! -p !PRE!
if errorlevel 1 (
    echo ------------- [FAIL] 오류 발생 -------------
) else (
    echo ------------- [SUCCESS] → "!DST!" -------------
)
pause
exit /b
