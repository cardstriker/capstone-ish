import tkinter as tk
import time
import ImgToTxtApplication

app = ImgToTxtApplication.ImgToTxtApp()

frame = tk.Tk()
frame.title("URL Reader")
frame.geometry('300x400')

def readInput():
    result_string_var.set("Processing... Please Wait...")
    urlInput = inputtxt.get("1.0",'end-1c')
    result = app.setURL(urlInput)
    print(result)
    if result == False:
        result_string_var.set("The provided URL is Invalid")
    else:
        result_string_var.set('The provided URL is Valid\nNumber of hyperlinks: ' + str(len(result[0][0])) + '\nNumber of Website path: ' + str(len(result[0][1])) + '\nNumber of images: ' + str(len(result[1])) + '\nNumber of other multimedia: ' + str(len(result[2][0])+len(result[2][1])))

inputtxt = tk.Text(frame, height = 4, width = 25)
inputtxt.pack()

printButton = tk.Button(frame, text = "Read file", command = readInput)
printButton.pack()

result_string_var = tk.StringVar()

lbl = tk.Label(frame, textvariable = result_string_var)
lbl.pack()

frame.mainloop()