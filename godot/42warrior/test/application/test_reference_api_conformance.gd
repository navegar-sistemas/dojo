extends GutTest
## DoD de US-011: cada solução-referência usa apenas a API (habilidades do warrior)
## introduzida até aquele nível. A allowlist de um nível N é a união cumulativa de
## BeginnerTower.definition(k).abilities para k em 1..N — fonte única de verdade. Apenas
## chamadas warrior.<metodo>() são restritas; valores de direção (Direction.*) e queries
## de Space (is_enemy/is_captive/...) não são habilidades e não entram na checagem.


func test_cada_solucao_usa_apenas_a_api_introduzida_ate_o_nivel() -> void:
	var re := RegEx.new()
	re.compile("warrior\\.([a-z_]+)\\(")
	for index in range(1, BeginnerTower.LEVEL_COUNT + 1):
		var allowed := {}
		for k in range(1, index + 1):
			for ability in BeginnerTower.definition(k).abilities:
				allowed[ability] = true
		var source := ReferenceSolutions.for_level(index)
		for occurrence in re.search_all(source):
			var method := occurrence.get_string(1)
			assert_true(
				allowed.has(method),
				(
					"L%d: solução chama warrior.%s() fora da allowlist %s"
					% [index, method, str(allowed.keys())]
				)
			)
