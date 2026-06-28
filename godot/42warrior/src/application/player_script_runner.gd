class_name PlayerScriptRunner
extends RefCounted
## Fronteira ÚNICA de execução do código do jogador (ADR-032). Entrada não-confiável:
## - Sintaxe inválida → compile() reporta e devolve null (RF-140).
## - Erro de runtime em play_turn (método inexistente, null, tipo) → GDScript aborta
##   a função do jogador sem derrubar o processo; o turno vira no-op (RF-141).
## - Loop infinito → o source é INSTRUMENTADO antes de compilar: cada `while C:` vira
##   `while (C) and __guard():`, e __guard() corta o laço após um teto de iterações
##   (LOOP_ITERATION_LIMIT). Sem thread (que crasha) e sem travar o jogo; o turno
##   atingido vira no-op + erro reportado (RF-142). `for` em GDScript itera sobre
##   coleção finita (não é fonte de laço infinito); recursão infinita estoura a pilha
##   e aborta nativamente como um erro de runtime.
##   Limitação conhecida: a instrumentação é textual (não-AST) — `while` dentro de
##   string literal ou em uma linha sintaticamente exótica pode não ser coberto.
##
## Detalhe de Application (depende de GDScript da engine, não da árvore de cenas).

## Teto de iterações de um único laço por turno. Alto o bastante para qualquer laço
## legítimo do jogador; baixo o bastante para cortar um loop infinito em tempo hábil.
const LOOP_ITERATION_LIMIT := 1_000_000
const _GUARD_COUNTER := "__guard_count"

var _error: String


func _init() -> void:
	_error = ""


func has_error() -> bool:
	return _error != ""


func error() -> String:
	return _error


## Compila o código (instrumentado) e devolve uma instância com play_turn, ou null.
func compile(source: String) -> Object:
	_error = ""
	var script := GDScript.new()
	script.source_code = _instrument(source)
	if script.reload() != OK:
		_error = "Erro de compilação: o código do jogador tem sintaxe inválida."
		return null
	var instance: Object = script.new()
	if instance == null:
		_error = "Não foi possível instanciar o código do jogador."
		return null
	if not instance.has_method("play_turn"):
		_error = "O código do jogador deve definir play_turn(warrior)."
		return null
	return instance


## Executa um turno e devolve a ação escolhida (ou null = no-op). Erro de runtime
## vira no-op (RF-141); laço que estoura o teto é cortado e reportado (RF-142).
func play_turn(instance: Object, facade: WarriorFacade) -> Action:
	_error = ""
	if instance == null:
		return null
	instance.set(_GUARD_COUNTER, 0)
	instance.call("play_turn", facade)
	if int(instance.get(_GUARD_COUNTER)) >= LOOP_ITERATION_LIMIT:
		_error = (
			"Execução interrompida: possível loop infinito no play_turn"
			+ " (limite de iterações atingido)."
		)
	return facade.chosen_action()


## Injeta a guarda de iteração: um contador + método __guard() e reescreve cada
## cabeçalho `while` para consultar a guarda a cada iteração.
func _instrument(source: String) -> String:
	var out := PackedStringArray()
	# O contador precisa ser declarado APÓS o `extends` (GDScript exige extends antes
	# de qualquer membro), logo depois dessa linha.
	var counter_injected := false
	for line: String in source.split("\n"):
		out.append(_guard_while(line))
		if not counter_injected and line.strip_edges().begins_with("extends"):
			out.append("var %s := 0" % _GUARD_COUNTER)
			counter_injected = true
	if not counter_injected:
		out.insert(0, "var %s := 0" % _GUARD_COUNTER)
	out.append("func __guard() -> bool:")
	out.append("\t%s += 1" % _GUARD_COUNTER)
	out.append("\treturn %s < %d" % [_GUARD_COUNTER, LOOP_ITERATION_LIMIT])
	return "\n".join(out)


## Reescreve `<indent>while <cond>:<resto>` para consultar __guard() por iteração;
## linhas que não são cabeçalho de while passam intactas.
func _guard_while(line: String) -> String:
	var while_pos := line.find("while ")
	if while_pos == -1 or line.substr(0, while_pos).strip_edges() != "":
		return line
	var colon := line.find(":", while_pos)
	if colon == -1:
		return line
	var indent := line.substr(0, while_pos)
	var cond := line.substr(while_pos + 6, colon - while_pos - 6).strip_edges()
	var rest := line.substr(colon + 1)
	return "%swhile (%s) and __guard():%s" % [indent, cond, rest]
