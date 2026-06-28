class_name PlayerScriptRunner
extends RefCounted
## Fronteira ÚNICA de execução do código do jogador (ADR-032). Entrada não-confiável:
## - Sintaxe inválida → compile() reporta e devolve null (RF-140).
## - Erro de runtime em play_turn (método inexistente, null, tipo) → GDScript aborta
##   a função do jogador sem derrubar o processo; o turno vira no-op (RF-141).
## - Loop infinito → o source é INSTRUMENTADO antes de compilar: cada `while C:` vira
##   `while (C) and __guard():`, e __guard() corta o laço após um teto de iterações
##   (LOOP_ITERATION_LIMIT). Sem thread (que crasha) e sem travar o jogo; o turno
##   atingido vira no-op + erro reportado (RF-142).
## - Recursão infinita → cada `func` do jogador é instrumentada com __enter_func():
##   se a profundidade de chamada exceder CALL_DEPTH_LIMIT, a função retorna imediatamente;
##   o turno vira no-op + erro reportado (RF-143). GDScript não tem try/catch para
##   stack overflow — o guard PREVINE, não reage.
##   Limitações conhecidas (instrumentação textual, não-AST): `while` em string literal
##   pode não ser coberto; `func` one-liner (`func foo(): pass`) não é instrumentado.
##
## Detalhe de Application (depende de GDScript da engine, não da árvore de cenas).

## Teto de iterações de um único laço por turno.
const LOOP_ITERATION_LIMIT := 1_000_000
## Teto de profundidade de chamada por turno (previne recursão infinita, RF-143).
const CALL_DEPTH_LIMIT := 64
const _GUARD_COUNTER := "__guard_count"
const _DEPTH_VAR := "__depth"

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


## Executa um turno e devolve a ação escolhida (ou null = no-op). Erros de runtime
## viram no-op (RF-141); laço que estoura o teto é cortado e reportado (RF-142);
## recursão que excede o teto é bloqueada e reportada (RF-143).
func play_turn(instance: Object, facade: WarriorFacade) -> Action:
	_error = ""
	if instance == null:
		return null
	instance.set(_GUARD_COUNTER, 0)
	instance.set(_DEPTH_VAR, 0)
	instance.call("play_turn", facade)
	if int(instance.get(_GUARD_COUNTER)) >= LOOP_ITERATION_LIMIT:
		_error = (
			"Execução interrompida: possível loop infinito no play_turn"
			+ " (limite de iterações atingido)."
		)
	elif int(instance.get(_DEPTH_VAR)) > CALL_DEPTH_LIMIT:
		_error = (
			"Execução interrompida: possível recursão infinita no play_turn"
			+ " (limite de profundidade de chamada atingido)."
		)
	return facade.chosen_action()


## Injeta guardas de iteração (while) e profundidade (func) para prevenir loops e
## recursões infinitas. Também injeta as variáveis de controle e os métodos __guard()
## e __enter_func().
func _instrument(source: String) -> String:
	var out := PackedStringArray()
	# Variáveis de controle precisam ser declaradas APÓS `extends` (GDScript exige
	# extends antes de qualquer membro). Flag rastreia se a injeção já ocorreu.
	var counter_injected := false
	# Flag: a próxima linha não-vazia não-comentário é a primeira do corpo de uma func.
	var inject_func_guard := false
	for line: String in source.split("\n"):
		if inject_func_guard:
			var stripped_line := line.strip_edges()
			if stripped_line != "" and not stripped_line.begins_with("#"):
				inject_func_guard = false
				var indent_count := line.length() - line.lstrip("\t").length()
				out.append("%sif not __enter_func(): return" % "\t".repeat(indent_count))
		out.append(_guard_while(line))
		if not counter_injected and line.strip_edges().begins_with("extends"):
			out.append("var %s := 0" % _GUARD_COUNTER)
			out.append("var %s := 0" % _DEPTH_VAR)
			counter_injected = true
		var stripped := line.strip_edges()
		if stripped.begins_with("func ") and not stripped.begins_with("func __"):
			inject_func_guard = false
			var no_comment := stripped.split("#")[0].strip_edges()
			if no_comment.ends_with(":"):
				inject_func_guard = true
	if not counter_injected:
		out.insert(0, "var %s := 0" % _DEPTH_VAR)
		out.insert(0, "var %s := 0" % _GUARD_COUNTER)
	out.append("func __guard() -> bool:")
	out.append("\t%s += 1" % _GUARD_COUNTER)
	out.append("\treturn %s < %d" % [_GUARD_COUNTER, LOOP_ITERATION_LIMIT])
	out.append("func __enter_func() -> bool:")
	out.append("\t%s += 1" % _DEPTH_VAR)
	out.append("\treturn %s <= %d" % [_DEPTH_VAR, CALL_DEPTH_LIMIT])
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
