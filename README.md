# PPT_Gesture_Demo
使用Google MediaPipe偵測手勢，結合PyAutoGui來控制滑鼠、鍵盤操作Power Point播放

* Gesture_Demo.pptx 測試用簡報檔（可略，可使用自己的 Power Point 簡報檔案）
* gesture_recognizer.py Google MediaPipe 官方提供的手勢辨識範例（Google Colab格式）
* gesture_recognizer.task Google MediaPipe 手勢辨識模型
* ppt_gesture_demo.py 手勢控制播放簡報範例

本範例運行前請先安裝好 Python, PIP，創建好虛擬環境，啟動後，再安裝 MediaPipe, PyAutoGui，如下所示。  
1. 切換到想要工作的磁碟 x (可略過，可直接使用啟動命令列模式時的路徑)  
x:  
2. 建立Python虛擬環境 （非必要，主要避免污染原先 Python 開發環境）  
python -m venv mediapipe_env  
3. 啟動Python虛擬環境，進入後命令列提示會變成 (mediapipe_env) x:\  
mediapipe_env\Scripts\activate  
4. 安裝Mediapipe (已包含numpy, matplotlib, opencv-contrib_python等)，可忽略版本設定（==0.10.0)則會安裝最新版本。  
pip install -q mediapipe==0.10.0  
5. 安裝PyAutoGui （處理鍵盤輸入及訊息輸出）  
pip install pyautogui  
6. 離開虛擬環境  
deactivate  

使用方式：  
1. 進入命令列模式 cmd，注意不要讓視窗最大化，可調整到畫面2/3大小大約置於螢幕中間即可。
2. 切換到想要工作的磁碟 x （依安裝磁碟決定）  
x:  
3. 啟動 Python 虛擬環境  
mediapipe_env\Scripts\activate  
4. 下載本範例並進入範例路徑  
git clone --depth=1 https://github.com/OmniXRI/PPT_Gesture_Demo.git  
cd PPT_Gesture_Demo  
5. 開啟 Power Point 簡報並最大化  
6. 執行範例程式，執行後游標會移到視窗最上方並點擊 Power Point 檔案並進入播放模式。而範例程式及視窗會自動移到背景執行（不可視）。   
python ppt_gesture_demo.py  
7. 當偵測到「打開手掌」動作就能自動播放下一頁。
8. 當欲結束控制時，點擊網路攝影機視窗後，再按「q」或「ESC」鍵即可離開程式
