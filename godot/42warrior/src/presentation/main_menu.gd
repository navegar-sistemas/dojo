class_name MainMenu
extends PanelContainer

signal start_requested(level: int)

var _store: ProgressStore

@onready var _start_btn: FourStateButton = $VBox/StartBtn
@onready var _continue_btn: FourStateButton = $VBox/ContinueBtn
@onready var _select_btn: FourStateButton = $VBox/SelectLevelsBtn
@onready var _audio_btn: FourStateButton = $VBox/AudioBtn
@onready var _about_btn: FourStateButton = $VBox/AboutBtn


func _ready() -> void:
	_store = ProgressStore.new()
	_start_btn.pressed.connect(_on_start_pressed)
	_continue_btn.pressed.connect(_on_continue_pressed)
	_select_btn.pressed.connect(_on_select_levels_pressed)
	_audio_btn.pressed.connect(_on_audio_pressed)
	_about_btn.pressed.connect(_on_about_pressed)
	_continue_btn.disabled = not _store.has_save()
	_apply_theme()


func _on_start_pressed() -> void:
	LevelProgressStore.new().unlock_level(1)
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.start(1)
	else:
		start_requested.emit(1)


func _on_select_levels_pressed() -> void:
	var screen_mgr: Node = get_node_or_null("/root/ScreenManager")
	if screen_mgr:
		screen_mgr.change_to("res://scenes/level_select_screen.tscn")


func _on_continue_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.start(_store.current_level())
	else:
		start_requested.emit(_store.current_level())


func _on_audio_pressed() -> void:
	pass


func _on_about_pressed() -> void:
	pass


func _apply_theme() -> void:
	theme = GlobalDesignSystem.build_theme()
