import cv2
import numpy as np

# function to resize and rescale video frame
def rescale_frames(frame,scale=0.70):
    width = int(frame.shape[0]*scale)
    height = int(frame.shape[1]*scale)
    
    dimension = (width,height)
    return cv2.resize(frame,dimension,interpolation=cv2.INTER_AREA)



image= cv2.imread('C:/Users/amitk/Desktop/University-answer-booklet-eval-dash/New folder/testImage.jpg')

original_image= image
gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edges= cv2.Canny(gray, 50,200)
contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

cv2.destroyAllWindows()

def get_contour_areas(contours):
    all_areas= []
    for cnt in contours:
        area= cv2.contourArea(cnt)
        all_areas.append(area)
    return all_areas


sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
largest_item= sorted_contours[0]

cv2.drawContours(original_image, largest_item, -1, (255,0,0),10)

largestContourArea = 0
largestContour = 0
for cnt in contours:
    contourArea = cv2.contourArea(cnt)
    if( contourArea > largestContourArea):
        largestContour = cnt
        largestContourArea = contourArea

# x,y are the co-ordinates of left-top point and w,h are width and height respectively
x,y,w,h = cv2.boundingRect(largestContour)

# This is simple slicing to get the "Region of Interest"
ROI = original_image[y:y+h,x:x+w]


# Convert to grayscale.
gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
  
# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))
  
# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
               param2 = 30, minRadius = 1, maxRadius = 40)
  
# Draw circles that are detected.
if detected_circles is not None:
  
    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))
  
    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
  
        # Draw the circumference of the circle.
        cv2.circle(ROI, (a, b), r, (0, 255, 0), 2)     


cv2.imshow("Detected Circles in OMR", ROI)
cv2.waitKey(0)
cv2.destroyAllWindows()