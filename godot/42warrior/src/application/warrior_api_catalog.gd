class_name WarriorApiCatalog
extends RefCounted
## Resolve, a partir das definições da tower (domínio), o conjunto cumulativo de
## ações/sentidos disponíveis até o nível atual, com assinatura e descrição curta.
## Sem hardcode de lista em cena (RNF-070) e sem API de cena neste arquivo (arch_guard).


static func entries_for_level(level_index: int) -> Array:
	var unlocked := _cumulative_abilities(level_index)
	var result: Array = []
	for entry: Dictionary in _all_entry_data():
		if unlocked.has(entry["name"]):
			result.append(entry)
	return result


static func _cumulative_abilities(level_index: int) -> PackedStringArray:
	var cumulative := PackedStringArray()
	var capped := clampi(level_index, 1, BeginnerTower.LEVEL_COUNT)
	for i: int in range(1, capped + 1):
		cumulative.append_array(BeginnerTower.definition(i).abilities)
	return cumulative


static func _all_entry_data() -> Array:
	return [
		{
			"name": "walk",
			"signature": "walk(direction: Direction = forward())",
			"description": "Move o warrior uma tile na direção.",
			"kind": "action",
		},
		{
			"name": "feel",
			"signature": "feel(direction: Direction = forward()) -> Space",
			"description": "Retorna o espaço adjacente: parede, inimigo, cativo, escada ou vazio.",
			"kind": "sense",
		},
		{
			"name": "attack",
			"signature": "attack(direction: Direction = forward())",
			"description": "Ataca a tile adjacente na direção.",
			"kind": "action",
		},
		{
			"name": "health",
			"signature": "health() -> int",
			"description": "Retorna o HP atual do warrior.",
			"kind": "sense",
		},
		{
			"name": "rest",
			"signature": "rest()",
			"description": "O warrior descansa e recupera HP.",
			"kind": "action",
		},
		{
			"name": "rescue",
			"signature": "rescue(direction: Direction = forward())",
			"description": "Resgata um cativo na tile adjacente.",
			"kind": "action",
		},
		{
			"name": "pivot",
			"signature": "pivot(direction: Direction = backward())",
			"description": "Gira o warrior sem mover (default: vira para trás).",
			"kind": "action",
		},
		{
			"name": "look",
			"signature": "look(direction: Direction = forward()) -> Array",
			"description": "Vê até 3 tiles à frente, retorna lista de Spaces.",
			"kind": "sense",
		},
		{
			"name": "shoot",
			"signature": "shoot(direction: Direction = forward())",
			"description": "Dispara uma flecha na direção.",
			"kind": "action",
		},
	]
