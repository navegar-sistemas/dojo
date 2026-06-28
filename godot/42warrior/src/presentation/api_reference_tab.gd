class_name ApiReferenceTab
extends ScrollContainer
## Aba 'API' do painel do editor: adaptador puro de saída. Renderiza os entries
## entregues pelo WarriorApiCatalog sem importar src/domain nem ter lógica de jogo.

@onready var _list: VBoxContainer = $List


func populate(entries: Array) -> void:
	for child in _list.get_children():
		child.queue_free()
	for entry: Dictionary in entries:
		_list.add_child(_build_entry(entry))


func _build_entry(entry: Dictionary) -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 2)

	var sig_label := Label.new()
	sig_label.text = entry["signature"]
	sig_label.add_theme_color_override("font_color", Color(0.5, 0.85, 1.0))
	sig_label.add_theme_font_size_override("font_size", 12)
	sig_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(sig_label)

	var desc_label := Label.new()
	desc_label.text = entry["description"]
	desc_label.add_theme_color_override("font_color", Color(0.75, 0.75, 0.75))
	desc_label.add_theme_font_size_override("font_size", 11)
	desc_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(desc_label)

	var sep := HSeparator.new()
	sep.add_theme_constant_override("separation", 4)
	box.add_child(sep)

	return box
