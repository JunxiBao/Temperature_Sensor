import os
import time

makerobo_ds18b20 = '28-46e7d4454fbc'  # DS18B20 设备地址

# 加载内核模块
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

# 初始化函数
def makerobo_setup():
    global makerobo_ds18b20
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            makerobo_ds18b20 = i  # 获取 DS18B20 的设备地址

# 读取温度数据
def makerobo_read():
    try:
        makerobo_location = '/sys/bus/w1/devices/' + makerobo_ds18b20 + '/w1_slave'
        with open(makerobo_location) as makerobo_tfile:
            makerobo_text = makerobo_tfile.read()
        secondline = makerobo_text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:]) / 1000
        return temperature
    except (IndexError, FileNotFoundError) as e:
        return None  # 返回 None 表示读取失败

# 循环函数
def makerobo_loop():
    while True:
        temp = makerobo_read()
        if temp is not None:
            print("Current temperature : %0.3f C" % temp)
        time.sleep(1)  # 每秒读取一次

# 释放资源
def destroy():
    pass

# 主程序入口
if __name__ == '__main__':
    try:
        makerobo_setup()
        makerobo_loop()
    except KeyboardInterrupt:
        destroy()
