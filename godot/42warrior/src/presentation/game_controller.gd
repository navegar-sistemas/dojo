class_name GameController
extends Node

signal level_won(score_total: int, turns: int, is_ace: bool)
signal level_lost

const MAX_TURNS := 200

var _loader := LevelLoader.new()
var _script_runner := PlayerScriptRunner.new()
var _scoring := ScoringService.new()
var _formatter := TurnEventFormatter.new()

var _level_index := 1
var _definition: LevelDefinition
var _initial_state: LevelState
var _state: LevelState

## Sequência pré-computada de TurnResult — um por turno executado.
var _turn_history: Array = []
## Texto de erro do PlayerScriptRunner para cada turno (paralelo a _turn_history).
var _turn_errors: Array = []

var _display_index := -1
var _level_events: Array = []
var _initial_enemy_count := 0
var _finished := false
var _animating := false
var _last_outcome: TurnResult.Outcome = TurnResult.Outcome.ONGOING
var _last_score: Score
var _last_turns: int = 0
var _timer: Timer

@onready var _dungeon: DungeonView = $DungeonView
@onready var _hud: HudView = $HudView
@onready var _editor: CodeEditorPanel = $EditorLayer/CodeEditorPanel
@onready var _console: TurnConsole = $DebugLayer/DebugPanel/VBox/TurnConsole
@onready var _state_panel: WarriorStatePanel = $DebugLayer/DebugPanel/VBox/WarriorStatePanel
@onready var _controls: ExecutionControls = $DebugLayer/DebugPanel/VBox/ExecutionControls


func _ready() -> void:
	_timer = Timer.new()
	_timer.wait_time = 0.45
	_timer.timeout.connect(_on_tick)
	add_child(_timer)
	_editor.run_pressed.connect(_on_run_pressed)
	_controls.play_pause_toggled.connect(_on_play_pause_toggled)
	_controls.step_requested.connect(_on_step_requested)
	_controls.speed_changed.connect(_on_speed_changed)
	var flow: Node = get_node_or_null("/root/TowerFlow")
	var start_level := 1
	if flow:
		level_won.connect(Callable(flow, "on_level_won"))
		level_lost.connect(Callable(flow, "on_level_lost"))
		start_level = flow.pending_level()
	_load_level(start_level)


func _load_level(index: int) -> void:
	_level_index = index
	_last_outcome = TurnResult.Outcome.ONGOING
	_definition = BeginnerTower.definition(index)
	_initial_state = _loader.load_definition(_definition)
	_state = _initial_state
	_turn_history = []
	_turn_errors = []
	_display_index = -1
	_level_events = []
	_initial_enemy_count = _initial_state.unit_positions().size()
	_finished = false
	_animating = false
	_timer.stop()
	_dungeon.refresh_level(_state)
	_hud.update_hud(_state, 0, _definition.description, 0)
	_state_panel.update_state(_state, 0, _initial_enemy_count)
	_console.clear()
	_controls.set_playing(false)
	_editor.setup_level(index, ReferenceSolutions.for_level(index))


func _on_run_pressed(source: String) -> void:
	var compiled := _script_runner.compile(source)
	if _script_runner.has_error():
		_editor.show_compile_error(_script_runner.error())
		return
	_editor.clear_error()
	_compute_turns(compiled)
	_display_index = -1
	_level_events = []
	_finished = false
	_animating = false
	_state = _initial_state
	_dungeon.refresh_level(_state)
	_hud.update_hud(_state, 0, _definition.description, 0)
	_state_panel.update_state(_state, 0, _initial_enemy_count)
	var texts: PackedStringArray = []
	for i: int in _turn_history.size():
		texts.append(_formatter.format_turn(_turn_history[i].events, _turn_errors[i]))
	_console.populate(Array(texts))
	_controls.set_playing(true)
	_display_index = 0
	_timer.start()


func _compute_turns(compiled: Object) -> void:
	_turn_history = []
	_turn_errors = []
	var resolver := TurnResolver.new()
	var current := _initial_state
	var turns := 0
	while turns < MAX_TURNS:
		var facade := WarriorFacade.new(current)
		var action := _script_runner.play_turn(compiled, facade)
		var error := ""
		if _script_runner.has_error():
			error = _script_runner.error()
		var result := resolver.resolve(current, action)
		_turn_history.append(result)
		_turn_errors.append(error)
		current = result.state
		turns += 1
		if result.outcome != TurnResult.Outcome.ONGOING:
			break


func _on_tick() -> void:
	if _finished or _animating:
		return
	_step()


func _step() -> void:
	if _display_index < 0 or _display_index >= _turn_history.size():
		_finish()
		return
	_animating = true
	var result: TurnResult = _turn_history[_display_index]
	_dungeon.on_turn_result(result, result.state)
	await _dungeon.animations_finished
	_animating = false
	_state = result.state
	_level_events.append_array(result.events)
	var turns := _display_index + 1
	var score := _scoring.score(_level_events, turns, _definition)
	_hud.update_hud(_state, turns, _definition.description, score.total)
	_state_panel.update_state(_state, turns, _initial_enemy_count)
	_console.set_current(_display_index)
	if result.outcome != TurnResult.Outcome.ONGOING:
		_last_outcome = result.outcome
		_last_score = score
		_last_turns = turns
	var audio: Node = get_node_or_null("/root/AudioManager")
	if audio:
		audio.on_events(result.events)
	_display_index += 1
	if result.outcome != TurnResult.Outcome.ONGOING:
		_finish()


func _finish() -> void:
	_finished = true
	_timer.stop()
	_controls.set_playing(false)
	if _last_outcome == TurnResult.Outcome.VICTORY:
		level_won.emit(_last_score.total, _last_turns, _last_score.is_ace())
	elif _last_outcome == TurnResult.Outcome.DEFEAT:
		level_lost.emit()


func _on_play_pause_toggled(playing: bool) -> void:
	if playing and not _finished:
		_timer.start()
	else:
		_timer.stop()


func _on_step_requested() -> void:
	if _finished or _animating:
		return
	_timer.stop()
	_step()


func _on_speed_changed(interval: float) -> void:
	_timer.wait_time = interval
	if not _timer.is_stopped():
		_timer.start()


func _unhandled_input(event: InputEvent) -> void:
	if get_node_or_null("/root/TowerFlow") != null:
		return
	if not (event is InputEventKey and event.pressed and not event.echo):
		return
	match (event as InputEventKey).keycode:
		KEY_ENTER, KEY_KP_ENTER:
			_load_level(_level_index % BeginnerTower.LEVEL_COUNT + 1)
		KEY_R:
			_load_level(_level_index)
