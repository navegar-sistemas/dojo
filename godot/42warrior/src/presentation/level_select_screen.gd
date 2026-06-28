class_name LevelSelectScreen
extends PanelContainer
## Tela de seleção de níveis: lista os 9 níveis com status e melhor pontuação.
## Acessada pelo menu principal (RF-090). Usa LevelProgressStore para leitura.

var _store := LevelProgressStore.new()

@onready var _list: VBoxContainer = $VBox/Scroll/List
@onready var _back_btn: Button = $VBox/BackBtn


func _ready() -> void:
	_back_btn.pressed.connect(_on_back)
	_populate()


func _populate() -> void:
	for child in _list.get_children():
		child.queue_free()
	_list.add_child(_build_sandbox_row())
	for entry: Dictionary in _store.all_levels_summary():
		_list.add_child(_build_row(entry))


func _build_row(entry: Dictionary) -> Control:
	var hbox := HBoxContainer.new()
	hbox.add_theme_constant_override("separation", 8)

	var lbl := Label.new()
	var status: String = entry["status"]
	var icon := (
		"🔒 "
		if status == LevelProgressStore.STATUS_LOCKED
		else "✓ " if status == LevelProgressStore.STATUS_WON else "• "
	)
	lbl.text = "%s Nível %d — %s" % [icon, entry["index"], entry["description"]]
	lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	lbl.add_theme_font_size_override("font_size", 13)
	hbox.add_child(lbl)

	if status == LevelProgressStore.STATUS_WON:
		var score_lbl := Label.new()
		var ace_mark := " ★" if entry["is_ace"] else ""
		score_lbl.text = "%d pts%s" % [entry["score_best"], ace_mark]
		score_lbl.add_theme_color_override("font_color", Color(0.9, 0.8, 0.4))
		score_lbl.add_theme_font_size_override("font_size", 13)
		hbox.add_child(score_lbl)

	if status != LevelProgressStore.STATUS_LOCKED:
		var btn := Button.new()
		btn.text = "Jogar"
		btn.add_theme_font_size_override("font_size", 12)
		var level_index: int = entry["index"]
		btn.pressed.connect(func() -> void: _on_select(level_index))
		hbox.add_child(btn)

	return hbox


func _build_sandbox_row() -> Control:
	var hbox := HBoxContainer.new()
	hbox.add_theme_constant_override("separation", 8)

	var lbl := Label.new()
	lbl.text = "🎯 Treinamento — Pratique a API sem pontuação"
	lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	lbl.add_theme_font_size_override("font_size", 13)
	lbl.add_theme_color_override("font_color", Color(0.7, 0.9, 0.7))
	hbox.add_child(lbl)

	var btn := Button.new()
	btn.text = "Jogar"
	btn.add_theme_font_size_override("font_size", 12)
	btn.pressed.connect(func() -> void: _on_select(0))
	hbox.add_child(btn)

	return hbox


func _on_select(level_index: int) -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.start(level_index)


func _on_back() -> void:
	var screen_mgr: Node = get_node_or_null("/root/ScreenManager")
	if screen_mgr:
		screen_mgr.change_to("res://scenes/main_menu.tscn")
