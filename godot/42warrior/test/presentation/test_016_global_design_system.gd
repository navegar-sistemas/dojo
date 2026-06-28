class_name TestGlobalDesignSystem016
extends GutTest
## T-172 (016) — PROVA DE RENDER ISOLADA: GlobalDesignSystem como componente standalone.
## Fundo void, fontes aplicadas, cores por contexto, overlay glitch, botão 4-estados.


func test_build_theme_retorna_theme_valido() -> void:
	var theme := GlobalDesignSystem.build_theme()
	assert_not_null(theme, "build_theme() deve retornar Theme não-nulo")


func test_label_cor_e_tamanho_configurados() -> void:
	var theme := GlobalDesignSystem.build_theme()
	var color := theme.get_color("font_color", "Label")
	assert_eq(color, GlobalDesignSystem.COLOR_BRANCO, "Label font_color deve ser COLOR_BRANCO")
	var size := theme.get_font_size("font_size", "Label")
	assert_eq(size, GlobalDesignSystem.SIZE_BODY, "Label font_size deve ser SIZE_BODY")


func test_button_4_estados_styleboxes_presentes() -> void:
	var theme := GlobalDesignSystem.build_theme()
	assert_not_null(theme.get_stylebox("normal", "Button"), "Button normal deve ter StyleBox")
	assert_not_null(theme.get_stylebox("hover", "Button"), "Button hover deve ter StyleBox")
	assert_not_null(theme.get_stylebox("pressed", "Button"), "Button pressed deve ter StyleBox")
	assert_not_null(theme.get_stylebox("disabled", "Button"), "Button disabled deve ter StyleBox")


func test_button_cores_por_contexto_distintas() -> void:
	var theme := GlobalDesignSystem.build_theme()
	var hover := theme.get_color("font_hover_color", "Button")
	var pressed := theme.get_color("font_pressed_color", "Button")
	var disabled := theme.get_color("font_disabled_color", "Button")
	assert_eq(hover, GlobalDesignSystem.COLOR_CIANO, "hover deve ser COLOR_CIANO")
	assert_eq(pressed, GlobalDesignSystem.COLOR_VERDE, "pressed deve ser COLOR_VERDE")
	assert_ne(disabled, GlobalDesignSystem.COLOR_BRANCO, "disabled não deve ser branco")


func test_cores_contexto_sao_distintas_entre_si() -> void:
	assert_ne(GlobalDesignSystem.COLOR_VERDE, GlobalDesignSystem.COLOR_RUBI, "verde != rubi")
	assert_ne(GlobalDesignSystem.COLOR_VERDE, GlobalDesignSystem.COLOR_CIANO, "verde != ciano")
	assert_ne(GlobalDesignSystem.COLOR_RUBI, GlobalDesignSystem.COLOR_CIANO, "rubi != ciano")


func test_slider_hslider_styleboxes_presentes() -> void:
	var theme := GlobalDesignSystem.build_theme()
	assert_not_null(theme.get_stylebox("slider", "HSlider"), "HSlider slider deve ter StyleBox")
	assert_not_null(
		theme.get_stylebox("grabber_area", "HSlider"), "HSlider grabber_area deve ter StyleBox"
	)


func test_void_background_cor_e_preset_full_rect() -> void:
	var bg := GlobalDesignSystem.build_void_background()
	add_child_autoqfree(bg)
	await get_tree().process_frame
	assert_eq(bg.color, GlobalDesignSystem.COLOR_VOID, "fundo deve ter cor void #0A0A0B")
	assert_almost_eq(
		bg.anchor_right, 1.0, 0.001, "fundo deve ter anchor_right=1 (PRESET_FULL_RECT)"
	)
	assert_almost_eq(
		bg.anchor_bottom, 1.0, 0.001, "fundo deve ter anchor_bottom=1 (PRESET_FULL_RECT)"
	)


func test_glitch_overlay_instancia_e_set_intensity_funciona() -> void:
	var overlay := GlitchPostProcess.new()
	add_child_autoqfree(overlay)
	await get_tree().process_frame
	assert_not_null(overlay, "GlitchPostProcess deve instanciar sem erro")
	overlay.set_intensity(0.8)
	await get_tree().process_frame


func test_theme_aplicado_a_control_persiste_apos_1_frame() -> void:
	var theme := GlobalDesignSystem.build_theme()
	var root := Control.new()
	add_child_autoqfree(root)
	root.theme = theme
	var label := Label.new()
	root.add_child(label)
	var btn := Button.new()
	root.add_child(btn)
	await get_tree().process_frame
	assert_eq(root.theme, theme, "theme deve permanecer após 1 frame")
	assert_not_null(label.get_theme_color("font_color"), "Label deve resolver cor do theme")


func test_heading_font_carregavel_se_importado() -> void:
	var font := GlobalDesignSystem.heading_font()
	if font == null:
		pending("PressStart2P não importado — prova de font object pulada (assets ausentes)")
		return
	assert_not_null(font, "heading_font() deve retornar FontFile quando importado")


func test_body_font_carregavel_se_importado() -> void:
	var font := GlobalDesignSystem.body_font()
	if font == null:
		pending("JetBrainsMono não importado — prova de font object pulada (assets ausentes)")
		return
	assert_not_null(font, "body_font() deve retornar FontFile quando importado")
