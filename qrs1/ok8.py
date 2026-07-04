import serial
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ================= 配置 =================
COM_PORT = "COM6"
BAUD_RATE = 115200
WAVE_POINTS = 50    # 波形窗口总点数
REFRESH_TIME = 0.03
MAX_READ_PER_LOOP = 15  # 单次循环最多数
# ========================================

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.0005)
wave = [0.0] * WAVE_POINTS  # 固定长度波形缓存

# 绘图初始化
plt.ion()
fig, ax = plt.subplots(figsize=(16, 8), num="示波器")
line, = ax.plot(wave, color="#00cc00", linewidth=1.2)
ax.set_ylim(0, 3.3)
ax.set_xlim(0, WAVE_POINTS - 1)
ax.grid(True, alpha=0.3)
# 绘图、数据处理部分
try:
    while True:
        read_count = 0
        # 限制单次读取数量，避免缓存一次性塞满重复数值
        while ser.in_waiting > 0 and read_count < MAX_READ_PER_LOOP:
            try:
                line_data = ser.readline().decode("utf-8").strip()
                if not line_data:
                    continue
                val = float(line_data)
                wave.pop(0)
                wave.append(val)
                read_count += 1
            except (ValueError, UnicodeDecodeError):
                continue
        # 刷新波形
        line.set_ydata(wave)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(REFRESH_TIME)

except KeyboardInterrupt:
    print("\n程序退出")
finally:
    ser.close()
    plt.close(fig)