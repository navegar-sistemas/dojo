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
##   Corpos INLINE (one-liner) — `func foo(): bar()`, `while c: x()`, `for/if ...: y()` —
##   são NORMALIZADOS para multi-linha ANTES da instrumentação, então os guards os cobrem
##   (sem isso, `func play_turn(w): play_turn(w)` recursava sem guarda e crashava o jogo).
##   Limitação residual: cabeçalho de bloco dentro de string literal não é coberto.
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
	# Normaliza corpos inline (one-liner) para multi-linha ANTES de injetar os guards —
	# sem isso, `func f(w): play_turn(w)` ou `while c: x()` escapam da instrumentação.
	var normalized := _normalize_inline_blocks(source)
	# Variáveis de controle precisam ser declaradas APÓS `extends` (GDScript exige
	# extends antes de qualquer membro). Flag rastreia se a injeção já ocorreu.
	var counter_injected := false
	# Flag: a próxima linha não-vazia não-comentário é a primeira do corpo de uma func.
	var inject_func_guard := false
	for line: String in normalized.split("\n"):
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


## Quebra cabeçalhos de bloco com corpo inline (`func f(): x()`, `while c: x()`) em
## múltiplas linhas, para que os guards de while/func sejam injetados também neles.
## Aplica recursivamente (cobre `func f(w): while true: x()`). Sem isso, um one-liner
## recursivo (`func play_turn(w): play_turn(w)`) escapa do depth-guard e crasha o jogo.
func _normalize_inline_blocks(source: String) -> String:
	var out := PackedStringArray()
	for line: String in source.split("\n"):
		_split_inline(line, out)
	return "\n".join(out)


## Acrescenta `line` a `out`, já normalizada: se for cabeçalho de bloco com corpo inline,
## emite o cabeçalho até o `:` e re-processa o corpo numa linha indentada +1 tab.
func _split_inline(line: String, out: PackedStringArray) -> void:
	if not _is_block_header(line.strip_edges()):
		out.append(line)
		return
	var colon := _statement_colon(line)
	if colon == -1:
		out.append(line)
		return
	var body := line.substr(colon + 1).strip_edges()
	# Corpo vazio ou só comentário → bloco multi-linha normal, nada a quebrar.
	if body == "" or body.begins_with("#"):
		out.append(line)
		return
	var indent := line.substr(0, line.length() - line.lstrip("\t").length())
	out.append(line.substr(0, colon + 1))
	_split_inline("%s\t%s" % [indent, body], out)


## Verdadeiro se a linha (já sem indentação) inicia um bloco que aceita corpo indentado.
func _is_block_header(stripped: String) -> bool:
	for kw: String in ["func ", "static func ", "while ", "for ", "if ", "elif ", "match "]:
		if stripped.begins_with(kw):
			return true
	return stripped == "else:" or stripped.begins_with("else:")


## Índice do `:` que TERMINA o cabeçalho do bloco, ciente de parênteses/colchetes/chaves
## e de strings (não confunde com `:` de dict-literal ou de param tipado). -1 se não houver.
func _statement_colon(line: String) -> int:
	var depth := 0
	var in_str := false
	var quote := ""
	var i := 0
	var n := line.length()
	while i < n:
		var c := line[i]
		if in_str:
			if c == "\\":
				i += 2
				continue
			if c == quote:
				in_str = false
		elif c == '"' or c == "'":
			in_str = true
			quote = c
		elif c == "(" or c == "[" or c == "{":
			depth += 1
		elif c == ")" or c == "]" or c == "}":
			depth -= 1
		elif c == "#":
			return -1
		elif c == ":" and depth == 0:
			return i
		i += 1
	return -1
