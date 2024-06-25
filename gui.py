#Importing necessary Libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import numpy
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
from tkinter import Label
from keras.models import load_model

# Loading the Model
model = load_model('Age_Sex_Detection.keras')

# Function to reduce the opacity of an image
def reduce_opacity(img, opacity):
    assert opacity >= 0 and opacity <= 1
    alpha = img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    img.putalpha(alpha)
    return img

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title("Age & Gender Detector")
top.configure(background='#E0E3FF')

# Load and process the background image
bg_image = Image.open(r"C:\Users\vivek\OneDrive\Desktop\AGE GENDER DETECTOR\Age.jpg").convert("RGBA")
bg_image = bg_image.resize((800, 600), Image.LANCZOS)
bg_image = reduce_opacity(bg_image, 0.6)  # Adjust opacity (0.0 to 1.0)
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Create a label for the background image
bg_label = Label(top, image=bg_image_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Initializing the labels (1 for Age and 2 for Sex)
label1 = Label(top, background="#00004d", font=('arial', 15, "bold"))
label2 = Label(top, background="#00004d", font=('arial', 15, "bold"))
sign_image = Label(top)

# Heading
heading = Label(top, text="  Age & Gender Detector  ", pady=20, font=('Times New Roman', 18, "bold"))
heading.configure(background="#99ebff", foreground="#00004d")
heading.pack(pady=(20, 0))

#Defining detect function which detects the age and gender of the person in image using the model
def Detect(file_path):
    global label_packed
    image=Image.open(file_path)
    image=image.resize((48,48))
    image=numpy.expand_dims(image,axis=0)
    image=np.array(image)
    image=np.delete(image,0,1)
    image=np.resize(image,(48,48,3))
    print(image.shape)
    sex_f=["Male","Female"]
    image=np.array([image])/255
    pred=model.predict(image)
    age=int(np.round(pred[1][0]))
    sex=int(np.round(pred[0][0]))
    print("Predicted Age is " + str(age))
    print("Predicted Gender is " + sex_f[sex])
    label1.configure(foreground="#FFFFFF",text=age)
    label2.configure(foreground="#FFFFFF",text=sex_f[sex])


# Defining Show_Detect function
def show_Detect_button(file_path):
    Detect_b=Button(top,text="Detect Image", command=lambda: Detect(file_path),padx=10,pady=5)
    Detect_b.configure(background="#99ebff", foreground="#00004d",font=("Times New Roman",10,"bold"))
    Detect_b.place(relx=0.79,rely=0.46)

#Defining Upload Image Function
def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image=im
        label1.configure(text="")
        label2.configure(text="")
        show_Detect_button(file_path)
    except Exception as e:
        print(e)
            

upload=Button(top,text="Upload an Image",command=upload_image,padx=10,pady=5)
upload.configure(background="#99ebff",foreground="#00004d",font=("Times New Roman",10,"bold"))
upload.pack(side="bottom",pady=50)
sign_image.pack(side="bottom",expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)



# Run the main loop
top.mainloop()
