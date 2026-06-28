extends GutTest
## Cobre o AnimationSequencer (013): fila ordenada de beats, serialização entre
## beats (N+1 só após N concluir), beat concorrente (par causa-efeito) e all_done.


func test_fila_vazia_emite_all_done() -> void:
	var seq := AnimationSequencer.new()
	watch_signals(seq)
	seq.play()
	await wait_for_signal(seq.all_done, 1.0)
	assert_signal_emitted(seq, "all_done")
	assert_eq(seq.sequence_size(), 0)


func test_all_done_nao_e_sincrono_sem_animacao() -> void:
	# Regressão do deadlock (code review): sem animação efetiva, all_done NÃO pode
	# sair SÍNCRONO dentro de play() — senão o `await` do chamador o perde e trava.
	var seq := AnimationSequencer.new()
	watch_signals(seq)
	seq.play()
	assert_signal_not_emitted(seq, "all_done", "all_done síncrono travaria o chamador")
	await wait_for_signal(seq.all_done, 1.0)
	assert_signal_emitted(seq, "all_done", "emite no frame seguinte")


func test_sequence_size_e_consultavel() -> void:
	var host := Node2D.new()
	add_child_autofree(host)
	var seq := AnimationSequencer.new()
	seq.enqueue_beat([_tween_factory(host, "position:x", 5.0)])
	seq.enqueue_beat([_tween_factory(host, "position:y", 5.0)])
	assert_eq(seq.sequence_size(), 2, "dois eventos = dois beats")
	assert_eq(seq.get_sequence().size(), 2, "a fila e consultavel (RF-133)")


func test_enqueue_beat_vazio_e_ignorado() -> void:
	var seq := AnimationSequencer.new()
	seq.enqueue_beat([])
	assert_eq(seq.sequence_size(), 0, "beat sem animacao nao entra na fila")


func test_beat_n_mais_1_so_inicia_apos_n_concluir() -> void:
	# RF-130/RF-132: prova estrutural de serialização — o beat 2 só é construído
	# (factory chamada) depois que o tween do beat 1 termina.
	var host := Node2D.new()
	add_child_autofree(host)
	var seq := AnimationSequencer.new()
	var beat1_concluido := [false]
	var beat1_estava_concluido_quando_beat2_iniciou := [false]

	var f1 := func() -> Tween:
		var tween := host.create_tween()
		tween.tween_property(host, "position:x", 10.0, 0.05)
		tween.finished.connect(func() -> void: beat1_concluido[0] = true)
		return tween
	var f2 := func() -> Tween:
		beat1_estava_concluido_quando_beat2_iniciou[0] = beat1_concluido[0]
		var tween := host.create_tween()
		tween.tween_property(host, "position:y", 10.0, 0.05)
		return tween

	seq.enqueue_beat([f1])
	seq.enqueue_beat([f2])
	seq.play()
	await wait_for_signal(seq.all_done, 2.0)

	assert_true(
		beat1_estava_concluido_quando_beat2_iniciou[0],
		"beat 2 iniciou antes do beat 1 concluir (sem serializacao)"
	)


func test_beat_concorrente_dispara_animacoes_juntas() -> void:
	# RF-131: o par causa-efeito (pulse+hurt) é UM beat com 2 animações tocadas
	# juntas — ambas as factories são chamadas no mesmo beat.
	var host := Node2D.new()
	add_child_autofree(host)
	var seq := AnimationSequencer.new()
	var chamadas := [0]

	var pulse := func() -> Tween:
		chamadas[0] += 1
		var tween := host.create_tween()
		tween.tween_property(host, "scale", Vector2(1.3, 1.3), 0.05)
		return tween
	var hurt := func() -> Tween:
		chamadas[0] += 1
		var tween := host.create_tween()
		tween.tween_property(host, "modulate:a", 0.5, 0.05)
		return tween

	seq.enqueue_beat([pulse, hurt])
	assert_eq(seq.sequence_size(), 1, "o par concorrente e um unico beat")
	seq.play()
	await wait_for_signal(seq.all_done, 2.0)
	assert_eq(chamadas[0], 2, "as duas animacoes do beat concorrente foram disparadas")


func test_all_done_emite_apos_ultimo_beat() -> void:
	var host := Node2D.new()
	add_child_autofree(host)
	var seq := AnimationSequencer.new()
	watch_signals(seq)
	seq.enqueue_beat([_tween_factory(host, "position:x", 5.0)])
	seq.enqueue_beat([_tween_factory(host, "position:y", 5.0)])
	seq.play()
	await wait_for_signal(seq.all_done, 2.0)
	assert_signal_emit_count(seq, "all_done", 1, "all_done emite uma vez, ao fim da sequencia")


func _tween_factory(host: Node2D, prop: String, value: float) -> Callable:
	return func() -> Tween:
		var tween := host.create_tween()
		tween.tween_property(host, prop, value, 0.05)
		return tween
