class_name TurnConsole
extends ScrollContainer
## Lista cronológica de entradas de turno — exibe o que o TurnEventFormatter
## produziu. Destaca o turno corrente e faz scroll automático até ele.

const _COLOR_DEFAULT := Color(0.75, 0.75, 0.75, 1.0)
const _COLOR_CURRENT := Color(0.4, 0.9, 0.5, 1.0)
const _COLOR_HEADER := Color(0.9, 0.8, 0.4, 1.0)

var _entries: Array = []
var _current := -1

@onready var _list: VBoxContainer = $List


func clear() -> void:
	for child: Node in _list.get_children():
		child.queue_free()
	_entries.clear()
	_current = -1


func populate(texts: Array) -> void:
	clear()
	for i: int in texts.size():
		var lbl := Label.new()
		lbl.text = "T%d — %s" % [i + 1, texts[i]]
		lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		lbl.add_theme_font_size_override("font_size", 11)
		lbl.add_theme_color_override("font_color", _COLOR_DEFAULT)
		_list.add_child(lbl)
		_entries.append(lbl)


func set_current(index: int) -> void:
	if _current >= 0 and _current < _entries.size():
		(_entries[_current] as Label).add_theme_color_override("font_color", _COLOR_DEFAULT)
	_current = index
	if index < 0 or index >= _entries.size():
		return
	var lbl := _entries[index] as Label
	lbl.add_theme_color_override("font_color", _COLOR_CURRENT)
	ensure_control_visible(lbl)
