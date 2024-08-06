import cv2

# Load the image
image = cv2.imread('image.jpg')
startX, startY = 50, 50
endX, endY = 200, 200
cropped_image = image[startY:endY, startX:endX]
cv2.imshow('Resized Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
