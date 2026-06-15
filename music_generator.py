from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="lyria-3-pro-preview",
    contents="""
			  장르 & 악기: 트로트
			  BPM & 키: 빠르게, 높게
			  무드: 신나게
			  보컬 여부: 한국 가사 생성
    """,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO","TEXT"],# 오디오와 가사(텍스트) 동시 반환 요청
    ),
)

lyrics = []
audio_data =None

# 모든 파트를 반복하며 데이터 분리
for part in response.parts:
    if part.text is not None:
        lyrics.append(part.text)
        print("📝 생성된 텍스트/가사:", part.text)
    elif part.inline_data is not None:
        audio_data = part.inline_data.data

if audio_data:
    with open("clip.mp3","wb") as f:
        f.write(audio_data)
    print("✅ 성공! 'clip.mp3' 파일이 저장되었습니다.")
else:
    print("❌ 오디오 데이터를 받지 못했습니다.")
