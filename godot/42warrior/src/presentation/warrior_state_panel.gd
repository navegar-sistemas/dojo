class_name WarriorStatePanel
extends PanelContainer
## Exibe o estado do warrior (HP, posição, direção) e do nível (turno, inimigos)
## para o turno corrente exibido pelo ExecutionControls.

@onready var _hp_label: Label = $VBox/HpLabel
@onready var _pos_label: Label = $VBox/PosLabel
@onready var _dir_label: Label = $VBox/DirLabel
@onready var _turn_label: Label = $VBox/TurnLabel
@onready var _enemies_label: Label = $VBox/EnemiesLabel


func update_state(state: LevelState, turn_num: int, initial_enemies: int) -> void:
	var w := state.warrior()
	_hp_label.text = "HP: %d/%d" % [w.health, w.max_health]
	_pos_label.text = "Pos: %d" % state.warrior_position()
	_dir_label.text = "Dir: %s" % ("→" if state.warrior_facing() > 0 else "←")
	_turn_label.text = "Turno: %d" % turn_num
	_enemies_label.text = "Inimigos: %d/%d" % [state.unit_positions().size(), initial_enemies]
