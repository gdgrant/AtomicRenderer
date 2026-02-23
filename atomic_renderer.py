import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageColor


### Objective: Take a list of points (x, y, c) plus a set of pre-processing and post-processing functions, and output a rendered image
### Pre-processing functions take a list of points
### Post-processing array functions take a numpy [RES_X, RES_Y, 3] array
### Post-processing image functions take a PIL image
### The final image should act like a 3-channel histogram



def make_colormap_from_four_hex(hex_a, hex_b, hex_c, hex_d):

	rgb_a = np.array(ImageColor.getcolor(hex_a, 'RGB'))[np.newaxis,:]/256
	rgb_b = np.array(ImageColor.getcolor(hex_b, 'RGB'))[np.newaxis,:]/256
	rgb_c = np.array(ImageColor.getcolor(hex_c, 'RGB'))[np.newaxis,:]/128
	rgb_d = np.array(ImageColor.getcolor(hex_d, 'RGB'))[np.newaxis,:]/128


	def color_applicator(cs):
		# Takes an array [N] of color coordinates, returns an array [Nx3] of RGB values

		cs = cs[:,np.newaxis]

		cs = rgb_a + (1-rgb_b) * np.cos(2*np.pi*(rgb_c * cs + rgb_d))
		cs = np.sqrt(np.square(cs) + 1e-3)
		cs = np.clip(cs, 0,1)

		return cs

	return color_applicator


def normalize(x):
	return (x-x.min())/(x.max()-x.min())


class AtomicRenderer:

	def __init__(self, img_size, margin=0.1):

		assert len(img_size) == 2
		assert margin >= 0
		assert margin < 0.4

		self.img_size = img_size
		self.img_array = np.zeros([*self.img_size,3])

		self.margin = margin

		self.img = None
		self.xs  = None
		self.ys  = None
		self.zs  = None
		self.cs  = None


	def make_diagnostic_array(self):

		self.img_array[:10,:10,0] = 1 	# Upper left = red
		self.img_array[:10,-10:,1] = 1  # Lower left = green
		self.img_array[-10:,:10,2] = 1  # Upper right = blue
		self.img_array[-10:,-10:,:] = 1 # Lower right = white


	def get_image_transposed_array(self):
		return np.transpose(self.img_array, (1,0,2))


	def plot_image_array(self):

		fig, ax = plt.subplots(1, 1, figsize=(6,4))
		im = ax.imshow(self.get_image_transposed_array(), aspect='equal')
		ax.set_axis_off()
		plt.tight_layout()
		plt.show()


	def convert_array_to_image(self):

		self.img = Image.fromarray((255*self.get_image_transposed_array()).astype(np.uint8))


	def show_image(self):

		self.img.show()


	def load_points_into_renderer(self, xs, ys, cs, colors_are_rgb=False):

		self.colors_are_rgb = colors_are_rgb

		self.xs = np.array(xs)
		self.ys = np.array(ys)
		self.cs = np.array(cs)


	def normalize_points(self):

		delta_x = self.xs.max() - self.xs.min()
		delta_y = self.ys.max() - self.ys.min()

		if delta_x < 1e-6 or delta_y < 1e-6 or np.isnan(self.xs.max()) or np.isnan(self.ys.max()):
			raise Exception('\n\nSimulation parameters are unstable.  Change parameters and try again.')

		xy_aspect = delta_x / delta_y

		if xy_aspect >= 1:
			x_aspect_adjust = 1
			y_aspect_adjust = 1/xy_aspect
		else:
			x_aspect_adjust = xy_aspect
			y_aspect_adjust = 1

		image_area_size = 1 - 2*self.margin

		self.xs = image_area_size * (normalize(self.xs) - 0.5) * x_aspect_adjust
		self.ys = image_area_size * (normalize(self.ys) - 0.5) * y_aspect_adjust

		if not self.colors_are_rgb:
			self.cs = normalize(self.cs)


	def apply_color_mapping(self, func):
		self.cs = func(self.cs)
		self.colors_are_rgb = True


	def apply_preprocessing_function(self, func, *args, **kwargs):

		self.xs, self.ys, self.cs = func(self.xs, self.ys, self.cs, *args, **kwargs)


	def apply_postprocessing_function(self, func, *args, **kwargs):

		self.img_array = func(self.img_array, *args, **kwargs)


	def load_points_into_array(self):

		# Obtain image size info
		w = self.img_size[0]
		h = self.img_size[1]
		r = w/h

		for x, y, c in zip(self.xs, self.ys, self.cs):

			if r < 1:
				rx = 1
				ry = r
			else:
				rx = 1/r
				ry = 1

			# Make pixel location
			try:
				pw = int(w*x*rx + w/2)
				ph = int(h*y*ry + h/2)
			except ValueError:
				raise Exception('\n\nSimulation parameters are unstable.  Change parameters and try again.')

			# Clip pixels to be in-bounds
			pw = np.clip(pw, 0, w-1)
			ph = np.clip(ph, 0, h-1)

			# Add color entry to pixel
			self.img_array[pw,ph] += c

		# Clip pixel values to be positive
		self.img_array = np.clip(self.img_array, 0, np.inf)


def postprocess_apply_gamma(array, gamma=0.5):
	return np.power(array, gamma)


def postprocess_normalize_colors_per_pixel(array):
	return array / np.amax(array, (0,1), keepdims=True)


def postprocess_normalize_color_by_total_max(array):
	return array / array.max()


def postprocess_make_negative(array):
	return 1 - array


postprocessors = {
	'apply_gamma'						: postprocess_apply_gamma,
	'normalize_color_per_pixel'			: postprocess_normalize_colors_per_pixel,
	'normalize_color_by_total_max'		: postprocess_normalize_color_by_total_max,
	'make_negative'						: postprocess_make_negative,
}
