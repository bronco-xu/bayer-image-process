import cv2 as cv
import glob

def cvt(inputpath,clip_hist_percent):
	i = 0
	for jpgfile in glob.glob(inputpath+"/"+"*.bmp"):
		image = cv.imread(jpgfile, 0)
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
		cv.imwrite('E:/{}.png'.format(i), auto_result)
		i = i+1

inputpath = "E:/"
clip_hist_percent = 8    #调节亮度
cvt(inputpath,clip_hist_percent)

