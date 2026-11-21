extends SceneTree

const FRAME_SIZE := Vector2i(540, 960)
const FPS := 24
const FRAMES := 42 * FPS
const BALLOON_BIRTHS := [0.88, 13.70, 17.68, 25.32]
const BALLOON_SIZES := [73, 55, 61, 118]
const BREATH := [
	[0.75, 1.50, "customer"], [13.70, 14.5, "customer"],
	[17.50, 18.25, "customer"], [25.00, 27.25, "clerk"]
]
const VOICE := [
	[4.25, 5.3, "customer"],
	[6.05, 9.0, "customer"], [13.0, 13.46, "customer"],
	[30.0, 32.75, "customer"], [38.25, 40.5, "clerk"]
]

var source_dir: String
var target_dir: String
var frame: Image
var images: Dictionary = {}


func _initialize() -> void:
	var arguments := OS.get_cmdline_user_args()
	if arguments.size() != 2:
		push_error("Expected artwork directory and frame output directory")
		quit(2)
		return
	source_dir = arguments[0]
	target_dir = arguments[1]

	var artwork := [
		"background", "customer_body", "clerk_body", "balloon", "coffee", "menu"
	]
	for role in ["customer", "clerk"]:
		for layer in [
			"arms_rest", "arms_reach", "arms_gather", "arms_elbow",
			"eyes_normal", "eyes_up", "eyes_closed",
			"mouth_closed", "mouth_open", "mouth_smile"
		]:
			artwork.append(role + "_" + layer)
	for name in artwork:
		var path: String = source_dir.path_join(name + ".svg")
		if not FileAccess.file_exists(path):
			push_error("Missing artwork: " + path)
			quit(2)
			return
		var image := Image.new()
		var result := image.load_svg_from_string(FileAccess.get_file_as_string(path))
		if result != OK:
			push_error("Could not rasterize " + path)
			quit(2)
			return
		image.convert(Image.FORMAT_RGBA8)
		images[name] = image
	for index in range(FRAMES):
		render_frame(float(index) / FPS)
		var path := target_dir.path_join("frame%04d.png" % index)
		if frame.save_png(path) != OK:
			push_error("Could not write " + path)
			quit(3)
			return
	print("Godot composited %d frames at %d fps" % [FRAMES, FPS])
	quit()


func tween(time: float, start: float, end: float) -> float:
	return smoothstep(start, end, time)


func stamp(name: String, center: Vector2, size: Vector2i, flip := false, clip_bottom := 960) -> void:
	var key := "%s:%s:%s" % [name, size, flip]
	if not images.has(key):
		var image: Image = images[name].duplicate()
		image.resize(size.x, size.y, Image.INTERPOLATE_LANCZOS)
		if flip:
			image.flip_x()
		images[key] = image
	var drawable: Image = images[key]
	var top_left := Vector2i(center - Vector2(size) * 0.5)
	var height := clampi(clip_bottom - top_left.y, 0, size.y)
	if height > 0:
		frame.blend_rect(drawable, Rect2i(0, 0, size.x, height), top_left)


func actor(role: String, time: float, center: Vector2, size: Vector2i,
		arms: String, eyes: String, smile: bool, flip := false, clip_bottom := 960) -> void:
	var mouth := "smile" if smile else "closed"
	for cue in VOICE:
		if cue[2] == role and time >= cue[0] and time < cue[1]:
			if absf(sin((time - cue[0]) * 19.0)) > 0.30:
				mouth = "open"
			break
	for cue in BREATH:
		if cue[2] == role and time >= cue[0] and time < cue[1]:
			mouth = "open"
			break
	stamp(role + "_body", center, size, flip, clip_bottom)
	stamp(role + "_arms_" + arms, center, size, flip, clip_bottom)
	stamp(role + "_eyes_" + eyes, center, size, flip, clip_bottom)
	stamp(role + "_mouth_" + mouth, center, size, flip, clip_bottom)


func balloon(index: int, time: float, center: Vector2) -> void:
	var birth: float = BALLOON_BIRTHS[index]
	if time < birth:
		return
	var nominal: int = BALLOON_SIZES[index]
	var size := maxi(6, int(round(lerpf(6, nominal, tween(time, birth, birth + 0.44)) / 4.0)) * 4)
	stamp("balloon", center, Vector2i(size, int(round(size * 215.0 / 180.0))))


