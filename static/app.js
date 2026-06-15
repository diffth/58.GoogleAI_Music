document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generator-form');
    const submitBtn = document.getElementById('submit-btn');
    const submitBtnText = submitBtn.querySelector('.btn-text');
    
    const statusContainer = document.getElementById('status-container');
    const loadingContainer = document.getElementById('loading-container');
    const resultContainer = document.getElementById('result-container');
    
    const audioPlayer = document.getElementById('audio-player');
    const downloadBtn = document.getElementById('download-btn');
    const lyricsContent = document.getElementById('lyrics-content');
    const copyBtn = document.getElementById('copy-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI 상태: 로딩 중으로 변경
        submitBtn.disabled = true;
        submitBtnText.textContent = '음악을 빚는 중...';
        
        statusContainer.classList.add('hidden');
        resultContainer.classList.add('hidden');
        loadingContainer.classList.remove('hidden');

        // 입력 값 캡처
        const formData = new FormData(form);
        const requestData = {
            genre: formData.get('genre'),
            bpm_key: formData.get('bpm_key'),
            mood: formData.get('mood'),
            vocal: formData.get('vocal')
        };

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || '음악 생성 중 오류가 발생했습니다.');
            }

            if (result.success) {
                // 가사 표시
                lyricsContent.textContent = result.lyrics;

                // 오디오 소스 설정
                if (result.audio) {
                    const audioSrc = `data:audio/mp3;base64,${result.audio}`;
                    audioPlayer.src = audioSrc;
                    downloadBtn.href = audioSrc;
                    downloadBtn.classList.remove('hidden');
                } else {
                    audioPlayer.src = '';
                    downloadBtn.classList.add('hidden');
                }

                // UI 상태: 결과 출력으로 변경
                loadingContainer.classList.add('hidden');
                resultContainer.classList.remove('hidden');
            } else {
                throw new Error('음악 생성을 실패했습니다.');
            }
        } catch (error) {
            console.error(error);
            alert(`❌ 에러: ${error.message}\n\n.env 파일에 GEMINI_API_KEY가 올바르게 입력되었는지 확인해주세요.`);
            
            // UI 복원
            loadingContainer.classList.add('hidden');
            statusContainer.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtnText.textContent = '음악 생성하기';
        }
    });

    // 가사 복사 기능
    copyBtn.addEventListener('click', () => {
        const text = lyricsContent.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '복사 완료! ✨';
            copyBtn.style.background = 'var(--success)';
            copyBtn.style.color = 'white';
            
            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.style.background = '';
                copyBtn.style.color = '';
            }, 2000);
        }).catch(err => {
            console.error('클립보드 복사 실패:', err);
        });
    });
});
