# made with the help of ChatGPT


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np

class ColoringBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coloring Book Creator")
        self.image = None

        # create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # create the file upload button
        self.file_button = tk.Button(self.main_frame, text="Upload Image", command=self.upload_image)
        self.file_button.pack()

        # create the edge detection slider
        self.canny_slider = tk.Scale(self.main_frame, label="Canny Edge Detection", from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_image)
        self.canny_slider.pack()

        # create the thresholding slider
        self.threshold_slider = tk.Scale(self.main_frame, label="Thresholding", from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_image)
        self.threshold_slider.pack()

        # create the dilation slider
        self.dilation_slider = tk.Scale(self.main_frame, label="Dilation", from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_image)
        self.dilation_slider.pack()

        # cerate the smoothing slider
        self.smoothing_slider = tk.Scale(self.main_frame, label="Smoothing", from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_image)
        self.smoothing_slider.pack()

        # create the contrast slider
        self.contrast_slider = tk.Scale(self.main_frame, label="Contrast", from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_image)
        # set to 50
        self.contrast_slider.set(50)
        self.contrast_slider.pack()

        # create the canvas to display the image
        self.canvas = tk.Canvas(self.main_frame, width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # create the save button
        self.save_button = tk.Button(self.main_frame, text="Save Image", command=self.save_image)
        self.save_button.pack()

    def upload_image(self):
        # open a file dialog to choose an image
        file_path = filedialog.askopenfilename()

        # load the image using OpenCV
        self.image = cv2.imread(file_path)

        # update the image in the canvas
        self.update_image()

    # def update_image(self, event=None):
    #     # apply the canny edge detection filter
    #     canny_edge = cv2.Canny(self.image, self.canny_slider.get(), self.threshold_slider.get())

    #     # apply the dilation filter
    #     kernel = np.ones((self.dilation_slider.get(), self.dilation_slider.get()), np.uint8)
    #     dilation = cv2.dilate(canny_edge, kernel, iterations=1)

    #     # convert the image to grayscale
    #     grayscale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    #     # adjust the contrast
    #     contrast = cv2.addWeighted(grayscale, self.contrast_slider.get() / 10, np.zeros_like(grayscale), 0, 0)

    #     # create the coloring book image
    #     coloring_book = cv2.subtract(contrast, dilation)

    #     # convert the coloring book image to RGB format
    #     coloring_book = cv2.cvtColor(coloring_book, cv2.COLOR_GRAY2RGB)

    #     img = cv2.resize(coloring_book, (self.canvas.winfo_width(), self.canvas.winfo_height()))
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     photo = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
    #     self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    #     self.canvas.photo = photo


    def update_image(self, event=None):
        # apply the canny edge detection filter
        canny_edge = cv2.Canny(self.image, self.canny_slider.get(), self.threshold_slider.get())

        # apply the dilation filter
        kernel = np.ones((self.dilation_slider.get(), self.dilation_slider.get()), np.uint8)
        dilation = cv2.dilate(canny_edge, kernel, iterations=1)

        # apply the smoothing filter
        kernel_size = self.smoothing_slider.get() * 2 + 1
        smoothing = cv2.GaussianBlur(self.image, (kernel_size, kernel_size), 0)

        # convert the image to grayscale
        grayscale = cv2.cvtColor(smoothing, cv2.COLOR_BGR2GRAY)

        # adjust the contrast
        contrast = cv2.addWeighted(grayscale, self.contrast_slider.get() / 10, np.zeros_like(grayscale), 0, 0)

        # create the coloring book image
        coloring_book = cv2.subtract(contrast, dilation)

        # convert the coloring book image to RGB format
        coloring_book = cv2.cvtColor(coloring_book, cv2.COLOR_GRAY2RGB)

        img = cv2.resize(coloring_book, (self.canvas.winfo_width(), self.canvas.winfo_height()))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        photo = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.photo = photo

        return img



    # def update_image(self, event=None):
    #     # convert the image to grayscale
    #     grayscale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    #     # adjust the contrast
    #     contrast = cv2.addWeighted(grayscale, self.contrast_slider.get() / 10, np.zeros_like(grayscale), 0, 0)

    #     # apply the canny edge detection filter
    #     canny_edge = cv2.Canny(contrast, self.canny_slider.get(), self.threshold_slider.get())

    #     # apply the dilation filter
    #     kernel = np.ones((self.dilation_slider.get(), self.dilation_slider.get()), np.uint8)
    #     dilation = cv2.dilate(canny_edge, kernel, iterations=1)

    #     # create the coloring book image
    #     coloring_book = cv2.subtract(contrast, dilation)

    #     # convert the coloring book image to RGB format
    #     coloring_book = cv2.cvtColor(coloring_book, cv2.COLOR_GRAY2RGB)

    #     img = cv2.resize(coloring_book, (self.canvas.winfo_width(), self.canvas.winfo_height()))
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     photo = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
    #     self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    #     self.canvas.photo = photo


    def save_image(self):
        if self.image is None:
            # if no image is uploaded yet, show a message box
            messagebox.showwarning("Warning", "Please upload an image first.")
        else:
            # open a file dialog to choose a save location and filename
            file_path = filedialog.asksaveasfilename(defaultextension=".png")

            # save the image
            cv2.imwrite(file_path, self.update_image())

            # show a message box to confirm the image is saved
            messagebox.showinfo("Image Saved", f"The image has been saved as {file_path}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColoringBookApp(root)
    root.mainloop()
