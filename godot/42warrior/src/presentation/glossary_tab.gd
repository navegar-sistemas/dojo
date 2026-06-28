class_name GlossaryTab
extends ScrollContainer
## Aba 'Glossário' do painel do editor: adaptador puro de saída. Renderiza as
## entidades do nível e os termos de pontuação do GlossaryCatalog.

@onready var _list: VBoxContainer = $List


func populate(entries: Dictionary) -> void:
	for child in _list.get_children():
		child.queue_free()
	var entities: Array = entries.get("entities", [])
	var score_terms: Array = entries.get("score_terms", [])
	if not entities.is_empty():
		_list.add_child(_section_label("Entidades"))
		for entity: Dictionary in entities:
			_list.add_child(_build_item(entity["name"], entity["description"]))
	if not score_terms.is_empty():
		_list.add_child(_section_label("Pontuação"))
		for term: Dictionary in score_terms:
			_list.add_child(
				_build_item(term["name"], "%s — %s" % [term["value"], term["definition"]])
			)


func _section_label(text: String) -> Label:
	var lbl := Label.new()
	lbl.text = text.to_upper()
	lbl.add_theme_color_override("font_color", Color(0.9, 0.8, 0.4))
	lbl.add_theme_font_size_override("font_size", 11)
	return lbl


func _build_item(name_text: String, description: String) -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 2)

	var name_lbl := Label.new()
	name_lbl.text = name_text
	name_lbl.add_theme_color_override("font_color", Color(0.85, 0.85, 1.0))
	name_lbl.add_theme_font_size_override("font_size", 12)
	box.add_child(name_lbl)

	var desc_lbl := Label.new()
	desc_lbl.text = description
	desc_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
	desc_lbl.add_theme_font_size_override("font_size", 11)
	desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(desc_lbl)

	var sep := HSeparator.new()
	sep.add_theme_constant_override("separation", 4)
	box.add_child(sep)

	return box
