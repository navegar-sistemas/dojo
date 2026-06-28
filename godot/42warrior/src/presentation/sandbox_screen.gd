class_name SandboxScreen
extends PanelContainer
## Tela Sandbox/Tutorial: grade limpa com herói + portal, tooltips passo a passo,
## badge MODO SANDBOX. Reusa DungeonView (T-160/T-161). (DoD T-168)

const _TOOLTIPS: PackedStringArray = [
	"Use feel() para inspecionar a célula à sua frente.",
	"Use walk() para mover o warrior um passo.",
	"Use attack() para atacar um inimigo adjacente.",
	"Use direction_of_stairs() para encontrar a escada.",
]

@onready var _badge: Label = $VBox/SandboxBadge
@onready var _tooltip_list: VBoxContainer = $VBox/TooltipList
@onready var _menu_btn: Button = $VBox/MenuBtn


func _ready() -> void:
	_populate_tooltips()
	_menu_btn.pressed.connect(_on_menu_pressed)
	_init_dungeon()


func _populate_tooltips() -> void:
	for tip: String in _TOOLTIPS:
		var lbl := Label.new()
		lbl.text = tip
		lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		_tooltip_list.add_child(lbl)


func _init_dungeon() -> void:
	var dungeon_scene := load("res://scenes/dungeon_view.tscn") as PackedScene
	if dungeon_scene == null:
		return
	var dungeon := dungeon_scene.instantiate() as DungeonView
	dungeon.name = "DungeonView"
	$VBox.add_child(dungeon)
	$VBox.move_child(dungeon, 1)
	var definition := BeginnerTower.definition(1)
	var state := LevelLoader.new().load_definition(definition)
	dungeon.refresh_level(state)


func _on_menu_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.on_go_to_menu()
