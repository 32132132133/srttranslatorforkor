# srttranslatorforkor

srttranslatorforkor는 SRT 자막 파일을 원하는 언어로 번역하는 간단한 파이썬 도구입니다. 기본 목적은 영어 자막을 한국어로 변환하는 것이지만 `--src`와 `--dest` 옵션을 이용해 다른 언어 조합도 사용할 수 있습니다.

## 주요 기능

- SRT 형식의 자막을 읽어 각 대사를 번역
- 시퀀스 번호와 타임 스탬프는 그대로 유지
- Google 번역 API를 활용하여 빠른 번역 제공

## 설치 방법

1. 저장소를 클론합니다.
   ```bash
   git clone <저장소_URL>
   cd srttranslatorforkor
   ```
2. 파이썬 3.8 이상이 필요합니다. 가상환경을 권장합니다.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. 필요한 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```

## 사용 방법

1. 번역하고 싶은 SRT 파일을 준비합니다.
2. 아래와 같이 스크립트를 실행합니다.
   ```bash
   python translate_srt.py -i original.srt -o translated.srt --src en --dest ko
   ```
   - `--src` : 원본 자막의 언어 코드 (기본값 `auto`)
   - `--dest` : 번역할 대상 언어 코드 (기본값 `ko`)
3. 실행 후 `translated.srt` 파일에서 번역된 자막을 확인할 수 있습니다.

## 검색 최적화를 위한 키워드

- SRT 자막 번역
- 한국어 자막 변환
- Python subtitle translator
- Googletrans 예제

위 키워드들을 README에 포함하여 검색 엔진에서 쉽게 찾을 수 있도록 하였습니다.

## 라이선스

MIT 라이선스를 사용하며, 자유롭게 수정 및 배포가 가능합니다.
