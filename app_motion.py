from Tkinter import *

import random
import get_photos


class MyApp(Tk):
	def __init__(self):

		Tk.__init__(self)


		#self.attributes('-zoomed', True)
		self.configure(bg='black')
		self.attributes("-fullscreen", True)
		self.configure(cursor="none")

		self.move_counter = 0


		self.play_show = True
		self.screen_width = self.winfo_screenwidth()
		self.screen_height = self.winfo_screenheight()
		self.photo = None
		self.screen_width, self.screen_height = (1920 + 100, 1080 + 100)


		self.photos = get_photos.get_photos(max_w=self.screen_width, max_h=self.screen_height)

		#self.w = Label(self, background='black')

		self.w = Canvas(self, width=self.screen_width, height=self.screen_height, background='black', highlightthickness=0)
		self.l = Label(self.w, background='black')

		self.l.pack(expand=True, fill="both")


		self.bind("<Escape>", self.quit)

		self.bind("s", self.start_stop_show)
		self.bind("<space>", self.start_stop_show)

		self.bind("<Left>", self.previous_photo)
		self.bind("<Right>", self.next_photo)

		self.bind('q', self.quit)

		self.show()

	def quit(self, event=None):
		self.destroy()

	def start_stop_show(self, event=None):
		if self.play_show:
			self.play_show = False
		else:
			self.play_show = True
			self.show()

	def previous_photo(self, event=None):

		self.play_show = False
		self.display_photo(self.photos.get_previous())

	def next_photo(self, event=None):

		self.play_show = False
		self.display_photo(self.photos.get_next())

	def display_photo(self, photo):
		#anchor = self.get_random_anchor()

		#self.w.pack(expand=True, fill="both")
		#if self.photo:
		#	self.w.delete(self.photo)

		#self.photo = self.w.create_image(anchor[1][0], anchor[1][1] , image=photo, anchor=anchor[0])



		self.l.configure(image=photo, anchor=self.get_random_anchor())
		self.l.pack()

		self.w.pack()
		self.move_counter = 0
		self.x_pos = bool(random.getrandbits(1))
		self.y_pos = bool(random.getrandbits(1))

		self.move_widget()

	def get_random_anchor(self):

		anchors = ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw', 'center']
		return anchors[random.randint(0, len(anchors) - 1)]

	def get_random_anchor2(self):

		w = self.screen_width - 50
		h = self.screen_height - 50
		half_w = w / 2
		half_h = h / 2
		return ('center', (half_w, half_h))

		#anchors = [('n', (half_w, -50)), ('e', (w, half_h)), ('s', (half_w, h)), ('w', (-50, half_h)), ('center', (half_w, half_h))]
		#return anchors[random.randint(0, len(anchors) - 1)]

	def move_widget(self):

		if self.play_show:
			self.move_counter += 1
			x = 1 if self.x_pos else -1
			y = 1 if self.y_pos else -1
			self.w.move(self.l, x, y)
			self.move_counter += 1
			self.after(500, self.move_widget)

	def show(self):

		if self.play_show:
			self.display_photo(self.photos.get_next())
			self.after(5000, self.show)




if __name__ == "__main__":
	root = MyApp()
	root.mainloop()
