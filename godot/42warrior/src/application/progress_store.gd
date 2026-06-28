class_name ProgressStore
extends RefCounted

const _SAVE_PATH := "user://progress.cfg"
const _KEY_LEVEL := "level"
const _KEY_VOL_MUSIC := "vol_music"
const _KEY_VOL_SFX := "vol_sfx"


func current_level() -> int:
	var cfg := ConfigFile.new()
	if cfg.load(_SAVE_PATH) != OK:
		return 1
	return cfg.get_value("progress", _KEY_LEVEL, 1)


func save_level(level: int) -> void:
	var cfg := ConfigFile.new()
	cfg.load(_SAVE_PATH)
	# Progress never regresses: only advance if the new level is higher than the saved one.
	var current: int = cfg.get_value("progress", _KEY_LEVEL, 1)
	if level <= current:
		return
	cfg.set_value("progress", _KEY_LEVEL, level)
	cfg.save(_SAVE_PATH)


func vol_music() -> float:
	var cfg := ConfigFile.new()
	if cfg.load(_SAVE_PATH) != OK:
		return 1.0
	return cfg.get_value("settings", _KEY_VOL_MUSIC, 1.0)


func vol_sfx() -> float:
	var cfg := ConfigFile.new()
	if cfg.load(_SAVE_PATH) != OK:
		return 1.0
	return cfg.get_value("settings", _KEY_VOL_SFX, 1.0)


func save_volume(music: float, sfx: float) -> void:
	var cfg := ConfigFile.new()
	cfg.load(_SAVE_PATH)
	cfg.set_value("settings", _KEY_VOL_MUSIC, music)
	cfg.set_value("settings", _KEY_VOL_SFX, sfx)
	cfg.save(_SAVE_PATH)


func has_save() -> bool:
	return FileAccess.file_exists(_SAVE_PATH)


func reset() -> void:
	if FileAccess.file_exists(_SAVE_PATH):
		DirAccess.remove_absolute(_SAVE_PATH)
