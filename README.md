# Phantom-Sentinel-The-Guardian-Across-Time-and-Space
鬼影監視：穿越時空的守護者

# GhostWatcher: The Time-Warping Guardian
一個專為監控小偷設計的專案，結合樹莓派的硬體功能，實現偵測入侵者並將影片通知至 LINE 的功能。

## 安裝指令
以下為專案運行所需的依賴模組及安裝指令：

### 必須的依賴套件
1. **RPi.GPIO**  
   用於控制樹莓派 GPIO 腳位的必要模組。  
   ```bash
   sudo apt install python3-rpi-lgpio
   ```

### 2. OpenCV
用於處理影像的功能。
```bash
pip install opencv-python
pip install opencv-python-headless
```

### 3. Picamera2
控制 Raspberry Pi 相機的模組。
```bash
pip install picamera2
sudo apt-get install -y libcamera-apps
```

### 4. LINE Bot SDK
用於透過 LINE 傳送影片訊息。
```bash
pip install line-bot-sdk
```

### 5. Requests
用於處理 HTTP 請求，例如上傳影片至 Imgur 的功能。
```bash
pip install requests
```

### 6. Pytz
處理時區所需的模組。
```bash
pip install pytz
```

### 備註

#### 相機測試建議
在開始正式運作前，可以使用以下指令來測試相機是否正常工作：  
```bash
libcamera-hello
```
#### 啟動網路功能
確保樹莓派已連接到網路，並且可以成功訪問 LINE API 與 Imgur 的服務。 
