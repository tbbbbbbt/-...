import serial
import matplotlib.pyplot as plt

# ================= 配置 =================
COM_PORT = "COM6"     # 你自己的串口号
BAUD_RATE = 115200
WAVE_POINTS = 100     # 固定100个点
REFRESH_TIME = 0.1    # 100ms刷新
# ========================================

# 打开串口
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.01)

# 初始化波形缓冲区（固定长度100）
wave = [0.0] * WAVE_POINTS

# 画图初始化
plt.ion()
fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot(wave)
ax.set_ylim(0, 3.3)
ax.set_xlim(0, WAVE_POINTS - 1)
ax.grid(True)

# 主循环
while True:
    # 读取所有可用数据
    while ser.in_waiting:
        line_data = ser.readline().decode("utf-8").strip()
        if line_data:
            
            val = float(line_data)
            
            # 示波器滚动逻辑：左边丢一个，右边加新的
            wave.pop(0)        # 删掉最旧的点
            wave.append(val)   # 加入新的点
    # 100ms 更新一次波形
    line.set_ydata(wave)
    plt.draw()
    plt.pause(REFRESH_TIME)

    