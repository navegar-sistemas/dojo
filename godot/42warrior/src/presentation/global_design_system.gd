class_name GlobalDesignSystem
extends RefCounted
## Design system data-driven do 42warrior (ADR-042, RNF-063).
## Fonte única: zero cor, fonte ou tamanho hardcoded fora daqui.
## Chame build_theme() para obter o Theme Godot; injete na raiz ou em controles.

# ── Paleta ───────────────────────────────────────────────────────────────────
const COLOR_VOID := Color(0.039, 0.039, 0.043, 1.0)  # #0A0A0B
const COLOR_GRAFITE := Color(0.110, 0.110, 0.118, 1.0)  # #1C1C1E
const COLOR_GRAFITE_MID := Color(0.180, 0.180, 0.192, 1.0)  # #2E2E31
const COLOR_VERDE := Color(0.0, 1.0, 0.4, 1.0)  # #00FF66 — sucesso
const COLOR_RUBI := Color(1.0, 0.0, 0.235, 1.0)  # #FF003C — perigo
const COLOR_CIANO := Color(0.0, 0.941, 1.0, 1.0)  # #00F0FF — info/hover
const COLOR_BRANCO := Color(0.910, 0.910, 0.910, 1.0)  # #E8E8E8
const COLOR_MUTED := Color(0.45, 0.45, 0.47, 1.0)  # texto desabilitado

# ── Fontes ───────────────────────────────────────────────────────────────────
const _FONT_HEADING_PATH := "res://design_files/v1/fonts/PressStart2P-Regular.ttf"
const _FONT_BODY_PATH := "res://design_files/v1/fonts/JetBrainsMono-Regular.ttf"
const _FONT_BOLD_PATH := "res://design_files/v1/fonts/JetBrainsMono-Bold.ttf"

# ── Tamanhos ──────────────────────────────────────────────────────────────────
const SIZE_HEADING := 16
const SIZE_BODY := 14
const SIZE_SMALL := 11


static func build_theme() -> Theme:
	var theme := Theme.new()
	var font_body: FontFile = _load_font(_FONT_BODY_PATH)
	var font_bold: FontFile = _load_font(_FONT_BOLD_PATH)
	_apply_label_theme(theme, font_body, font_bold)
	_apply_button_theme(theme, font_body)
	_apply_slider_theme(theme)
	return theme


static func heading_font() -> FontFile:
	return _load_font(_FONT_HEADING_PATH)


static func body_font() -> FontFile:
	return _load_font(_FONT_BODY_PATH)


static func build_void_background() -> ColorRect:
	var bg := ColorRect.new()
	bg.color = COLOR_VOID
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	return bg


static func _load_font(path: String) -> FontFile:
	if ResourceLoader.exists(path):
		return load(path) as FontFile
	return null


static func _apply_label_theme(theme: Theme, font_body: FontFile, font_bold: FontFile) -> void:
	if font_body != null:
		theme.set_font("font", "Label", font_body)
		theme.set_font("font", "LineEdit", font_body)
		theme.set_font("font", "CodeEdit", font_body)
		theme.set_font("normal_font", "RichTextLabel", font_body)
	if font_bold != null:
		theme.set_font("bold_font", "RichTextLabel", font_bold)
	theme.set_font_size("font_size", "Label", SIZE_BODY)
	theme.set_font_size("font_size", "LineEdit", SIZE_BODY)
	theme.set_font_size("font_size", "CodeEdit", SIZE_BODY)
	theme.set_font_size("normal_font_size", "RichTextLabel", SIZE_BODY)
	theme.set_color("font_color", "Label", COLOR_BRANCO)
	theme.set_color("font_color", "LineEdit", COLOR_BRANCO)
	theme.set_color("default_color", "RichTextLabel", COLOR_BRANCO)


static func _apply_button_theme(theme: Theme, font_body: FontFile) -> void:
	if font_body != null:
		theme.set_font("font", "Button", font_body)
	theme.set_font_size("font_size", "Button", SIZE_BODY)
	theme.set_color("font_color", "Button", COLOR_BRANCO)
	theme.set_color("font_hover_color", "Button", COLOR_CIANO)
	theme.set_color("font_pressed_color", "Button", COLOR_VERDE)
	theme.set_color("font_disabled_color", "Button", COLOR_MUTED)
	theme.set_color("font_focus_color", "Button", COLOR_CIANO)
	theme.set_stylebox("normal", "Button", _button_style(COLOR_GRAFITE, Color.TRANSPARENT, 0))
	theme.set_stylebox("hover", "Button", _button_style(COLOR_GRAFITE_MID, COLOR_CIANO, 1))
	theme.set_stylebox("pressed", "Button", _button_style(COLOR_GRAFITE, COLOR_VERDE, 1))
	theme.set_stylebox("disabled", "Button", _button_style(COLOR_VOID, COLOR_GRAFITE, 1))
	theme.set_stylebox("focus", "Button", _button_style(COLOR_GRAFITE_MID, COLOR_CIANO, 1))


static func _apply_slider_theme(theme: Theme) -> void:
	var bg := StyleBoxFlat.new()
	bg.bg_color = COLOR_GRAFITE
	bg.corner_radius_top_left = 2
	bg.corner_radius_top_right = 2
	bg.corner_radius_bottom_left = 2
	bg.corner_radius_bottom_right = 2
	var fill := StyleBoxFlat.new()
	fill.bg_color = COLOR_VERDE
	fill.corner_radius_top_left = 2
	fill.corner_radius_top_right = 2
	fill.corner_radius_bottom_left = 2
	fill.corner_radius_bottom_right = 2
	theme.set_stylebox("slider", "HSlider", bg)
	theme.set_stylebox("grabber_area", "HSlider", fill)


static func _button_style(bg: Color, border: Color, bwidth: int) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.border_width_top = bwidth
	s.border_width_right = bwidth
	s.border_width_bottom = bwidth
	s.border_width_left = bwidth
	s.corner_radius_top_left = 2
	s.corner_radius_top_right = 2
	s.corner_radius_bottom_left = 2
	s.corner_radius_bottom_right = 2
	s.content_margin_left = 8.0
	s.content_margin_right = 8.0
	s.content_margin_top = 4.0
	s.content_margin_bottom = 4.0
	return s
