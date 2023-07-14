# インポート
import numpy as np
import cv2
import sys
import os
import ffmpeg
import moviepy.editor as mp


# パス、動画名指定
path = "C:/Users/masar/Desktop/Program/Python/Img" + "/"
mviname = "Ado_utakatararabai"

# 拡張子付きの変数を生成
extension_mviname = mviname + ".mp4"

# 動画ファイル読み込み(動画用)
mvi = cv2.VideoCapture(path + extension_mviname)
# 動画ファイル読み込み(音声用)
audio = ffmpeg.input(path + extension_mviname)
stream = ffmpeg.output(audio, path + mviname + ".mp3")

# 動画ファイルを正常に読み込めたか判定
if not mvi.isOpened():
	print("Faild to Load File")
	sys.exit()
else:
	print("Complete to Load File")

# 幅と高さを取得
width = int(mvi.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(mvi.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)

#フレームレートを取得
frame_rate = float(mvi.get(cv2.CAP_PROP_FPS))

# 元動画と同じサイズのケースを作成
fmt = cv2.VideoWriter_fourcc("m", "p", "4", "v")
writer = cv2.VideoWriter(path + mviname + "_LineDrawing_OneTime.mp4", fmt, frame_rate, size, isColor = False)

# カウント用変数
num = 0
# 次のフレームが存在するか判定
bimg = True

# 全フレームを対象に処理
while bimg:
	# 現在のフレーム情報を取得(存在するか、画像)
	bimg, img = mvi.read()
	# 存在する場合
	if bimg:
		# グレースケール変換(元動画はカラー)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# カーネルの定義(フィルタの定義)
		kernel = np.array([[0, -1, 0], 
		                   [-1, 4, -1], 
		                   [0, -1, 0]], np.uint8)

		# グレースケール画像を膨張処理
		processingimg = cv2.dilate(img, kernel, iterations = 2)

		# グレースケール画像と膨張処理後画像の差分取得
		img = processingimg - img

		# 色反転
		img = cv2.bitwise_not(img)
		
		# ケースに画像を差し込む
		writer.write(img)
		
	num = num + 1
	
writer.release()
mvi.release()

mvi_audio = mp.VideoFileClip(path + extension_mviname).subclip()
try:
	mvi_audio.audio.write_audiofile("0audio.mp3")
except AttributeError:
	clip = mp.VideoFileClip(path + mviname + "_LineDrawing_OneTime1.mp4").subclip()
	clip.write_videofile(path + mviname + "_LineDrawing1.mp4")
	
	clip = mp.VideoFileClip(path + mviname + "_LineDrawing_OneTime2.mp4").subclip()
	clip.write_videofile(path + mviname + "_LineDrawing2.mp4")
	
	os.remove(path + mviname + "_LineDrawing_OneTime1.mp4")
	os.remove(path + mviname + "_LineDrawing_OneTime2.mp4")

clip = mp.VideoFileClip(path + mviname + "_LineDrawing_OneTime1.mp4").subclip()
clip.write_videofile(path + mviname + "_LineDrawing1.mp4", audio = '0audio.mp3')

clip = mp.VideoFileClip(path + mviname + "_LineDrawing_OneTime2.mp4").subclip()
clip.write_videofile(path + mviname + "_LineDrawing2.mp4", audio = '0audio.mp3')

os.remove(path + mviname + "_LineDrawing_OneTime1.mp4")
os.remove(path + mviname + "_LineDrawing_OneTime2.mp4")