class_name LevelProgressStore
extends RefCounted
## Persistência por nível: status (locked/unlocked/won), melhor pontuação e
## flag ace. Toda escrita em user://; 0 escrita em res://.

const STATUS_LOCKED := "locked"
const STATUS_UNLOCKED := "unlocked"
const STATUS_WON := "won"

const _SAVE_PATH := "user://level_progress.cfg"
const _KEY_STATUS := "status"
const _KEY_SCORE := "score_best"
const _KEY_ACE := "is_ace"


func level_status(level: int) -> String:
	if level == 0:
		return STATUS_UNLOCKED
	return _cfg_get(_section(level), _KEY_STATUS, STATUS_LOCKED)


func best_score_for(level: int) -> int:
	return _cfg_get(_section(level), _KEY_SCORE, 0)


func is_ace_for(level: int) -> bool:
	return _cfg_get(_section(level), _KEY_ACE, false)


func unlock_level(level: int) -> void:
	if level == 0:
		return
	if level < 1 or level > BeginnerTower.LEVEL_COUNT:
		return
	var current := level_status(level)
	if current != STATUS_LOCKED:
		return
	_cfg_set(_section(level), _KEY_STATUS, STATUS_UNLOCKED)


func save_result(level: int, score: int, won: bool, p_is_ace: bool) -> void:
	if level < 1 or level > BeginnerTower.LEVEL_COUNT:
		return
	if won:
		_cfg_set(_section(level), _KEY_STATUS, STATUS_WON)
		if score > best_score_for(level):
			_cfg_set(_section(level), _KEY_SCORE, score)
			_cfg_set(_section(level), _KEY_ACE, p_is_ace)
		elif p_is_ace and not is_ace_for(level):
			_cfg_set(_section(level), _KEY_ACE, true)


func all_levels_summary() -> Array:
	var result: Array = []
	for i: int in range(1, BeginnerTower.LEVEL_COUNT + 1):
		var status := level_status(i)
		(
			result
			. append(
				{
					"index": i,
					"status": status,
					"score_best": best_score_for(i) if status == STATUS_WON else 0,
					"is_ace": is_ace_for(i),
					"description": BeginnerTower.definition(i).description,
				}
			)
		)
	return result


func reset() -> void:
	if FileAccess.file_exists(_SAVE_PATH):
		DirAccess.remove_absolute(_SAVE_PATH)


func _section(level: int) -> String:
	return "L%d" % level


func _cfg_get(section: String, key: String, default: Variant) -> Variant:
	var cfg := ConfigFile.new()
	if cfg.load(_SAVE_PATH) != OK:
		return default
	return cfg.get_value(section, key, default)


func _cfg_set(section: String, key: String, value: Variant) -> void:
	var cfg := ConfigFile.new()
	cfg.load(_SAVE_PATH)
	cfg.set_value(section, key, value)
	cfg.save(_SAVE_PATH)
