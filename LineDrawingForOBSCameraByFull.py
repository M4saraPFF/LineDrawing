import cv2
import cupy
import numpy as np
import cupy as cp
import win32gui
import win32con

# カメラを取得
# 0→外付けWebカメラ
# 2→OBS仮想カメラ
Camera = cv2.VideoCapture(2)

WindowWidth = 1920
WindowHeight = 1080

# カメラ解像度をリサイズ
Camera.set(cv2.CAP_PROP_FRAME_WIDTH, WindowWidth)
Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, WindowHeight)

# win32guiの設定
cv2.namedWindow("LineDrawingForCamera")
WindowName = win32gui.FindWindow(None, "LineDrawingForCamera")
win32gui.SetWindowLong(WindowName, win32con.GWL_STYLE, win32con.WS_POPUP)

# カーネルの定義(フィルタの定義)
kernel = np.array([[0, -1, 0], 
                   [-1, 4, -1], 
                   [0, -1, 0]], np.uint8)

# キー入力で終了することを表示
print("Push On The Key To End")

# カメラが検出できた場合
if Camera:
	# 解像度等を出力
	ret, frame = Camera.read()
	ZeroArray = np.zeros((frame.shape[0], frame.shape[1], 3))
	print(frame.shape, ZeroArray.shape)
	
	# 撮影中(1フレームずつ取得)
	while True:
		# フレームを取得
		Num, frame = Camera.read()
		
		# グレースケール変換
		GrayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# GPUメモリにデータを送信
		GrayImgOfGPU = cp.asarray(GrayFrame)
		
		# グレースケール画像を膨張処理/収縮処理
		PadImage = cp.pad(GrayImgOfGPU, 1, "edge")
		ProcessingImg = cp.lib.stride_tricks.as_strided(PadImage, GrayImgOfGPU.shape + (3, 3), PadImage.strides * 2)
		
		# 膨張処理画像と収縮処理画像の差分取得
		imgOfGPU = GrayImgOfGPU - cp.min(ProcessingImg, axis=(2, 3))
		
		# GPUから計算後の数値を取得
		img = imgOfGPU.get()
		
		# 白黒反転
		img = cv2.bitwise_not(img)
		
		# フレームを画面に表示
		cv2.imshow("LineDrawingForCamera", img)
		win32gui.SetWindowPos(WindowName, win32con.HWND_TOPMOST, 0, 0, WindowWidth, WindowHeight, win32con.SWP_SHOWWINDOW)
		
		# キー入力で終了(cv2.waitKey()は入力無しで-1)
		if cv2.waitKey(1) != -1:
			break

# カメラが検出できなかった場合
else:
	print("Not Found Camera, This PC")
	
	input()

# カメラとウィンドウを終了
Camera.release()
cv2.destroyAllWindows()