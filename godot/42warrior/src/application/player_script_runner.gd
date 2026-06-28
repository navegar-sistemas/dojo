class_name PlayerScriptRunner
extends RefCounted
## Compila o código GDScript do jogador em runtime e o executa por turno contra a
## WarriorFacade. Entrada não-confiável: falhas de compilação, ausência de play_turn
## ou turno sem ação NÃO travam o jogo — viram erro reportado / no-op.
##
## Detalhe de Application (depende de GDScript da engine, mas não da árvore de cenas).

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
		_error = "Erro de compilação no código do jogador."
		return null
	var instance: Object = script.new()
	if instance == null:
		_error = "Não foi possível instanciar o código do jogador."
		return null
	if not instance.has_method("play_turn"):
		_error = "O código do jogador deve definir play_turn(warrior)."
		return null
	return instance


## Executa um turno: chama play_turn(facade) e devolve a ação escolhida (ou null = no-op).
func play_turn(instance: Object, facade: WarriorFacade) -> Action:
	if instance == null:
		return null
	instance.call("play_turn", facade)
	return facade.chosen_action()
