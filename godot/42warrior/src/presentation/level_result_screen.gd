class_name LevelResultScreen
extends PanelContainer
## Tela de resultado: exibe pontuação/ace na vitória, ou mensagem de derrota.
## Botões avançam nível ou reiniciam (DoD T-052).

@onready var _title: Label = $VBox/Title
@onready var _score_label: Label = $VBox/ScoreLabel
@onready var _ace_label: Label = $VBox/AceLabel
@onready var _next_btn: Button = $VBox/NextBtn
@onready var _retry_btn: Button = $VBox/RetryBtn
@onready var _menu_btn: Button = $VBox/MenuBtn


func _ready() -> void:
	_next_btn.pressed.connect(_on_next_pressed)
	_retry_btn.pressed.connect(_on_retry_pressed)
	_menu_btn.pressed.connect(_on_menu_pressed)
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if not flow:
		return
	var res: Dictionary = flow.last_result()
	if res.get("won", false):
		_show_won(res)
	else:
		_show_lost()


func _show_won(res: Dictionary) -> void:
	_title.text = ThemeCatalog.message("victory")
	_score_label.text = ThemeCatalog.message("score_label", [res.score_total, res.turns])
	_ace_label.text = ThemeCatalog.message("ace") if res.get("is_ace", false) else ""
	_next_btn.visible = true
	_retry_btn.visible = true
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow and flow.pending_level() >= BeginnerTower.LEVEL_COUNT:
		_next_btn.visible = false


func _show_lost() -> void:
	_title.text = ThemeCatalog.message("defeat")
	_score_label.text = ThemeCatalog.message("retry")
	_ace_label.text = ""
	_next_btn.visible = false
	_retry_btn.visible = true


func _on_next_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.on_next_level()


func _on_retry_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.on_retry()


func _on_menu_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.on_go_to_menu()
