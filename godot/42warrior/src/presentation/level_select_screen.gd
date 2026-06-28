class_name LevelSelectScreen
extends PanelContainer
## Tela de seleção de níveis: grade 3×3 dos 9 andares com estados visuais.
## ui_check = concluído, ui_star = ace, ui_lock = bloqueado, ciano = atual, magenta = chefe.

const LEVEL_COUNT := 9
const _COLOR_LOCKED := Color(0.4, 0.4, 0.4, 1.0)
const _COLOR_CURRENT := Color(0, 0.941, 1, 1.0)
const _COLOR_BOSS := Color(1, 0, 0.737, 1.0)
const _COLOR_WON := Color(0.4, 0.9, 0.5, 1.0)

var _store := LevelProgressStore.new()

@onready var _grid: GridContainer = $VBox/LevelGrid
@onready var _back_btn: FourStateButton = $VBox/BackBtn


func _ready() -> void:
	_back_btn.pressed.connect(_on_back)
	_apply_theme()
	_populate()


func _populate() -> void:
	for child in _grid.get_children():
		child.queue_free()
	var summary: Array = _store.all_levels_summary()
	for i: int in range(1, LEVEL_COUNT + 1):
		var entry: Dictionary = {}
		for s: Dictionary in summary:
			if s.get("index", -1) == i:
				entry = s
				break
		_grid.add_child(_build_level_btn(i, entry))


func _build_level_btn(index: int, entry: Dictionary) -> FourStateButton:
	var btn := FourStateButton.new()
	btn.name = "LevelBtn_%d" % index
	btn.custom_minimum_size = Vector2(88, 64)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var status: String = entry.get("status", LevelProgressStore.STATUS_LOCKED)
	var is_ace: bool = entry.get("is_ace", false)

	var label := ""
	var color := _COLOR_LOCKED

	if index == LEVEL_COUNT:
		label = "BOSS\n[%02d]" % index
		color = _COLOR_BOSS if status != LevelProgressStore.STATUS_LOCKED else _COLOR_LOCKED
	elif status == LevelProgressStore.STATUS_LOCKED:
		label = "🔒\n[%02d]" % index
		color = _COLOR_LOCKED
		btn.disabled = true
	elif status == LevelProgressStore.STATUS_WON:
		var mark := " ★" if is_ace else " ✓"
		label = "[%02d]%s" % [index, mark]
		color = _COLOR_WON
	else:
		label = "▶\n[%02d]" % index
		color = _COLOR_CURRENT

	btn.text = label
	btn.add_theme_color_override("font_color", color)
	btn.add_theme_font_size_override("font_size", 13)

	if status != LevelProgressStore.STATUS_LOCKED:
		var level_index := index
		btn.pressed.connect(func() -> void: _on_select(level_index))

	return btn


func _on_select(level_index: int) -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.start(level_index)


func _on_back() -> void:
	var screen_mgr: Node = get_node_or_null("/root/ScreenManager")
	if screen_mgr:
		screen_mgr.change_to("res://scenes/main_menu.tscn")


func _apply_theme() -> void:
	theme = GlobalDesignSystem.build_theme()
