# Import packages
import cv2
import pickle
# Lists to store the bounding box coordinates
top_left_corner=[]
bottom_right_corner=[]

# function which will be called on mouse input
def drawRectangle(action, x, y, flags, *userdata):
  # Referencing global variables 
  global top_left_corner, bottom_right_corner
  # Mark the top left corner when left mouse button is pressed
  if action == cv2.EVENT_LBUTTONDOWN:
    top_left_corner.append((x,y))
    # When left mouse button is released, mark bottom right corner
  elif action == cv2.EVENT_LBUTTONUP:
    bottom_right_corner.append((x,y))
    # Draw the rectangle
    cv2.rectangle(image, top_left_corner[-1], bottom_right_corner[-1], (0,255,0),2, 8)
    cv2.imshow("Window",image)

# Read Images
image = cv2.imread("car_test_img.png")
image = cv2.resize(image, (1280,720), interpolation = cv2.INTER_AREA)

# Make a temporary image, will be useful to clear the drawing
temp = image.copy()
# Create a named window
cv2.namedWindow("Window")
# highgui function called when mouse events occur
cv2.setMouseCallback("Window", drawRectangle)

k=0
# Close the window when key q is pressed
while k!=113:
  # Display the image
  cv2.imshow("Window", image)
  k = cv2.waitKey(0)
  # If c is pressed, clear the window, using the dummy image
  if (k == 99):
    image= temp.copy()
    cv2.imshow("Window", image)

# print(top_left_corner, bottom_right_corner)
with open('CarParkPos', 'wb') as f:
    pickle.dump(top_left_corner,f)
    pickle.dump(bottom_right_corner,f)

cv2.destroyAllWindows()