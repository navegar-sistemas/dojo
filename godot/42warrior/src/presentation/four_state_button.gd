class_name FourStateButton
extends Button
## Botão 4-estados data-driven: normal (borda ciano) / hover (preenchido+glow) /
## pressed (escurecido, +1px borda) / disabled (cinza). ADR-042 / RF-165.

const _CIANO := Color(0.0, 0.941, 1.0)
const _BG_HOVER := Color(0.0, 0.941, 1.0, 0.15)
const _BG_PRESSED := Color(0.0, 0.941, 1.0, 0.28)
const _GRAFITE := Color(0.35, 0.35, 0.35)
const _GRAFITE_BG := Color(0.12, 0.12, 0.12)
const _TRANSPARENT := Color(0.0, 0.0, 0.0, 0.0)
const _CORNER := 4
const _PADDING_H := 8.0
const _PADDING_V := 4.0

var style_normal: StyleBoxFlat
var style_hover: StyleBoxFlat
var style_pressed: StyleBoxFlat
var style_disabled: StyleBoxFlat


func _ready() -> void:
	_apply_styles()


func _apply_styles() -> void:
	style_normal = _build_normal()
	style_hover = _build_hover()
	style_pressed = _build_pressed()
	style_disabled = _build_disabled()
	add_theme_stylebox_override("normal", style_normal)
	add_theme_stylebox_override("hover", style_hover)
	add_theme_stylebox_override("pressed", style_pressed)
	add_theme_stylebox_override("disabled", style_disabled)
	add_theme_stylebox_override("focus", style_normal)


func _build_normal() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = _TRANSPARENT
	s.set_border_width_all(1)
	s.border_color = _CIANO
	s.set_corner_radius_all(_CORNER)
	s.content_margin_left = _PADDING_H
	s.content_margin_right = _PADDING_H
	s.content_margin_top = _PADDING_V
	s.content_margin_bottom = _PADDING_V
	return s


func _build_hover() -> StyleBoxFlat:
	var s := _build_normal()
	s.bg_color = _BG_HOVER
	s.shadow_color = Color(_CIANO, 0.5)
	s.shadow_size = 4
	return s


func _build_pressed() -> StyleBoxFlat:
	var s := _build_normal()
	s.bg_color = _BG_PRESSED
	s.set_border_width_all(2)
	return s


func _build_disabled() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = _GRAFITE_BG
	s.set_border_width_all(1)
	s.border_color = _GRAFITE
	s.set_corner_radius_all(_CORNER)
	s.content_margin_left = _PADDING_H
	s.content_margin_right = _PADDING_H
	s.content_margin_top = _PADDING_V
	s.content_margin_bottom = _PADDING_V
	return s
