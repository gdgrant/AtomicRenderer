from atomic_renderer import AtomicRenderer, postprocessors, make_colormap_from_four_hex

from designs import circle, lorenz, sine_delay, burgers_map, aizawa, \
	popcorn, hourglass, henon, gingerbread, cat


# Note 1: Some of the included designs (e.g., sine delay) have a bit of randomness,
# so the design can change on sequential iterations without user input.

# Note 2: Some of the included designs (e.g., popcorn) have regions where instability
# is known, and so those regions are blocked off from the user (via exceptions).

# Note 3: Some of the included designs (e.g., burgers map) have stable regions that
# are challenging to find and stay within but are hard to identify a priori, so
# users may need to tweak input parameters a few times to get nice images.

# Note 4: Some of the included designs (e.g., gingerbread) are incredibly sensitive
# near the default parameters and prone to instability outside that range.  Experimentation
# with small changes is encouraged!

# Note 4: Sometimes the color option will rotate the design, sometimes it will just
# subtly change how the color operation is calculated.


##################
### Parameters ###
##################

# Image sizing
image_width  = 600
image_height = 600
image_margin = 0.1

# Other image setup (gamma default is 0.5 (or 0.3 for negatives); lower number means lower contrast)
gamma = 0.4
color_negative = False

# Color applicator hex codes (color is a bit of a misnomer - they're color-like control values)
base_color 		= '#0000FF'
reference_color	= '#5599BB'
cycling_color 	= '#AA4488'
bias_color 		= '#BB0099'

# Design setup - choose from the imported set of designs, then tweak the options for that design
# > lettered params are 0 to 1 (0.5=default), color options are {0,1,2}
design = lorenz
color_option = 1
A = 0.5
B = 0.5
C = 0.5


##################
### Processing ###
##################

img_size = (image_width, image_height)
AR = AtomicRenderer(img_size, image_margin)

try:
	xs, ys, cs = design(A, B, C, color_option)
except OverflowError:
	raise Exception('\n\nSimulation parameters are unstable.  Change parameters and try again.')

AR.load_points_into_renderer(xs, ys, cs)
AR.normalize_points()

color_applicator = make_colormap_from_four_hex(reference_color, base_color, cycling_color, bias_color)
AR.apply_color_mapping(color_applicator)
AR.load_points_into_array()

AR.apply_postprocessing_function(postprocessors['apply_gamma'], gamma)
AR.apply_postprocessing_function(postprocessors['normalize_color_per_pixel'])

if color_negative:
	AR.apply_postprocessing_function(postprocessors['make_negative'])

AR.convert_array_to_image()
AR.show_image()