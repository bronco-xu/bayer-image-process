import cv2 as cv
import numpy as np
from PIL import Image

def cvt(image,clip_hist_percent):
	image = np.array(image,dtype = np.uint8)
	dst = cv.cvtColor(image, cv.COLOR_BAYER_BG2BGR)
	r, g, b = cv.split(dst)
	r_avg = cv.mean(r)[0]
	g_avg = cv.mean(g)[0]
	b_avg = cv.mean(b)[0]

	# 求各个通道所占增益
	k = (r_avg + g_avg + b_avg) / 3
	kr = k / r_avg
	kg = k / g_avg
	kb = k / b_avg

	r = cv.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
	g = cv.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
	b = cv.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)

	balance_img = cv.merge([r, g, b])
	# auto_result, alpha, beta = bright.automatic_brightness_and_contrast(balance_img, clip_hist_percent=8)

	gray = cv.cvtColor(balance_img, cv.COLOR_BGR2GRAY)

	# Calculate grayscale histogram

	hist = cv.calcHist([gray], [0], None, [256], [0, 256])
	hist_size = len(hist)

	# Calculate cumulative distribution from the histogram
	accumulator = []
	accumulator.append(float(hist[0]))
	for index in range(1, hist_size):
		accumulator.append(accumulator[index - 1] + float(hist[index]))

	# Locate points to clip
	new = clip_hist_percent
	maximum = accumulator[-1]
	new *= (maximum / 100.0)
	new 		/= 2.0

	# Locate left cut
	minimum_gray = 0
	while accumulator[minimum_gray] < new:
		minimum_gray += 1

	# Locate right cut
	maximum_gray = hist_size - 1
	while accumulator[maximum_gray] >= (maximum - new):
		maximum_gray -= 1

	# Calculate alpha and beta values
	alpha = 255 / (maximum_gray - minimum_gray)
	beta = -minimum_gray * alpha
	auto_result = cv.convertScaleAbs(balance_img, alpha=alpha, beta=beta)
	# cv.imshow("1",auto_result)
	# cv.moveWindow("1", 800, 800)
	# cv.waitKey()
	# turn out
	# result = np.array(auto_result, dtype=np.uint8)
	r, g, b = cv.split(auto_result)
	print(r, g, b)
	return(r, g, b)



# 图片输入（数组）,例：
image = [[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55],[1,2,3,5,1,5,4,5,5,1,56,6,62,2,3,2,32,3,6,45,5,5,5,2,2,6,54,6,55,55,55,66,33,11,22,22,65,56,66,22,11,55,22,35,45,33,55]]
# 调节亮度，例：
clip_hist_percent = 8
# 运行函数，例：
cvt(image,clip_hist_percent)

