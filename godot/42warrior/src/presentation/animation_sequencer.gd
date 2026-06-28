class_name AnimationSequencer
extends RefCounted
## Orquestra as animações de um turno como uma fila ORDENADA de beats (ADR-030).
## Cada beat só inicia depois que o anterior CONCLUI (await), tornando a
## causalidade legível: andou -> chegou -> reagiu (RF-130). Um beat pode conter
## mais de uma animação CONCORRENTE — o par causa-efeito do mesmo instante, p.ex.
## pulse(atacante)+hurt(alvo) de um ATTACKED, é um único beat (ADR-031/RF-131).
## A fila é consultável (sequence_size/get_sequence) para que um teste prove que
## o beat N+1 só inicia após o N (RF-132/133), sem depender de timing.

signal all_done

## Cada entrada de _beats é um Array de Callable; cada Callable cria e retorna um
## Tween (ou null se não houver sprite). Beats com >1 Callable são concorrentes.
var _beats: Array = []
var _playing := false


## Enfileira um beat. `factories` são Callables que, ao serem chamadas no momento
## de tocar o beat, criam os tweens concorrentes daquele beat e os retornam.
func enqueue_beat(factories: Array) -> void:
	if factories.is_empty():
		return
	_beats.append(factories)


func sequence_size() -> int:
	return _beats.size()


func is_empty() -> bool:
	return _beats.is_empty()


## Cópia rasa da fila — consultável por testes (RF-133). Não expõe a fila interna.
func get_sequence() -> Array:
	return _beats.duplicate()


## Toca os beats em ordem: cria TODOS os tweens de um beat antes de aguardar
## (para que sejam concorrentes dentro do beat) e só passa ao próximo beat depois
## que todos concluem. Emite all_done ao fim da sequência (inclusive se vazia).
func play() -> void:
	if _playing:
		return
	_playing = true
	for beat: Array in _beats:
		var tweens: Array = []
		for factory: Callable in beat:
			var tween: Tween = factory.call()
			if tween != null:
				tweens.append(tween)
		for tween: Tween in tweens:
			if tween.is_valid():
				await tween.finished
	_playing = false
	all_done.emit()
