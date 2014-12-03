from Tkinter import *

from PIL import ImageTk
from PIL import Image

class Fullscreen_Window(object):

	def __init__(self):
		self.tk = Tk()

		image = Image.open("/home/blake/Desktop/2014-11-13.jpg")
		photo = ImageTk.PhotoImage(image)

		self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
		self.tk.configure(bg='black')
		self.frame = Frame(self.tk)
		self.state = False

		self.tk.bind("<F11>", self.toggle_fullscreen)
		self.tk.bind("<Escape>", self.end_fullscreen)
		w = Label(self.tk, image=photo, background='black',)
		w.pack()
		self.tk.mainloop()

	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.tk.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.tk.attributes("-fullscreen", False)
		return "break"

	def show_image(self):
		pass


if __name__ == '__main__':
	w = Fullscreen_Window()
