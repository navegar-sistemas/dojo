class_name LevelSkeletonProvider
extends RefCounted

const _API_DOCS: Dictionary = {
	"walk": "warrior.walk()              # avança na direção forward",
	"feel": "warrior.feel()  # Space adjacente (is_empty/is_enemy/is_captive/is_wall/is_stairs)",
	"attack": "warrior.attack()           # ataca o adjacente na direção forward",
	"health": "warrior.health()           # int: HP atual do warrior",
	"rest": "warrior.rest()             # descansa: recupera 10% do HP máximo",
	"rescue": "warrior.rescue()           # resgata o cativo adjacente",
	"pivot": "warrior.pivot()            # inverte o facing (forward↔backward)",
	"look": "warrior.look()             # Array[Space]: até 3 espaços à frente",
	"shoot": "warrior.shoot()            # atira na primeira unidade na linha",
}

const _SENSE_DOCS: Array = [
	"warrior.direction_of_stairs()  # Direction para a escada",
	"warrior.listen()               # Array[Space] com todas as unidades visíveis",
	"warrior.direction_of(space)    # Direction relativa a um Space",
]


func skeleton(level_index: int) -> String:
	var available := _cumulative_abilities(level_index)
	var lines: PackedStringArray = []
	lines.append("extends RefCounted")
	lines.append("")
	lines.append("# Habilidades disponíveis neste nível:")
	for key: String in available:
		if _API_DOCS.has(key):
			lines.append("#   " + _API_DOCS[key])
	lines.append("#")
	lines.append("# Sentidos sempre disponíveis:")
	for doc: String in _SENSE_DOCS:
		lines.append("#   " + doc)
	lines.append("")
	lines.append("func play_turn(warrior):")
	lines.append("\tpass  # escreva sua lógica aqui")
	return "\n".join(lines)


func _cumulative_abilities(level_index: int) -> PackedStringArray:
	var cumulative: PackedStringArray = []
	for i: int in range(1, level_index + 1):
		var def := BeginnerTower.definition(i)
		for ability: String in def.abilities:
			if not ability in cumulative:
				cumulative.append(ability)
	return cumulative
