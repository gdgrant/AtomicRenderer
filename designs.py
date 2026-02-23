import numpy as np


def circle(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	t = np.linspace(0,8*np.pi,200000)

	A = (4/3)*(A+0.25)
	B = (4/3)*(B+0.25)
	C = (4/3)*(C+0.25)

	xs = A*np.sin(B*t)
	ys = np.cos(C*t)

	if color_option == 0:
		cs = np.sin(t/2)

	elif color_option == 1:
		cs = np.sin(t)

	else:
		cs = np.sin(2*t)

	return list(xs), list(ys), list(cs)


def lorenz(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	ρ = 28 + 8*(A - 0.5)
	σ = 10 + 8*(B - 0.5)
	β = 8/3 + 1.5*(C - 0.5)

	dt = 0.001

	x = 0.2*np.random.rand()-0.1
	y = 0.2*np.random.rand()-0.1
	z = 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	zs = []

	for i in range(210000):

		x = x + (σ * (y - x)) * dt
		y = y + (x * (ρ - z) - y) * dt
		z = z + (x * y - β * z) * dt

		if i > 9999:

			xs.append(x)
			ys.append(y)
			zs.append(z)

	if color_option == 0:
		return xs, ys, zs
	elif color_option == 1:
		return xs, zs, ys
	else:
		return ys, zs, xs


def sine_delay(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	a = 10*A + 0.1
	b = min([1, (2*B) * ((10 - a)/10 + 0.3)])

	if A < 0.2 and B < 0.4:
		raise Exception('\n\nFor stability, sine delay parameters must fulfill: B ≥ 0.4 if A < 0.2')

	x_n_m1 = (C + 0.5) * 0.2*np.random.rand()-0.1
	x_n    = (C + 0.5) * 0.2*np.random.rand()-0.1
	x_n_p1 = (C + 0.5) * 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	cs = []

	for i in range(210000):

		x_n_p1 = b * x_n_m1 + a*np.sin(x_n)

		if i > 9999:
			fuzz_x = 0.1 * np.random.rand() * (C - 0.5)
			fuzz_y = 0.1 * np.random.rand() * (C - 0.5)

			xs.append(x_n + fuzz_x)
			ys.append(x_n_p1 + fuzz_y)

			if color_option == 0:
				cs.append(x_n_m1*x_n_m1)
			elif color_option == 1:
				cs.append(x_n_m1*x_n)
			else:
				cs.append(x_n_m1*x_n_p1)

		x_n_m1 = x_n
		x_n = x_n_p1

	return xs, ys, cs


def burgers_map(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	x = 0.2*np.random.rand()-0.1
	y = 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	cs = []

	for i in range(210000):

		x_p1 = (1-1.5*A)*x - y**2
		y_p1 = (1+(B/2+0.5))*y + x*y

		x = x_p1
		y = y_p1

		if i > 9999:

			xs.append(x)
			ys.append(y)

			if color_option == 0:
				cs.append(x)
			elif color_option == 1:
				cs.append(y)
			else:
				cs.append(x*y)

	return xs, ys, cs


def aizawa(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	b = 0.7 * (A/2+0.85)
	d = (B+0.5)*3.5
	c = (C+0.5)*0.6

	a = 0.95
	e = 0.25
	f = 0.1

	dt = 0.001

	x = 0.2*np.random.rand()-0.1
	y = 0.2*np.random.rand()-0.1
	z = 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	zs = []

	for i in range(210000):

		x = x + dt * ((z - b) * x - d * y)
		y = y + dt * (d * x + (z - b) * y)
		z = z + dt * (c + a * z - z**3/3 - (x**2 + y**2) * (1 + e * z) + f * z * x**3)

		if i > 9999:

			xs.append(x)
			ys.append(y)
			zs.append(z)

	if color_option == 0:
		return xs, zs, ys
	elif color_option == 1:
		return xs, ys, zs
	else:
		return zs, ys, xs


def popcorn(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	if A < 0.3 and B < 0.4:
		raise Exception('\n\nFor stability, popcorn parameters must fulfill: B ≥ 0.4 if A < 0.3')

	a = A/2 + 0.5
	b = 4*B + 0.5

	x = 0.2*np.random.rand()-0.1
	y = 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	cs = []

	for i in range(210000):

		x_p1 = a * np.sin(y + np.tan(b*y)) + (C-0.5) * y
		y_p1 = a * np.sin(x + np.tan(b*x)) + (C-0.5) * x

		x = x_p1
		y = y_p1

		if i > 9999:

			xs.append(x)
			ys.append(y)

			if color_option == 0:
				cs.append(x)
			elif color_option == 1:
				cs.append(y)
			else:
				cs.append(x*y)

	return xs, ys, cs


def hourglass(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	if A > 0.6 and B > 0.9:
		raise Exception('\n\nFor stability, hourglass parameters must fulfill: A ≤ 0.6 if B > 0.9')

	a = 1.7 + A/4
	e = 0.7*(B - 0.5)

	x_m1 = 0.2*np.random.rand()-0.1
	x    = 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	cs = []

	for i in range(210000):

		x_p1 = x * (a - np.abs(x_m1)**(2+e)) + 0.05*(C-0.5)*np.random.rand()

		if i > 9999:

			xs.append(x)
			ys.append(x_p1)

			if color_option == 0:
				cs.append(x)
			elif color_option == 1:
				cs.append(x_p1)
			else:
				cs.append(x*x_p1)

		x_m1 = x
		x = x_p1

	return xs, ys, cs


def henon(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	a = 1.3 + A/10
	b = 0.2 + B/10

	x = 0.2*np.random.rand()-0.1
	y = 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	cs = []

	for i in range(210000):

		x_p1 = 1 - a * x**2 + y + 0.05*(C-0.5)*np.random.rand()
		y_p1 = b * x + 0.05*(C-0.5)*np.random.rand()

		x = x_p1
		y = y_p1

		if i > 9999:

			if color_option == 0:
				xs.append(x)
				ys.append(y)
				cs.append(x)
			elif color_option == 1:
				xs.append(-y)
				ys.append(-x)
				cs.append(y)
			else:
				xs.append(x)
				ys.append(y)
				cs.append(x*y)

	return xs, ys, cs


def gingerbread(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	if np.abs(A) < np.abs(B):
		raise Exception('\n\nFor stability, gingerbread parameters must fulfill: |A| ≥ |B|')

	a = -(A/5+0.9) - 1e-3
	b = -(B/5+0.9)

	# a = -1.001
	# b = -1.00001

	x = 0.2*np.random.rand()-0.1
	y = 0.2*np.random.rand()-0.1

	xs = []
	ys = []
	cs = []

	for i in range(210000):

		x_p1 = 1 - a * np.abs(x) + b * y
		y_p1 = x + 0.01*(C-0.4999)*np.random.rand()

		x = x_p1
		y = y_p1

		if i > 9999:

			if color_option == 0:
				xs.append(x)
				ys.append(y)
				cs.append(x)
			elif color_option == 1:
				xs.append(-y)
				ys.append(-x)
				cs.append(y)
			else:
				xs.append(x)
				ys.append(y)
				cs.append(x*y)

	return xs, ys, cs


def cat(A, B, C, color_option=0):

	assert A >= 0 and A <= 1
	assert B >= 0 and B <= 1
	assert C >= 0 and C <= 1
	assert color_option in [0,1,2]

	x = 0.2*np.random.rand()
	y = 0.2*np.random.rand()

	a = 0.7*A + 0.4
	b = 0.7*B + 0.4
	c = 1 + (C - 0.5)

	xs = []
	ys = []
	cs = []

	for i in range(210000):

		x_p1 = np.mod(2*x**a + y**b, 1)**c
		y_p1 = np.mod(x**a + y**b, 1)

		x = x_p1
		y = y_p1

		if i > 9999:

			if color_option == 0:
				xs.append(x)
				ys.append(y)
				cs.append(x)
			elif color_option == 1:
				xs.append(-y)
				ys.append(-x)
				cs.append(y)
			else:
				xs.append(x)
				ys.append(y)
				cs.append(x*y)

	return xs, ys, cs
