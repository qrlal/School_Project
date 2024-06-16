import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

# 파일 경로 설정
input_file = 'output1.wav'
output_file = 'output.wav'

# 음성 파일 로드
y, sr = librosa.load(input_file, sr=None)
t = np.arange(len(y)) / sr
noise = np.random.normal(0, 0.1, len(y))
y = y+noise 
# 푸리에 변환 적용
Y = fft(y)

# 주파수 성분의 크기 계산
magnitude = np.abs(Y)

# 고주파 성분 제거 (임계값 이상)
threshold_high = 30000  # 이 값은 실제 적용 시 조정 필요
Y[np.abs(Y) > threshold_high] = 0

# 너무 적은 비중을 차지하는 주파수 성분 제거
threshold_low = 80  # 가장 큰 성분의 1% 이하인 성분 제거
Y[np.abs(Y) < threshold_low] = 0

# 역 푸리에 변환 적용
y_filtered = ifft(Y).real

# 잡음 제거된 음성 파일 저장
sf.write(output_file, y_filtered, sr)

# 결과를 시각화하여 비교
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.title('Original Signal')
plt.plot(y)
plt.xlabel('Sample')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.title('Filtered Signal')
plt.plot(y_filtered)
plt.xlabel('Sample')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
