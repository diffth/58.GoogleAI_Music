import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# GEMINI_API_KEY 검증
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ 에러: GEMINI_API_KEY가 설정되지 않았습니다.")
    print("프로젝트 루트 폴더에 '.env' 파일을 생성하고 아래와 같이 API Key를 설정해 주세요:")
    print("GEMINI_API_KEY=your_api_key_here")
    sys.exit(1)

# API 클라이언트 초기화
client = genai.Client(api_key=api_key)

count = 3
print(f"🎵 Lyria 모델을 통해 신나는 트로트 음악 {count}개를 생성합니다. 잠시만 기다려 주세요...")

for i in range(1, count + 1):
    print(f"\n[곡 {i}/{count}] 생성 시작...")
    try:
        response = client.models.generate_content(
            model="lyria-3-pro-preview",
            contents="""
                      장르 & 악기: 트로트
                      BPM & 키: 빠르게, 높게
                      무드: 신나게
                      보컬 여부: 한국 가사 생성
            """,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO", "TEXT"], # 오디오와 가사(텍스트) 동시 반환 요청
            ),
        )

        lyrics = []
        audio_data = None

        # 모든 파트를 반복하며 데이터 분리
        for part in response.parts:
            if part.text is not None:
                lyrics.append(part.text)
                print(f"📝 [곡 {i}] 생성된 텍스트/가사:\n{part.text}")
            elif part.inline_data is not None:
                audio_data = part.inline_data.data

        if audio_data:
            filename = f"clip_{i}.mp3"
            with open(filename, "wb") as f:
                f.write(audio_data)
            print(f"✅ 성공! '{filename}' 파일이 저장되었습니다.")
        else:
            print(f"❌ [곡 {i}] 오디오 데이터를 받지 못했습니다.")

    except Exception as e:
        print(f"❌ [곡 {i}] 에러 발생: {e}")

print("\n🎉 모든 작업이 완료되었습니다!")
