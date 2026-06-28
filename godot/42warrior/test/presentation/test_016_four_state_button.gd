extends GutTest
## T-162 (016) — PROVA DE RENDER ISOLADA: FourStateButton 4 estados data-driven.
## Instancia FourStateButton sem game.tscn e assere que os 4 StyleBoxes
## existem, são distintos e refletem os estados normal/hover/pressed/disabled.


func test_four_styleboxes_all_present() -> void:
	var btn := FourStateButton.new()
	add_child_autoqfree(btn)
	await get_tree().process_frame

	assert_not_null(btn.style_normal, "normal StyleBox deve existir")
	assert_not_null(btn.style_hover, "hover StyleBox deve existir")
	assert_not_null(btn.style_pressed, "pressed StyleBox deve existir")
	assert_not_null(btn.style_disabled, "disabled StyleBox deve existir")


func test_normal_has_ciano_border() -> void:
	var btn := FourStateButton.new()
	add_child_autoqfree(btn)
	await get_tree().process_frame

	var normal := btn.style_normal
	assert_not_null(normal, "style_normal deve ser StyleBoxFlat")
	# Ciano #00F0FF: R=0, G≈0.94, B=1.0
	assert_almost_eq(normal.border_color.r, 0.0, 0.05, "normal border_color.r deve ser ~0 (ciano)")
	assert_almost_eq(normal.border_color.b, 1.0, 0.1, "normal border_color.b deve ser ~1.0 (ciano)")


func test_hover_bg_differs_from_normal() -> void:
	var btn := FourStateButton.new()
	add_child_autoqfree(btn)
	await get_tree().process_frame

	assert_ne(
		btn.style_hover.bg_color,
		btn.style_normal.bg_color,
		"hover.bg_color deve diferir de normal (preenchido+glow)"
	)


func test_pressed_has_wider_border_than_normal() -> void:
	var btn := FourStateButton.new()
	add_child_autoqfree(btn)
	await get_tree().process_frame

	assert_gt(
		btn.style_pressed.border_width_top,
		btn.style_normal.border_width_top,
		"pressed deve ter borda +1px mais larga que normal"
	)


func test_disabled_has_gray_border() -> void:
	var btn := FourStateButton.new()
	add_child_autoqfree(btn)
	await get_tree().process_frame

	var bc := btn.style_disabled.border_color
	# Cinza: R ≈ G ≈ B (neutro, não ciano)
	assert_almost_eq(bc.r, bc.g, 0.05, "disabled border deve ser neutro (cinza): r ≈ g")
	assert_almost_eq(bc.g, bc.b, 0.05, "disabled border deve ser neutro (cinza): g ≈ b")


func test_render_proof_control_bar_visible() -> void:
	var bar := HBoxContainer.new()
	var btn_play := FourStateButton.new()
	btn_play.text = "▶ Retomar"
	var btn_step := FourStateButton.new()
	btn_step.text = "Passo"
	btn_step.disabled = true
	bar.add_child(btn_play)
	bar.add_child(btn_step)
	add_child_autoqfree(bar)

	await get_tree().process_frame

	assert_true(btn_play.visible, "botão play deve estar visível na barra de controles")
	assert_true(btn_step.visible, "botão step deve estar visível na barra de controles")
	assert_not_null(btn_play.style_normal, "botão play deve ter style_normal configurado")
	assert_not_null(btn_step.style_disabled, "botão step deve ter style_disabled configurado")
