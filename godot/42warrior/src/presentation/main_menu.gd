class_name MainMenu
extends PanelContainer
## Menu principal: iniciar/continuar, controles de volume música e SFX (DoD T-055).

signal start_requested(level: int)

var _store: ProgressStore

@onready var _start_btn: Button = $VBox/StartBtn
@onready var _continue_btn: Button = $VBox/ContinueBtn
@onready var _music_slider: HSlider = $VBox/VolumeBox/MusicSlider
@onready var _sfx_slider: HSlider = $VBox/VolumeBox/SfxSlider


func _ready() -> void:
	_store = ProgressStore.new()
	_start_btn.pressed.connect(_on_start_pressed)
	_continue_btn.pressed.connect(_on_continue_pressed)
	_continue_btn.disabled = not _store.has_save()
	_music_slider.value = _store.vol_music()
	_sfx_slider.value = _store.vol_sfx()
	_music_slider.value_changed.connect(_on_music_vol_changed)
	_sfx_slider.value_changed.connect(_on_sfx_vol_changed)


func _on_start_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.start(1)
	else:
		start_requested.emit(1)


func _on_continue_pressed() -> void:
	var flow: Node = get_node_or_null("/root/TowerFlow")
	if flow:
		flow.start(_store.current_level())
	else:
		start_requested.emit(_store.current_level())


func _on_music_vol_changed(value: float) -> void:
	var audio: Node = get_node_or_null("/root/AudioManager")
	if audio:
		audio.set_vol_music(value)
	_store.save_volume(value, _sfx_slider.value)


func _on_sfx_vol_changed(value: float) -> void:
	var audio: Node = get_node_or_null("/root/AudioManager")
	if audio:
		audio.set_vol_sfx(value)
	_store.save_volume(_music_slider.value, value)
