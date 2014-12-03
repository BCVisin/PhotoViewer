from Tkinter import *

from PIL import ImageTk
from PIL import Image
import time
import threading
import random
import Queue
import random

from pprint import pprint

class MyApp(Tk):
	def __init__(self):

		Tk.__init__(self)


		self.attributes('-zoomed', True)
		self.configure(bg='black')
		self.state = True
		#self.attributes("-fullscreen", self.state)
		#self.configure(cursor="none")

		self.fr = Frame(self, background='black', cursor='none')
		self.fr.pack()
		self.play_show = True
		self.screen_width = self.winfo_screenwidth() + 100
		self.screen_height = self.winfo_screenheight() + 100

		self.photos = GetPhotos(max_w=self.screen_width, max_h=self.screen_height)

		self.w = Label(self, background='black')
		self.w.pack(expand=True, fill="both")

		self.bind("<F11>", self.toggle_fullscreen)
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

		self.w.configure(image=photo, anchor=self.get_random_anchor(), width=self.screen_width, height=self.screen_height)
		self.w.place(x=0, y=0)
		self.w.photo = photo
		#self.move_counter = 0
		#self.after(10, self.move_widget)

	def get_random_anchor(self):

		anchors = ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw', 'center']
		return anchors[random.randint(0, len(anchors) - 1)]

	def move_widget(self):
		if self.move_counter < 50:
			self.move_counter += 1
			x = 1
			y = 1
			self.w.place(x=self.w.winfo_x() + x, y=self.w.winfo_y() + y)
			self.move_counter += 1
			self.after(100, self.move_widget)
		else:
			self.move_counter = 0
			return


	def show(self):

		if self.play_show:
			self.display_photo(self.photos.get_next())
			self.after(5000, self.show)

	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.attributes("-fullscreen", False)
		return "break"


class GetPhotos(object):

	def __init__(self, max_w, max_h):

		self.max_w, self.max_h = max_w, max_h

		self.image_index = -1
		self.images = ['/home/blake/workspace/PhotoViewer/photos/%s.JPG' % x for x in  range(1, 11)]

		self.image_queue = Queue.Queue()

		self.image_dict = {}

	def thread_load_images(self):

		while True:
			try:
				image_location, image = self.image_queue.get_nowait()
				print 'loaded %s' % image_location
				self.image_dict[image_location] = image
			except Queue.Empty:
				print 'empty queue'
				break

	def get_next_index(self):

		if self.image_index >= len(self.images) - 1:
			self.image_index = 0
		else:
			self.image_index += 1

		return self.image_index

	def get_previous_index(self):
		if self.image_index <= 0:
			self.image_index = len(self.images) - 1
		else:
			self.image_index -= 1

		return self.image_index

	def get_photo(self, image_path):
		print 'get_photo'
		#check the queue for other images that we may have returned
		self.thread_load_images()

		#try to return the image if it's been pre-loaded:
		try:
			return self.image_dict[image_path]
		except KeyError:
			#load the image
			print 'directly loading the image'
			self.image_dict[image_path] = load_image(self.image_queue, image_path, self.max_w, self.max_h).run(True)

		return self.image_dict[image_path]

	def get_next(self):
		this_photo_index = self.get_next_index()
		print 'this_photo_index: %s' % this_photo_index
		self.preload(start_index=this_photo_index)

		return self.get_photo(self.images[this_photo_index])

	def get_previous(self):

		return self.get_photo(self.images[self.get_previous_index()])

	def preload(self, start_index, forward=True):
		print 'preload'
		preload_num = 4
		if forward:
			index_range = range(start_index + 1, min(start_index + preload_num + 1, len(self.images)))
		else:
			index_range = range(max(0, start_index - preload_num), start_index)

		print index_range

		for i in index_range:
			try:
				print 'Image in Cache'
				self.image_dict[self.images[i]]
			except KeyError:
				print 'preloading %s' % self.images[i]
				load_image(self.image_queue, self.images[i], self.max_w, self.max_h).start()

class load_image(threading.Thread):

	def __init__(self, return_queue, image_path, max_x, max_y):

		self.return_queue = return_queue
		self.image_path = image_path
		self.max_x = max_x
		self.max_y = max_y
		threading.Thread.__init__(self)

	def run(self, direct=False):
		print 'run'
		print self.image_path

		image = Image.open(self.image_path)
		new_size = self.get_new_size(self.max_x, self.max_y, image)
		resized_image = image.resize(new_size, Image.ANTIALIAS)
		final_image = ImageTk.PhotoImage(resized_image)
		if direct:
			return final_image
		else:
			self.return_queue.put((self.image_path, final_image))

	def get_new_size(self, max_width, max_height, image):

		x, y = image.size

		if x > max_width or x > y:
			y = int(max(y * max_width / x, 1))
			x = int(max_width)

		if y > max_height or  x < y:
			x = int(max(x * max_height / y, 1))
			y = int(max_height)
		new_size = x, y

		return new_size

if __name__ == "__main__":
	root = MyApp()
	root.mainloop()
