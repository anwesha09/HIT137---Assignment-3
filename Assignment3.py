import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import os


# --- Requirement 1: OOP Structure ---
class ImageData:
    # Constructor to initialize image data and encapsulate file path and dimensions
    def __init__(self, path):
        self.__file_path = path
        self.cv_img = cv2.imread(path)
        self.__width = self.cv_img.shape[1]
        self.__height = self.cv_img.shape[0]

    # Getters for encapsulated attributes
    def get_path(self):
        return self.__file_path

    # Width and Height getters for status bar display
    def get_dimensions(self):
        return self.__width, self.__height


# --- Requirement 2: Image Processor (OpenCV Logic) ---
class ImageProcessor:
    def convert_to_grayscale(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def apply_gaussian_blur(self, frame, intensity):
        k = int(intensity) if int(intensity) % 2 != 0 else int(intensity) + 1
        return cv2.GaussianBlur(frame, (k, k), 0)

    def detect_canny_edges(self, frame):
        return cv2.Canny(frame, 100, 200)

    def rotate_fixed(self, frame, degrees):
        mapping = {
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE,
        }
        return cv2.rotate(frame, mapping.get(degrees, cv2.ROTATE_90_CLOCKWISE))

    def flip_image(self, frame, direction):
        return cv2.flip(frame, direction)


# --- Requirement 3: GUI Application ---
class ImageEditorApp:
    def __init__(self, root):
        # Basic window setup
        self.root = root
        self.root.title("Image Editor - Tkinter Project")
        self.root.geometry("950x600")

        # Variables to store the current image and history for undo/redo
        self.processor = ImageProcessor()
        self.image_data = None
        self.current_frame = None
        self.undo_stack = []

        # Build the interface
        self.create_menu()
        self.create_main_layout()
        self.create_status_bar()

    # ---------------- MENU BAR ----------------
    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo_action)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menu_bar)

    # ---------------- MAIN LAYOUT ----------------
    def create_main_layout(self):
        # Canvas for image display and a control panel on the right
        self.canvas = tk.Canvas(self.root, bg="#dcdcdc")
        self.canvas.pack(side="left", fill="both", expand=True)

        control_panel = tk.Frame(self.root, width=220, bg="#f2f2f2")
        control_panel.pack(side="right", fill="y")
        # Control Panel Title
        tk.Label(
            control_panel, text="Controls", font=("Arial", 12, "bold"), bg="#f2f2f2"
        ).pack(pady=10)

        # Buttons for OpenCV Functions
        ttk.Button(control_panel, text="Grayscale", command=self.btn_grayscale).pack(
            fill="x", padx=5, pady=2
        )
        ttk.Button(control_panel, text="Canny Edges", command=self.btn_edges).pack(
            fill="x", padx=5, pady=2
        )
        ttk.Button(control_panel, text="Flip Horizontal", command=self.btn_flip).pack(
            fill="x", padx=5, pady=2
        )
        ttk.Button(control_panel, text="Rotate 90", command=self.btn_rotate).pack(
            fill="x", padx=5, pady=2
        )

        tk.Label(control_panel, text="Blur Intensity", bg="#f2f2f2").pack(pady=(10, 0))
        self.blur_val = tk.IntVar(value=5)
        self.blur_slider = ttk.Scale(
            control_panel, from_=1, to=51, variable=self.blur_val
        )
        self.blur_slider.pack(fill="x", padx=5)
        # Blur button
        ttk.Button(control_panel, text="Apply Blur", command=self.btn_blur).pack(
            fill="x", padx=5, pady=5
        )

        ttk.Button(control_panel, text="Undo", command=self.undo_action).pack(
            fill="x", padx=5, pady=20
        )

    # ---------------- STATUS BAR ----------------
    def create_status_bar(self):
        self.status_bar = tk.Label(
            self.root, text="No image loaded", bd=1, relief="sunken", anchor="w"
        )
        self.status_bar.pack(side="bottom", fill="x")

    # ---------------- FUNCTIONALITY ----------------
    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp")])
        if path:
            self.image_data = ImageData(path)
            self.current_frame = self.image_data.cv_img.copy()
            self.undo_stack = [self.current_frame.copy()]
            self.display_image()
            self.update_status()

    # Display the current image on the canvas
    def display_image(self):
        if self.current_frame is None:
            return

        # Convert OpenCV BGR to RGB for Tkinter
        if len(self.current_frame.shape) == 2:  # Grayscale
            rgb_img = cv2.cvtColor(self.current_frame, cv2.COLOR_GRAY2RGB)
        else:
            rgb_img = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)

        # Resize image to fit canvas while maintaining aspect ratio
        img = Image.fromarray(rgb_img)
        img.thumbnail((700, 500))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(380, 280, image=self.tk_img)

    # Update the status bar with image info
    def update_status(self):
        if self.image_data:
            w, h = self.current_frame.shape[1], self.current_frame.shape[0]
            self.status_bar.config(
                text=f"{os.path.basename(self.image_data.get_path())} - {w}x{h}px"
            )

    # Save the current state for undo functionality
    def save_state(self):
        self.undo_stack.append(self.current_frame.copy())

    # --- Button Logic (Bridge to Requirement 2) ---

    # Function to handle Grayscale button click
    def btn_grayscale(self):
        if self.current_frame is not None:
            self.save_state()
            self.current_frame = self.processor.convert_to_grayscale(self.current_frame)
            self.display_image()

    # Function to handle Canny Edges button click
    def btn_edges(self):
        if self.current_frame is not None:
            self.save_state()
            self.current_frame = self.processor.detect_canny_edges(self.current_frame)
            self.display_image()

    # Function to handle Flip button click
    def btn_flip(self):
        if self.current_frame is not None:
            self.save_state()
            self.current_frame = self.processor.flip_image(self.current_frame, 1)
            self.display_image()

    # Function to handle Rotate button click
    def btn_rotate(self):
        if self.current_frame is not None:
            self.save_state()
            self.current_frame = self.processor.rotate_fixed(self.current_frame, 90)
            self.display_image()

    # Function to handle Blur button click
    def btn_blur(self):
        if self.current_frame is not None:
            self.save_state()
            self.current_frame = self.processor.apply_gaussian_blur(
                self.current_frame, self.blur_val.get()
            )
            self.display_image()

    # --- Additional Functionalities for Undo/Redo and Save ---
    def undo_action(self):
        if len(self.undo_stack) > 1:
            self.undo_stack.pop()
            self.current_frame = self.undo_stack[-1].copy()
            self.display_image()

    def save_image(self):
        if self.current_frame is not None:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                cv2.imwrite(path, self.current_frame)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
