import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from PIL import Image, ImageTk
from signature import match

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("Image Files", ".jpeg;.jpg;*.png"),
    ]))
    if filename:
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        messagebox.showerror("Error", "Camera could not be opened!")
        return False

    cv2.namedWindow("Capture Image")

    while True:
        ret, frame = cam.read()
        if not ret:
            messagebox.showerror("Error", "Failed to grab frame!")
            break
        cv2.imshow("Capture Image", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir('temp'):
                os.makedirs('temp', mode=0o777)
            img_name = f"./temp/test_img{sign}.png"
            cv2.imwrite(filename=img_name, img=frame)
            break

    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    filename = os.path.join(os.getcwd(), 'temp', f'test_img{sign}.png')
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        success = capture_image_from_cam_into_temp(sign=sign)
        if success:
            ent.delete(0, tk.END)
            ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    if not os.path.exists(path1):
        messagebox.showerror("Error", f"File not found: {path1}")
        return
    if not os.path.exists(path2):
        messagebox.showerror("Error", f"File not found: {path2}")
        return

    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure: Signatures Do Not Match",
                             f"Signatures are {result:.2f}% similar!")
    else:
        messagebox.showinfo("Success: Signatures Match",
                            f"Signatures are {result:.2f}% similar!")
    return True

root = tk.Tk()
root.title("Signature Matching")
root.geometry("600x700")

# Load background image
bg_image = Image.open("SplitShire-03692-1800x1200.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

style = ttk.Style()
style.configure('TLabel', background='black', foreground='white', font=("Helvetica", 12))
style.configure('Title.TLabel', background='black', foreground='white', font=("Helvetica", 16, 'bold'))
style.configure('Left.TLabel', background='black', foreground='white', font=("Helvetica", 14))

style.configure('Rounded.TButton', font=("Helvetica", 10), padding=6, relief="flat",
                borderwidth=1, focusthickness=3, focuscolor='none', background='light blue', foreground='black')
style.map('Rounded.TButton', background=[('active', 'gray'), ('!disabled', 'light blue')],
          relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
style.configure('Green.TButton', font=("Helvetica", 10), padding=6, relief="flat", background='green', foreground='black')
style.map('Green.TButton', background=[('active', 'dark green'), ('!disabled', 'green')],
          relief=[('pressed', 'sunken'), ('!pressed', 'flat')])

uname_label = ttk.Label(root, text="Compare Two Signatures:", style='Title.TLabel')
uname_label.place(relx=0.5, y=50, anchor=tk.CENTER)

img1_message = ttk.Label(root, text="Signature 1:", style='Left.TLabel')
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=("Helvetica", 10), width=50)
image1_path_entry.place(x=150, y=120)

img1_browse_button = ttk.Button(
    root, text="Browse", style='Rounded.TButton', command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=520, y=160)

img1_capture_button = ttk.Button(
    root, text="Capture", style='Rounded.TButton', command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=520, y=120)

img2_message = ttk.Label(root, text="Signature 2:", style='Left.TLabel')
img2_message.place(x=10, y=250)

image2_path_entry = tk.Entry(root, font=("Helvetica", 10), width=50)
image2_path_entry.place(x=150, y=240)

img2_browse_button = ttk.Button(
    root, text="Browse", style='Rounded.TButton', command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=520, y=280)

img2_capture_button = ttk.Button(
    root, text="Capture", style='Rounded.TButton', command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=520, y=240)

compare_button = ttk.Button(
    root, text="Compare", style='Green.TButton', command=lambda: checkSimilarity(window=root,
                                                          path1=image1_path_entry.get(),
                                                          path2=image2_path_entry.get()))
compare_button.place(x=250, y=340)

root.mainloop()