extends GutTest
## Ponta-a-ponta: cada solução-referência vence o seu nível (RF-013).

# L8 reincluído: a fase de inimigos passou a decidir sobre o snapshot do início do turno
# (EnemyPhase de 2 etapas, fiel ao prepare/perform do gem), então o warrior não leva os 2
# tiros de 11 no mesmo turno — dá para enfrentar um wizard por vez. Tópico: fidelidade-combate.
const SOLVABLE_LEVELS := [1, 2, 3, 4, 5, 6, 7, 8, 9]


func test_cada_nivel_solucionavel_e_vencido_pela_solucao_referencia() -> void:
	var loader := LevelLoader.new()
	var runner := LevelRunner.new()
	for index in SOLVABLE_LEVELS:
		var state := loader.load_level(index)
		var result: Dictionary = runner.run(state, ReferenceSolutions.for_level(index))
		assert_eq(
			result["outcome"],
			TurnResult.Outcome.VICTORY,
			"L%d outcome=%d turns=%d" % [index, result["outcome"], result["turns"]]
		)
