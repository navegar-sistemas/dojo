class_name PlayerCodeStore
extends RefCounted


func save(level_index: int, source: String) -> void:
	var file := FileAccess.open(_path(level_index), FileAccess.WRITE)
	if file:
		file.store_string(source)


func load_or_empty(level_index: int) -> String:
	var path := _path(level_index)
	if not FileAccess.file_exists(path):
		return ""
	var file := FileAccess.open(path, FileAccess.READ)
	if not file:
		return ""
	return file.get_as_text()


func has_saved(level_index: int) -> bool:
	return FileAccess.file_exists(_path(level_index))


func _path(level_index: int) -> String:
	return "user://player_code_level_%d.gd" % level_index
