
import threading
import Queue

from PIL import ImageTk
from PIL import Image

class get_photos(object):

	def __init__(self, max_w, max_h):

		self.max_w, self.max_h = max_w, max_h

		self.image_index = -1
		self.images = ['photos/%s.JPG' % x for x in  range(1, 11)]

		self.image_queue = Queue.Queue()

		self.image_dict = {}

	def thread_load_images(self):

		while True:
			try:
				image_location, image = self.image_queue.get_nowait()
				self.image_dict[image_location] = image
			except Queue.Empty:
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
		#check the queue for other images that we may have returned
		self.thread_load_images()

		#try to return the image if it's been pre-loaded:
		try:
			return self.image_dict[image_path]
		except KeyError:
			#load the image
			self.image_dict[image_path] = load_image(self.image_queue, image_path, self.max_w, self.max_h).run(True)

		return self.image_dict[image_path]

	def get_next(self):
		this_photo_index = self.get_next_index()
		self.preload(start_index=this_photo_index)

		return self.get_photo(self.images[this_photo_index])

	def get_previous(self):

		return self.get_photo(self.images[self.get_previous_index()])

	def preload(self, start_index, forward=True):
		preload_num = 4
		if forward:
			index_range = range(start_index + 1, min(start_index + preload_num + 1, len(self.images)))
		else:
			index_range = range(max(0, start_index - preload_num), start_index)

		for i in index_range:
			try:
				self.image_dict[self.images[i]]
			except KeyError:
				load_image(self.image_queue, self.images[i], self.max_w, self.max_h).start()

class load_image(threading.Thread):

	def __init__(self, return_queue, image_path, max_x, max_y):

		self.return_queue = return_queue
		self.image_path = image_path
		self.max_x = max_x
		self.max_y = max_y
		threading.Thread.__init__(self)

	def run(self, direct=False):

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