extends Node
## Autoload "ScreenManager" — troca atômica de telas (uma-tela-por-vez).
## change_to(path) monta a nova cena sob o root, define current_scene
## e libera (queue_free) a anterior, garantindo exatamente 1 tela de topo viva.


func change_to(path: String) -> void:
	var prev: Node = get_tree().current_scene
	var next: Node = (load(path) as PackedScene).instantiate()
	get_tree().root.add_child(next)
	get_tree().current_scene = next
	if prev != null:
		prev.queue_free()
