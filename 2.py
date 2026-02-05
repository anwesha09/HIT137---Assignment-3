import cv2
import os


# Class definition for image processing tasks
class ImageProcessor:
    # Constructor to initialize the image attribute
    def __init__(self, image_path=None):
        self.image = None
        if image_path:
            self.load_image(image_path)

    # Image loading function
    def load_image(self, path):
        self.image = cv2.imread(path)
        return self.image is not None

    # Function to convert image to grayscale
    def convert_to_grayscale(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Function to apply Gaussian Blur to the image
    def apply_gaussian_blur(self, frame, intensity):
        # Kernel must be odd
        k = int(intensity) if int(intensity) % 2 != 0 else int(intensity) + 1
        return cv2.GaussianBlur(frame, (k, k), 0)

    # Function to detect edges using Canny algorithm
    def detect_canny_edges(self, frame):
        return cv2.Canny(frame, 100, 200)

    # Function to adjust brightness and contrast
    def adjust_bc(self, frame, brightness=0, contrast=0):
        # Linear transform: f(x) = alpha * x + beta
        alpha = (contrast + 100) / 100.0
        beta = brightness
        return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Function to rotate image by fixed degrees
    def rotate_fixed(self, frame, degrees):
        mapping = {
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE,
        }
        return cv2.rotate(frame, mapping.get(degrees, cv2.ROTATE_90_CLOCKWISE))

    # Function to flip the image in specified direction
    def flip_image(self, frame, direction):
        # 1 = Horizontal, 0 = Vertical
        return cv2.flip(frame, direction)

    # Function to resize the image to specified width and height
    def resize_frame(self, frame, w, h):
        return cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)


# 1. Initialize the Class
proc = ImageProcessor()

file_path = "/Users/sumitmanandhar/Desktop/SYD06 - ASSIGNMENT1/Software Now/ASSIGNMENT3/Photo.png"

if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found. Please place an image in the folder.")

# 3. Load and Process
if proc.load_image(file_path):
    orig = proc.image

    # Applying the requested features
    gray = proc.convert_to_grayscale(orig)
    blur = proc.apply_gaussian_blur(orig, 25)
    edges = proc.detect_canny_edges(orig)
    bright = proc.adjust_bc(orig, brightness=40, contrast=20)
    rot = proc.rotate_fixed(orig, 90)
    flip = proc.flip_image(orig, 0)
    small = proc.resize_frame(orig, 400, 300)

    print(
        "1. Original Image \n 2. Grayscale \n 3. Blur \n 4. Edges \n 5. Brightness/Contrast \n 6. Rotated \n 7. Flipped \n 8. Resized"
    )
    num = input("Enter a number to continue...")

    # Show results using OpenCV's native GUI
    while num != "":
        if num not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Invalid input. Exiting.")
            break
        elif num == "1":
            cv2.imshow("Original", orig)
            cv2.waitKey(0)
        elif num == "2":
            cv2.imshow("Grayscale", gray)
            cv2.waitKey(0)
        elif num == "3":
            cv2.imshow("Blur", blur)
            cv2.waitKey(0)
        elif num == "4":
            cv2.imshow("Edges", edges)
            cv2.waitKey(0)
        elif num == "5":
            cv2.imshow("Brightness/Contrast", bright)
            cv2.waitKey(0)
        elif num == "6":
            cv2.imshow("Rotated", rot)
            cv2.waitKey(0)
        elif num == "7":
            cv2.imshow("Flipped", flip)
            cv2.waitKey(0)
        elif num == "8":
            cv2.imshow("Resized", small)
            cv2.waitKey(0)
        else:
            print("Failed to load image.")
            break
        num = input(
            "Enter a number to continue...\n (Press Enter without input to exit)\n "
        )
        print("Press any key on your keyboard to exit.")
    cv2.destroyAllWindows()
