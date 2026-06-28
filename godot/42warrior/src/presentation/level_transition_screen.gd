class_name LevelTransitionScreen
extends PanelContainer
## Tela de transição exibida antes de cada nível: mostra número, descrição e
## habilidades introduzidas (DoD T-051).

@onready var _title: Label = $VBox/Title
@onready var _desc: Label = $VBox/Description
@onready var _abilities: Label = $VBox/Abilities
@onready var _start_btn: Button = $VBox/StartBtn


func _ready() -> void:
	_start_btn.pressed.connect(_on_start_pressed)
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		var def: LevelDefinition = BeginnerTower.definition(flow.pending_level())
		_show_level(def)


func _show_level(definition: LevelDefinition) -> void:
	_title.text = ThemeCatalog.message("floor_heading", [definition.index])
	_desc.text = definition.description
	if definition.abilities.is_empty():
		_abilities.text = ""
	else:
		_abilities.text = "Habilidades: " + ", ".join(definition.abilities)


func _on_start_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.on_transition_confirmed()
