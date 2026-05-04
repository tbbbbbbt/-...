import serial
import matplotlib.pyplot as plt

# ================= 配置 =================
COM_PORT = "COM6"
BAUD_RATE = 115200
WAVE_POINTS = 100
REFRESH_TIME = 0.1
TRIG_LEVEL = 1.65
# ========================================

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.01)
wave = [0.0] * WAVE_POINTS

# 周期计算变量（修复：不用缓冲区长度，用独立计数）
edge_count = 0
first_cnt = 0
point_cnt = 0
period = 25

plt.ion()
fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot(wave)
ax.set_ylim(0, 3.3)
ax.set_xlim(0, WAVE_POINTS - 1)
ax.grid(True)

# 主循环
while True:
    while ser.in_waiting:
        line_data = ser.readline().decode("utf-8").strip()
        if line_data:

            # ===================== 收到 aaa =====================
            if line_data == "aaa":
                print("✅ 收到 AUTO，设置 4 倍周期显示")
                WAVE_POINTS = period * 4

                # 修复：重建缓冲区 + 重建线条
                wave = [0.0] * WAVE_POINTS
                line.set_xdata(range(WAVE_POINTS))
                ax.set_xlim(0, WAVE_POINTS - 1)

                print(f"✅ 新屏幕宽度：{WAVE_POINTS} 点 (周期 {period}ms)")
                continue

            # ===================== 正常数据 =====================
            val = float(line_data)

            # 滚动逻辑（修复：永远不会空）
            if len(wave) >= WAVE_POINTS:
                wave.pop(0)
            wave.append(val)

            # 周期计算（修复：用独立计数器，100% 准）
            point_cnt += 1
            if len(wave) >= 2:
                if wave[-2] < TRIG_LEVEL and wave[-1] >= TRIG_LEVEL:
                    edge_count += 1

                    if edge_count == 1:
                        first_cnt = point_cnt

                    if edge_count == 3:
                        period = point_cnt - first_cnt  # 正确周期
                        edge_count = 0
                        print(f"📊 周期计算成功：{period} ms")

    # 刷新画面
    line.set_ydata(wave)
    plt.draw()
    plt.pause(REFRESH_TIME)