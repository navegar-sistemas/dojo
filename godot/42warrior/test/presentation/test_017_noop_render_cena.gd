extends GutTest
## T-170 (017) follow-up: prova de CENA REAL.
## Carrega game.tscn, executa 1 turno no-op (script vazio = WarriorFacade.action() → null →
## NO_OP), renderiza >=1 frame e afirma que display_index avançou (loop não congelou).
##
## Complementa test_017_noop_cena.gd (AnimationSequencer em isolamento) com runtime completo:
## game_controller._step() → DungeonView.on_turn_result() → AnimationSequencer.play()
## (fila vazia, sem tween) → all_done deferred → animations_finished → loop avança.

const _SCENE := "res://scenes/game.tscn"
const _WAIT_S := 1.0  # > 0.45 s (intervalo padrão do timer de turno)


func test_turno_noop_em_cena_real_nao_congela() -> void:
	var packed: PackedScene = load(_SCENE)
	var game_view: Node = packed.instantiate()
	add_child_autoqfree(game_view)

	# _ready roda: cria Timer, carrega nível 1, conecta sinais
	await get_tree().process_frame
	await get_tree().process_frame

	# No-op: play_turn sem nenhuma chamada → WarriorFacade.action() → null → NO_OP
	var script_noop := "func play_turn(warrior):\n\tpass"
	game_view._on_run_pressed(script_noop)

	# Aguarda Timer disparar (0.45 s) + AnimationSequencer all_done deferred (1 frame)
	await wait_seconds(_WAIT_S)

	assert_true(
		game_view._display_index > 0 or game_view._finished,
		"display_index > 0 ou _finished=true: loop de turnos avançou sem congelar"
	)
