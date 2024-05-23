def calculate_wavelength(frequency_mhz):
    c = 3 * 10**8  # 光速，單位：公尺/秒
    frequency_hz = frequency_mhz * 10**6  # 將頻率轉換為赫茲
    wavelength_m = c / frequency_hz  # 計算波長，單位：公尺
    wavelength_cm = wavelength_m * 100  # 將波長轉換為公分
    return wavelength_cm

# 輸入頻率（單位：MHz）
frequency_mhz = float(input("請輸入頻率（MHz）："))

# 計算波長
wavelength_cm = calculate_wavelength(frequency_mhz)

#4分之波長
quarter_wavelength_cm = wavelength_cm/4

#2分之波長
half_wavelength_cm = wavelength_cm/2


# 輸出結果
print(f"{frequency_mhz} MHz 的波長 {wavelength_cm} 公分 , 4分之波長 {quarter_wavelength_cm} 公分 , 2分之波長 {half_wavelength_cm} 公分 ")