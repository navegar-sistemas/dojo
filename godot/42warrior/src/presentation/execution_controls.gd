class_name ExecutionControls
extends PanelContainer
## Governa o ritmo de apresentação do loop de turno: play/pause, passo-a-passo
## e velocidade. Emite sinais; quem ouve (GameController) controla o timer.

signal play_pause_toggled(playing: bool)
signal step_requested
signal speed_changed(interval: float)

## Intervalo mínimo (mais rápido) em segundos.
const SPEED_FAST := 0.10
## Intervalo máximo (mais lento) em segundos.
const SPEED_SLOW := 2.0

var _playing := false

@onready var _play_btn: Button = $HBox/PlayBtn
@onready var _step_btn: Button = $HBox/StepBtn
@onready var _speed_slider: HSlider = $HBox/SpeedSlider


func _ready() -> void:
	_play_btn.pressed.connect(_on_play_pressed)
	_step_btn.pressed.connect(_on_step_pressed)
	_speed_slider.min_value = SPEED_FAST
	_speed_slider.max_value = SPEED_SLOW
	_speed_slider.value = 0.45
	_speed_slider.value_changed.connect(_on_speed_changed)


func set_playing(value: bool) -> void:
	_playing = value
	_play_btn.text = "⏸ Pausar" if value else "▶ Retomar"
	_step_btn.disabled = value


func _on_play_pressed() -> void:
	_playing = not _playing
	set_playing(_playing)
	play_pause_toggled.emit(_playing)


func _on_step_pressed() -> void:
	step_requested.emit()


func _on_speed_changed(value: float) -> void:
	speed_changed.emit(value)
