# 计算短路电流和开路电压
import csv
import os
from datetime import datetime

from numpy import power


def calculate_iv_metrics(measurement_data, cell_area, cell_ID):
    if not measurement_data:
        return 0, 0
    
    data_time, voltages, currents = zip(*measurement_data)
    # 反转电流值
    currents = [-curr for curr in currents]
    
     # 确保数据长度大于 1
    if len(voltages) < 2 or len(currents) < 2:
        raise ValueError("Data must contain at least two points.")
    
    # 确保数据长度一致
    if len(voltages) != len(currents):
        raise ValueError("Voltage and current data must have the same length.")
    

    # 确保数据是有序的
    # if not all(voltages[i] <= voltages[i+1] for i in range(len(voltages)-1)):
    #     raise ValueError("Voltage data must be in ascending order.")

    # 确保数据是有序的 （不是降序）
    # if not all(currents[i] <= currents[i+1] for i in range(len(currents)-1)):
    #     raise ValueError("Current data must be in ascending order.")
    
    # 判断数据是否过零
    
    # if voltages[0] >= 0 or voltages[-1] <= 0:
    #     raise ValueError("Voltage data must span both positive and negative values.")

    # if currents[0] >= 0 or currents[-1] <= 0:
    #     raise ValueError("Current data must span both positive and negative values.")
    # 用线性插值法计算短路电流和开路电压
    
   

    # 找到最接近 0 电压的数据点
    min_voltage_index = min(range(len(voltages)), key=lambda i: abs(voltages[i]))
    short_circuit_current = currents[min_voltage_index]

    # 找到最接近 0 电流的数据点
    min_current_index = min(range(len(currents)), key=lambda i: abs(currents[i]))
    open_circuit_voltage = voltages[min_current_index]

    # 电流乘电压功率列表
    power_list = [curr * volt for curr, volt in zip(currents, voltages)]
    # 找到最大功率点
    max_power_index = power_list.index(max(power_list))
    max_power_voltage = voltages[max_power_index]
    max_power_current = currents[max_power_index]
    max_power = power_list[max_power_index]

    # 填充因子
    fill_factor = (max_power / (short_circuit_current * open_circuit_voltage)) * 100

    # 电池片效率
    ETA = (max_power / cell_area) * 1000
    # 电流密度 mA/cm²
    Jsc = (short_circuit_current / cell_area)  

    # 建立数据文件夹存储数据
    if not os.path.exists('data—analysis'):
        os.makedirs('data—analysis')
    # 完整路径
    # 增加时间戳
    # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timesdate = datetime.now().strftime('%Y-%m-%d')
    filename = os.path.join('data—analysis', f'{timesdate}iv_results.csv')

    # 保存到文件中追加模式   
    with open(filename, 'a', newline='') as f:
        # 增加时间戳用数据最后时间
        timestamp = data_time[-1]
        writer = csv.writer(f)
        # 增加表头
        if f.tell() == 0:
            writer.writerow(['cell_ID', '时间戳', '短路电流', '开路电压', '最大功率', 'ETA', '最大功率电压', '最大功率电流', '填充因子', 'Jsc'])
        writer.writerow([cell_ID, timestamp, short_circuit_current, open_circuit_voltage, max_power, ETA, max_power_voltage, max_power_current, fill_factor, Jsc])
    # print(short_circuit_current, open_circuit_voltage, max_power, max_power_voltage, max_power_current, fill_factor)
    return short_circuit_current, open_circuit_voltage, max_power, ETA, max_power_voltage,  max_power_current, fill_factor, Jsc    