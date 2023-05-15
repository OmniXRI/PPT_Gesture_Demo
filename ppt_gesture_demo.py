"""
# ppt_gesture_demo.py
#
# 利用網路攝影機作為影像輸入裝置，並採用 MediaPipe 的手勢辨識套件來偵測控制播放的手勢，最後使用 PyAutoGUI 來控制滑鼠、鍵盤，取代簡報遙控器播放簡報。
# 
# 作者：Jack OmniXRI, 2023/05/15
#
# Google MediaPipe 手勢辨識參考資料： https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer/python
# Google MediaPipe 手勢辨識 Colab 參考範例程式： https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/gesture_recognizer/python/gesture_recognizer.ipynb
# PyAutoGui 參考範例程式： https://pyautogui.readthedocs.io/en/latest/index.html
#
# 本範例使用前請先自行下載手勢辨識模型檔案，並將其和本程式放在同一路徑下運行。
# https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task
#
# 本範例運行前請先安裝好 Python, PIP，創建好虛擬環境，啟動後，再安裝 MediaPipe, PyAutoGui，如下所示。
# 1. 切換到想要工作的磁碟 x (可略過，可直接使用啟動命令列模式時的路徑)
x:
# 2. 建立Python虛擬環境
python -m venv mediapipe_env
# 3. 啟動Python虛擬環境
mediapipe_env\Scripts\activate
# 進入後命令列提示會變成 (mediapipe_env) x:\
# 4. 安裝Mediapipe (已包含numpy, matplotlib, opencv-contrib_python等)，可忽略版本設定（==0.10.0)則會安裝最新版本。
pip install -q mediapipe==0.10.0
# 5. 安裝PyAutoGui （處理鍵盤輸入及訊息輸出）
pip install pyautogui
"""

# 運行手勢辨識推論及可視化結果，這裡使用逐幀影格辨識，而非使用回調(callback)函式處理。

# 引入必要函式庫
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from matplotlib import pyplot as plt
import cv2 # 引入 OpenCV 函式庫
import numpy # 引入numpy函式庫
import pyautogui as ag # 引入PyAutoGui函式庫

# 宣告繪製手勢相關物件
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# 定義顯示手勢及手部特徵點函式 display_gesture_and_hand_landmarks
# 輸入原始影像、手勢及手部特徵點資料
# 輸出繪製好手部特徵點及連結之影像及手勢名稱
def display_gesture_and_hand_landmarks(images, gestures, hand_landmarks):
    image = images.numpy_view()  # 將numpy格式影像轉回opencv格式影像
    top_gestures = [gestures for gestures in gestures] # 取得手勢資料陣列
    hand_landmarks_list = [hand_landmarks for hand_landmarks in hand_landmarks] # 取得手部21個特徵點資料
 
    title = '' # 存放手勢名稱及置信度字串
    gesture_name = '' #存放手勢名稱

    # 若手勢內容不空則產生「手勢名稱加置信度」字串
    if numpy.size(top_gestures) != 0:
      gesture_name = top_gestures[0][0].category_name
      gesture_score = top_gestures[0][0].score
      title = f"{gesture_name}({gesture_score:.2f})"

    annotated_image = image.copy() # 複製一份影像再開始繪製內容
    
    # 若手部特徵點座標不空則繪製點及線於影像上
    if numpy.size(hand_landmarks_list) != 0:
      # 逐點繪製手部特徵點及連結線段
      for hand_landmarks in hand_landmarks_list:
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])

        mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks_proto,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    
    # 繪製手勢名稱及置信度字串到影像左上角
    cv2.putText(annotated_image, f"{title}",
                (20, 30), cv2.FONT_HERSHEY_DUPLEX,
                1, (0, 0, 255), 1, cv2.LINE_AA)

    # 回傳結果影像及手勢名稱
    return annotated_image, gesture_name 

# 先開啟Power Point 並最大化等待啟動（F5鍵）及操作命令
# 令滑鼠移到Power Point視窗位置並點擊
ag.moveTo(960, 10, 1)
ag.click()
ag.press('f5')

# 宣告手勢辨識器及初使化相關參數
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

# 開啟網路攝影機擷取影像
cap = cv2.VideoCapture(0) 

# 開始連續取像並推論及控制簡報播放
while(True): 
    # 從網路攝影機擷取一張影像
    ret, frame = cap.read()

    # 轉換影像格式以滿足 MediaPipe 
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
  
    # 進行手勢辨識並取得手勢及手部特徵資料
    recognition_result = recognizer.recognize(mp_image) 
    top_gesture = recognition_result.gestures
    hand_landmarks = recognition_result.hand_landmarks

    # 呼叫顯示手勢及手部特徵點函式並取得結果影像及手勢名稱
    annotated_image, gesture_name = display_gesture_and_hand_landmarks(mp_image, top_gesture, hand_landmarks)
    cv2.imshow('frame', annotated_image)

    # 若偵測到「打開手掌」手勢則模擬「Page Down」按鍵按下，令簡報往下一頁播放。
    # 模擬按鍵按下後，等待1秒，再繼續偵測手勢，以免重覆觸發。
    # 這裡的手勢可換成其它手勢，如 "Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up", "Victory"等。
    if gesture_name == "Open_Palm":
      ag.press('pagedown')
      ag.PAUSE = 1
     
    # 當按下 q 或 ESC 鍵則離開迴圈
    key = cv2.waitKey(1)

    if key == ord('q') or key == 27:
        break

# 釋放網路攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()