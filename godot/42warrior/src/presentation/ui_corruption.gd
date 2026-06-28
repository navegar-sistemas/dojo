class_name UiCorruption
extends CanvasLayer
## Corrupção progressiva da UI por andar (ADR-035, RF-153).
## Aplica overlay de scanlines determinístico por andar; intensidade lida do ThemeCatalog.

const _SHADER_PATH := "res://src/presentation/glitch_effect_shader.gdshader"
## Fator de escala: a corrupção da UI é mais sutil que o pós-processo de evento.
const _UI_SCALE := 0.35

var _rect: ColorRect
var _mat: ShaderMaterial
var _time: float = 0.0


func _ready() -> void:
	layer = 50
	_rect = ColorRect.new()
	_rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_mat = ShaderMaterial.new()
	_mat.shader = load(_SHADER_PATH) as Shader
	_rect.material = _mat
	add_child(_rect)
	_mat.set_shader_parameter("intensity", 0.0)
	_mat.set_shader_parameter("time_val", 0.0)


func set_floor(floor_index: int) -> void:
	var base := ThemeCatalog.corruption_for_floor(floor_index)
	_mat.set_shader_parameter("intensity", base * _UI_SCALE)


func _process(delta: float) -> void:
	_time += delta * 60.0
	_mat.set_shader_parameter("time_val", _time)
