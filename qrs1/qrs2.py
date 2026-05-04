import serial
import matplotlib.pyplot as plt
import numpy as np

# ================= 配置 =================
COM_PORT = "COM6"
BAUD_RATE = 115200
WAVE_POINTS = 100
REFRESH_TIME = 0.01
TRIG_LEVEL = 1.65
# ========================================

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.001)

wave = [0.0] * 200  # 保持你原来的大小

edge_count = 0
first_cnt = 0
point_cnt = 0
period = 25

plt.ion()
fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot([0]*WAVE_POINTS)
ax.set_ylim(0, 3.3)
ax.set_xlim(0, WAVE_POINTS - 1)
ax.grid(True)

while True:
    while ser.in_waiting:
        line_data = ser.readline().decode("utf-8").strip()
        if line_data:

            if line_data == "aaa":
                print("✅ 收到 AUTO → 4倍周期显示")
                WAVE_POINTS = period * 4

                ax.clear()
                line, = ax.plot([0]*WAVE_POINTS)
                ax.set_ylim(0, 3.3)
                ax.set_xlim(0, WAVE_POINTS - 1)
                ax.grid(True)
                continue

            val = float(line_data)
            if len(wave) >= 200:
                wave.pop(0)
            wave.append(val)

            point_cnt += 1
            if len(wave) >= 2:
                if wave[-2] < TRIG_LEVEL and wave[-1] >= TRIG_LEVEL:
                    edge_count += 1
                    if edge_count == 1:
                        first_cnt = point_cnt
                    if edge_count == 3:
                        period = point_cnt - first_cnt
                        edge_count = 0
                        print(f"📌 周期 = {period} ms")

    # 🔥 只保留：触发显示（和你原来 else 里一模一样）
    search_area = wave[-WAVE_POINTS * 2 :]
    trig_pos = -1
    for i in range(1, len(search_area)):
        if search_area[i-1] < TRIG_LEVEL and search_area[i] >= TRIG_LEVEL:
            trig_pos = i
            break

    # 🔥 强制保证长度够，不丢波形
    if trig_pos != -1 and trig_pos + WAVE_POINTS <= len(search_area):
        show = search_area[trig_pos : trig_pos + WAVE_POINTS]
    else:
        show = search_area[-WAVE_POINTS:]

    line.set_ydata(show)
    line.set_xdata(np.arange(len(show)))
    
    plt.draw()
    plt.pause(REFRESH_TIME)