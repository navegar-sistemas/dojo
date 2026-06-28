extends GutTest
## RNF-050: domínio não referencia áudio.
## Verifica que nenhum .gd em src/domain/ menciona AudioStream, AudioPlayer, etc.


func test_domain_zero_referencias_a_audio() -> void:
	var dir := DirAccess.open("res://src/domain")
	assert_not_null(dir, "diretório src/domain existe")
	var files := _collect_gd(dir, "res://src/domain")
	for path: String in files:
		var fa := FileAccess.open(path, FileAccess.READ)
		if fa == null:
			continue
		var source := fa.get_as_text()
		assert_false(
			source.contains("AudioStream") or source.contains("AudioPlayer"),
			"%s não deve referenciar áudio" % path
		)


func _collect_gd(dir: DirAccess, base: String) -> Array:
	var result: Array = []
	dir.list_dir_begin()
	var name := dir.get_next()
	while name != "":
		if dir.current_is_dir() and not name.begins_with("."):
			var sub := DirAccess.open(base + "/" + name)
			if sub:
				result.append_array(_collect_gd(sub, base + "/" + name))
		elif name.ends_with(".gd"):
			result.append(base + "/" + name)
		name = dir.get_next()
	dir.list_dir_end()
	return result
