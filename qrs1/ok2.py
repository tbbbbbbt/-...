import serial
import matplotlib.pyplot as plt

# ===================== 配置 =====================
COM_PORT = "COM6"      # 你的串口号
BAUD_RATE = 115200
WINDOW_SIZE = 100      # 一屏显示100点
TRIGGER_LEVEL = 1.65   # 触发电平
REFRESH = 0.1          # 100ms刷新
# =================================================

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.01)

# 大缓存，保证不丢数据
buffer = []
last_display = [0.0]*WINDOW_SIZE

# 绘图初始化
plt.ion()
fig, ax = plt.subplots(figsize=(9,4))
line, = ax.plot(last_display)
ax.set_ylim(0, 3.5)
ax.set_xlim(0, WINDOW_SIZE-1)
ax.grid(True)

# ------------------- 主循环 -------------------
while True:
    # 1. 读所有串口数据，只进不出，不修改
    while ser.in_waiting:
        
        line_dat = ser.readline().decode("utf-8").strip()
        val = float(line_dat)
        buffer.append(val)
       

    # 限制缓存长度，防止内存爆炸
    if len(buffer) > 500:
        buffer = buffer[-500:]

    # 2. 找触发点（上升沿穿过 1.65V）
    display = None
    if len(buffer) >= WINDOW_SIZE:
        for i in range(1, len(buffer)):
            prev = buffer[i-1]
            curr = buffer[i]
            # 上升沿触发：从低变高穿过触发点
            if prev < TRIGGER_LEVEL and curr >= TRIGGER_LEVEL:
                # 从触发点开始取 WINDOW_SIZE 个点
                end = i + WINDOW_SIZE
                if end <= len(buffer):
                    display = buffer[i:end]
                    break

    # 3. 找到了就更新，没找到保持上一帧（画面不抖）
    if display is not None:
        last_display = display

    # 4. 画图（完全不修改波形）
    line.set_ydata(last_display)
    plt.draw()
    plt.pause(REFRESH)