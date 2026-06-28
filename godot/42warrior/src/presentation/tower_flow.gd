extends Node
## Autoload "TowerFlow" — orquestra o fluxo de cenas da torre:
## menu → transição → jogo → resultado → (próximo / créditos).

var _store := ProgressStore.new()
var _level_store := LevelProgressStore.new()
var _current_level := 1
var _last_score_total := 0
var _last_turns := 0
var _last_is_ace := false
var _last_won := false


func pending_level() -> int:
	return _current_level


func last_result() -> Dictionary:
	return {
		"won": _last_won,
		"score_total": _last_score_total,
		"turns": _last_turns,
		"is_ace": _last_is_ace,
	}


func start(level: int) -> void:
	_current_level = level
	ScreenManager.change_to("res://scenes/level_transition.tscn")


func on_transition_confirmed() -> void:
	ScreenManager.change_to("res://scenes/game.tscn")


func on_level_won(score_total: int, turns: int, is_ace: bool) -> void:
	_last_score_total = score_total
	_last_turns = turns
	_last_is_ace = is_ace
	_last_won = true
	_level_store.save_result(_current_level, score_total, true, is_ace)
	if _current_level < BeginnerTower.LEVEL_COUNT:
		_store.save_level(_current_level + 1)
		_level_store.unlock_level(_current_level + 1)
	if _current_level >= BeginnerTower.LEVEL_COUNT:
		ScreenManager.change_to("res://scenes/tower_complete.tscn")
	else:
		ScreenManager.change_to("res://scenes/level_result.tscn")


func on_level_lost() -> void:
	_last_won = false
	ScreenManager.change_to("res://scenes/level_result.tscn")


func on_next_level() -> void:
	_current_level += 1
	start(_current_level)


func on_retry() -> void:
	start(_current_level)


func on_go_to_menu() -> void:
	ScreenManager.change_to("res://scenes/main_menu.tscn")
