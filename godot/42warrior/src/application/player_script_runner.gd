class_name PlayerScriptRunner
extends RefCounted
## Fronteira ÚNICA de execução do código do jogador (ADR-032). Entrada não-confiável:
## - Sintaxe inválida → compile() reporta e devolve null (RF-140).
## - Erro de runtime em play_turn (método inexistente, null, tipo) → GDScript aborta
##   a função do jogador sem derrubar o processo; o turno vira no-op (RF-141).
##
## RF-142 (loop/recursão infinita) — LIMITAÇÃO CONHECIDA, ainda NÃO resolvida aqui:
## GDScript é síncrono e sem try/catch. Não há mecanismo seguro de interromper um
## `while true` no mesmo thread (trava o jogo), e executar o turno numa Thread com
## tempo-limite foi DESCARTADO por evidência empírica: erro de runtime/recursão do
## jogador dentro de uma Thread crasha o processo (Bus error) — pior que o problema.
## A escolha do mecanismo está escalada (instrumentar o source com guarda de iteração
## vs. sandbox em processo separado). Até lá, esta fronteira cobre sintaxe + runtime.
##
## Detalhe de Application (depende de GDScript da engine, não da árvore de cenas).

var _error: String


func _init() -> void:
	_error = ""


func has_error() -> bool:
	return _error != ""


func error() -> String:
	return _error


## Compila o código e devolve uma instância com play_turn, ou null (com has_error()).
func compile(source: String) -> Object:
	_error = ""
	var script := GDScript.new()
	script.source_code = source
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


## Executa um turno: chama play_turn(facade) e devolve a ação escolhida (ou null =
## no-op). Um erro de runtime no código do jogador aborta a função sem crashar o
## jogo: nenhuma ação é registrada, o turno vira no-op e o jogador pode corrigir e
## rodar de novo (RF-141).
func play_turn(instance: Object, facade: WarriorFacade) -> Action:
	_error = ""
	if instance == null:
		return null
	instance.call("play_turn", facade)
	return facade.chosen_action()
