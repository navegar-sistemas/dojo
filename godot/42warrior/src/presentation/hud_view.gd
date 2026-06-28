class_name HudView
extends CanvasLayer

@onready var _hp_label: Label = $StatusBar/HpLabel
@onready var _turn_label: Label = $StatusBar/TurnLabel
@onready var _level_label: Label = $StatusBar/LevelLabel
@onready var _score_label: Label = $StatusBar/ScoreLabel
@onready var _hint_label: Label = $HintLabel


func update_hud(state: LevelState, turn: int, description: String, score: int) -> void:
	var warrior := state.warrior()
	_hp_label.text = "♥ %d/%d" % [warrior.health, warrior.max_health]
	_turn_label.text = "Turno: %d" % turn
	_level_label.text = description
	_score_label.text = "Score: %d" % score


func setup_hint(text: String) -> void:
	_hint_label.text = text
	_hint_label.visible = not text.is_empty()


func apply_theme(t: Theme) -> void:
	for child in get_children():
		if child is Control:
			(child as Control).theme = t