func render_frame(time: float) -> void:
	frame = Image.create(FRAME_SIZE.x, FRAME_SIZE.y, false, Image.FORMAT_RGBA8)
	stamp("background", Vector2(FRAME_SIZE) * 0.5, FRAME_SIZE)

	var customer := Vector2(369, 578)
	var clerk := Vector2(185, 474)
	var customer_size := Vector2i(229, 301)
	var clerk_size := Vector2i(180, 236)
	var customer_arms := "rest"
	var clerk_arms := "rest"
	var customer_eyes := "normal"
	var clerk_eyes := "normal"
	var smile := time >= 31
	var cup := Vector2(242, 532)
	var menu := Vector2(278, 515)
	var f1 := Vector2(354, 353)
	var f2 := Vector2(418, 446)
	var f3 := Vector2(356, 286)
	var f4 := Vector2(153, 335)

	if time < 3.0:
		# In the opening insert, the breath origin and gaze remain in one frame.
		customer_size = Vector2i(299, 392)
		customer = Vector2(358, 562 + 22 * tween(time, 0.35, 1.0))
		clerk = Vector2(-115, 480)
		customer_arms = "elbow"
		f1 = Vector2(348, 536).lerp(Vector2(324, 404), tween(time, 0.88, 2.75))
		if time > 1.28:
			customer_eyes = "up"
	elif time < 11.0:
		customer_eyes = "up" if time < 4.0 else "normal"
		clerk_eyes = "up" if time > 9.0 else "normal"
	elif time < 22.0:
		customer_arms = "reach" if time < 17.4 else "gather"
		customer_eyes = "up" if time > 17.7 else "normal"
		f1 = f1.lerp(Vector2(288, 489), tween(time, 11.0, 12.7))
		f2 = Vector2(362, 542).lerp(f2, tween(time, 13.7, 16.25))
		f3 = Vector2(362, 542).lerp(f3, tween(time, 17.68, 20.2))
	elif time < 34.0:
		customer_arms = "gather"
		customer_eyes = "up" if time < 30 else "normal"
		clerk_arms = "reach" if time < 24.5 else "rest"
		clerk_eyes = "closed" if time >= 25.0 and time < 27.25 else "normal"
		f1 = Vector2(288, 489)
		f4 = Vector2(191, 446).lerp(f4, tween(time, 25.32, 26.28))
		cup = Vector2(205, 516).lerp(cup, tween(time, 22.5, 24.0))
		customer.y += 12 * tween(time, 29.4, 31.3)
	else:
		var walk := tween(time, 34.0, 38.0)
		clerk = clerk.lerp(Vector2(432, 526), walk)
		var follow := tween(time, 35.2, 38.0)
		customer = customer.lerp(Vector2(336, 609), follow)
		customer.y += sin(follow * TAU * 2) * 9
		clerk.y += sin(walk * TAU * 2) * 11
		customer_arms = "gather"
		clerk_arms = "reach"
		f1 = Vector2(288, 489).lerp(Vector2(344, 390), follow)
		f2 = f2.lerp(Vector2(415, 392), follow)
		f3 = f3.lerp(Vector2(377, 335), tween(time, 35.0, 38.0))
		f4 = f4.lerp(Vector2(425, 263), walk)
		cup = cup.lerp(customer + Vector2(35, 48), follow)

	actor("clerk", time, clerk, clerk_size, clerk_arms, clerk_eyes, time > 37.0, time >= 34.0,
		544 if clerk.x < 316 else 960)
	actor("customer", time, customer, customer_size, customer_arms, customer_eyes, smile)
	balloon(0, time, f1)
	balloon(1, time, f2)
	balloon(2, time, f3)
	balloon(3, time, f4)
	stamp("menu", menu, Vector2i(58, 73))
	if time >= 22.4:
		stamp("coffee", cup, Vector2i(49, 64))

	if time < 3.0:
		# Keep the upper chest, mouth, and full trajectory in the same shot.
		frame = frame.get_region(Rect2i(262, 346, 180, 320))
		frame.resize(FRAME_SIZE.x, FRAME_SIZE.y, Image.INTERPOLATE_LANCZOS)
