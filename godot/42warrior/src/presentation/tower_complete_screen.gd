class_name TowerCompleteScreen
extends PanelContainer
## Tela de conclusão da torre + créditos, exibida ao vencer o nível 9 (DoD T-053).

@onready var _menu_btn: Button = $VBox/MenuBtn


func _ready() -> void:
	_menu_btn.pressed.connect(_on_menu_pressed)


func _on_menu_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.on_go_to_menu()
