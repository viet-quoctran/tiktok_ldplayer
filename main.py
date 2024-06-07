from ppadb.client import Client as AdbClient
import uiautomator2 as u2
import time
import random
from concurrent.futures import ThreadPoolExecutor

# Khởi tạo kết nối ADB cho nhiều giả lập
def connect_multiple_adb():
    client = AdbClient(host="127.0.0.1", port=5037)
    # Thêm các thiết bị đã liệt kê từ lệnh `adb devices`
    devices = [
        client.device("127.0.0.1:5555"),  # Giả lập 1
        # Thêm các giả lập khác nếu cần
    ]
    connected_devices = [device for device in devices if device is not None]

    if len(connected_devices) == 0:
        print("No devices connected")
        exit(1)

    for device in connected_devices:
        print(f"Connected to {device.serial}")

    return connected_devices

# Lấy cấu trúc UI của ứng dụng TikTok
def get_ui_structure(device_serial):
    d = u2.connect(device_serial)
    d.app_start('com.ss.android.ugc.trill')
    time.sleep(15)  # Tăng thời gian chờ để đảm bảo ứng dụng mở hoàn toàn

    # Lấy cấu trúc UI hiện tại và lưu vào file XML
    xml = d.dump_hierarchy()
    with open(f"tiktok_ui_{device_serial}.xml", "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"UI structure saved for device {device_serial}")

# Tự động hóa các thao tác trên TikTok
def automate_tiktok(device):
    # Mở ứng dụng TikTok (cập nhật ID gói chính xác)
    print(f"Attempting to start TikTok on {device.serial}")
    output = device.shell('am start -n com.ss.android.ugc.trill/com.ss.android.ugc.aweme.splash.SplashActivity')

    # Đợi ứng dụng mở
    time.sleep(15)  # Tăng thời gian chờ để giảm tải

    # Vuốt lên để xem video tiếp theo
    def swipe_up(device):
        # Duration ngẫu nhiên từ 500ms đến 1500ms (0.5 giây đến 1.5 giây)
        duration = random.randint(500, 1500)
        print(f"Swiping up on {device.serial} with duration {duration}")
        output = device.shell(f'input swipe 500 1500 500 500 {duration}')
        print(output)
    
    # Vuốt ngẫu nhiên từ 10 đến 15 lần
    num_swipes = random.randint(10, 15)
    for _ in range(num_swipes):
        swipe_up(device)
        wait_time = random.randint(10, 20)  # Tăng thời gian chờ để giảm tải
        print(f"Waiting for {wait_time} seconds on {device.serial}")
        time.sleep(wait_time)

# Khởi động và thực hiện tự động hóa
def main():
    devices = connect_multiple_adb()
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        # Thực hiện tự động hóa và lấy cấu trúc UI song song
        futures = []
        for device in devices:
            futures.append(executor.submit(automate_tiktok, device))
            futures.append(executor.submit(get_ui_structure, device.serial))
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
