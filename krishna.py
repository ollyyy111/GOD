import cv2 # type: ignore
import turtle
import numpy as np

# 1. Load Image
IMAGE_PATH = r"PASTE THE IMAGE PATH HERE" # Replace with your image path
image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Error: Could not load image file. Please verify the file path!")
    exit()

# Resize image to fit screen properly
height, width = image.shape[:2]
max_dim = 650
scale = max_dim / max(height, width)
new_w, new_h = int(width * scale), int(height * scale)
image = cv2.resize(image, (new_w, new_h))

# 2. Extract Edge Contours
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(blurred, 25, 85)

contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Filter out tiny noise artifacts
valid_contours = [c for c in contours if len(c) >= 3]

# SORT CONTOURS FROM BOTTOM TO TOP:
# Sort based on the maximum Y value (bottom-most point) of each contour line segment
valid_contours.sort(key=lambda c: np.max(c[:, 0, 1]), reverse=True)

# 3. Setup Turtle Window tuned for Cosmic/Solar Aesthetics
screen = turtle.Screen()
screen.setup(new_w + 100, new_h + 100)
screen.colormode(255)
screen.bgcolor("#04050c")  # Deep space dark background
screen.title("Bottom-to-Top Progressive Krishna Drawing")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.width(1.8)

x_offset = -new_w / 2
y_offset = new_h / 2

# 4. Animate Progressive Line Sketch (Bottom-to-Top)
step_counter = 0

for contour in valid_contours:
    # Lift pen and move to starting point of the stroke
    start_x, start_y = contour[0][0]
    pen.penup()
    pen.goto(start_x + x_offset, -start_y + y_offset)
    
    # Draw contour continuously along its points
    for point in contour:
        px_x, px_y = point[0]
        
        # Clamp bounds
        px_x = min(px_x, new_w - 1)
        px_y = min(px_y, new_h - 1)

        # Extract RGB from image with vibrancy boost for golden & blue hues
        b, g, r = image[px_y, px_x]
        r_boost = min(255, int(r * 1.25))
        g_boost = min(255, int(g * 1.20))
        b_boost = min(255, int(b * 1.15))

        pen.pencolor(r_boost, g_boost, b_boost)
        pen.pendown()
        pen.goto(px_x + x_offset, -px_y + y_offset)

        step_counter += 1

        # SPEED / FLOW CONTROL:
        # Refreshes every 25 points so strokes are visibly drawn in medium-paced sequence
        if step_counter % 25 == 0:
            screen.update()

screen.update()
print("Progressive bottom-to-top drawing completed!")
turtle.done()