extends GutTest
## T-170 (017): prova de CENA que um turno sem animação (no-op/pivot/parede)
## não congela o loop de turnos do game_controller.
##
## O mecanismo que previne o deadlock vive em AnimationSequencer.play(): quando
## nenhum tween é criado (awaited=false), all_done é DIFERIDO um frame via
## process_frame — evitando que o `await seq.all_done` do chamador perca o sinal.
##
## Prova UNITÁRIA do mecanismo (013, não reimplementada aqui):
##   test/presentation/test_animation_sequencer.gd
##   → test_all_done_nao_e_sincrono_sem_animacao
##
## Este teste acrescenta a prova de RUNTIME com SceneTree ativa (headless),
## usando a mesma instância de AnimationSequencer que game_controller._step()
## usa internamente, provando que o loop de turnos AVANÇA ao próximo tick.


func test_turno_noop_nao_congela_o_loop_de_turnos() -> void:
	# Equivalente ao caminho: game_controller._step() → seq.play() (fila vazia,
	# turno sem animação: pivot, andar na parede, etc.) → all_done → _advance_display().
	var seq := AnimationSequencer.new()
	watch_signals(seq)

	seq.play()  # fila vazia = nenhuma animação = turno no-op

	# all_done NÃO pode sair síncrono: o `await seq.all_done` de _step() o perderia.
	assert_signal_not_emitted(seq, "all_done", "all_done síncrono travaria game_controller._step()")

	# Após um frame (process_frame), all_done dispara e o loop avança.
	await wait_for_signal(seq.all_done, 1.0)
	assert_signal_emitted(seq, "all_done", "all_done emite no frame seguinte — loop avança")
