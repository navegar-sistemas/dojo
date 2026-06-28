class_name GlitchPostProcess
extends CanvasLayer
## Pós-processo de glitch: RGB split + scanlines com intensidade escalável (ADR-035).
## Adicionado programaticamente como filho do GameController.
## Intensidade decai automaticamente por frame; definida via set_intensity().

const _SHADER_PATH := "res://src/presentation/glitch_effect_shader.gdshader"
const _DECAY_PER_FRAME := 0.018

var _rect: ColorRect
var _mat: ShaderMaterial
var _intensity: float = 0.0
var _time: float = 0.0


func _ready() -> void:
	layer = 100
	_rect = ColorRect.new()
	_rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_mat = ShaderMaterial.new()
	_mat.shader = load(_SHADER_PATH) as Shader
	_rect.material = _mat
	add_child(_rect)
	_mat.set_shader_parameter("intensity", 0.0)
	_mat.set_shader_parameter("time_val", 0.0)


func set_intensity(value: float) -> void:
	_intensity = clampf(value, 0.0, 1.0)


func _process(delta: float) -> void:
	_time += delta * 60.0
	if _intensity > 0.0:
		_intensity = maxf(0.0, _intensity - _DECAY_PER_FRAME)
	_mat.set_shader_parameter("intensity", _intensity)
	_mat.set_shader_parameter("time_val", _time)
