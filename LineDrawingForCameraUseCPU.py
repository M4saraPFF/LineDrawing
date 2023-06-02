import cv2
import numpy as np
import tkinter

# カメラを取得
# 0→外付けWebカメラ
# 2→OBS仮想カメラ
Camera = cv2.VideoCapture(0)

# カーネルの定義(フィルタの定義)
kernel = np.array([[0, -1, 0], 
                   [-1, 4, -1], 
                   [0, -1, 0]], np.uint8)

# キー入力で終了することを表示
print("Push On The Key To End")

# カメラが検出できた場合
if Camera:
	Num, frame = Camera.read()
	print(frame.shape)
	# 撮影中(1フレームずつ取得)
	while True:
		# フレームを取得
		Num, frame = Camera.read()
	
		# グレースケール変換
		GrayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# グレースケール画像を膨張処理
		Processingimg = cv2.dilate(GrayFrame, kernel, iterations = 2)
		# グレースケール画像と膨張処理後画像の差分取得
		GrayFrame = Processingimg - GrayFrame
		# 白黒反転
		GrayFrame = cv2.bitwise_not(GrayFrame)
	
		# フレームを画面に表示
		cv2.imshow("LineDrawingForCamera", GrayFrame)
	
		# キー入力で終了(cv2.waitKey()は入力無しで-1)
		if cv2.waitKey(1) != -1:
			break

# カメラが検出できなかった場合
else:
	print("Not Found Camera, This PC")
	
	# 無限ループ
	while True:
		# キー入力で終了(cv2.waitKey()は入力無しで-1)
		if cv2.waitKey(1) != -1:
			break

# カメラとウィンドウを終了
Camera.release()
cv2.destroyAllWindows()