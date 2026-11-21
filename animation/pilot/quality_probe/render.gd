extends SceneTree


func _initialize() -> void:
	var arguments := OS.get_cmdline_user_args()
	if arguments.size() != 1:
		push_error("Expected a directory with 72 SVG frames")
		quit(2)
		return
	for index in range(72):
		var stem := arguments[0].path_join("frame%03d" % index)
		var frame := Image.new()
		if frame.load_svg_from_string(FileAccess.get_file_as_string(stem + ".svg")) != OK:
			push_error("Invalid SVG frame: " + stem)
			quit(3)
			return
		if frame.get_size() != Vector2i(1080, 1920) or frame.save_png(stem + ".png") != OK:
			push_error("Incorrect resolution or unwritable image: " + stem)
			quit(4)
			return
	quit()
