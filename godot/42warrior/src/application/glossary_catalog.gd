class_name GlossaryCatalog
extends RefCounted
## Resolve, do estado inicial do nível (entidades) e da definição (pontuação),
## o conteúdo data-driven do glossário. Sem hardcode por nível; sem API de cena.


static func entries_for_level(level_index: int) -> Dictionary:
	var definition := BeginnerTower.definition(level_index)
	var state := LevelLoader.new().load_definition(definition)
	return {
		"entities": _entity_entries(state),
		"score_terms": _score_entries(definition, state),
	}


static func _entity_entries(state: LevelState) -> Array:
	var seen := {}
	var result: Array = []
	for pos: int in state.unit_positions():
		var unit: Unit = state.unit_at(pos)
		var key := _entity_key(unit)
		if key == "" or seen.has(key):
			continue
		seen[key] = true
		result.append({"name": _entity_name(unit), "description": _entity_description(unit)})
	return result


static func _score_entries(definition: LevelDefinition, state: LevelState) -> Array:
	var tempo := {
		"name": "Bônus de tempo",
		"definition": "Pts ganhos pelos turnos restantes ao concluir o nível.",
		"value": "máx %d pts" % definition.time_bonus,
	}
	var resgate := {
		"name": "Bônus de resgate",
		"definition": "Pts por cativo resgatado com rescue().",
		"value": "20 pts/cativo",
	}
	var ace := {
		"name": "Meta ACE",
		"definition": "Pontuação mínima para avaliação ACE.",
		"value": "%d pts" % definition.ace_score,
	}
	var terms: Array = [tempo]
	if _has_captives(state):
		terms.append(resgate)
	terms.append(ace)
	return terms


static func _has_captives(state: LevelState) -> bool:
	for pos: int in state.unit_positions():
		if state.unit_at(pos) is Captive:
			return true
	return false


static func _entity_key(unit: Unit) -> String:
	if unit is Sludge and not (unit is ThickSludge):
		return "sludge"
	if unit is ThickSludge:
		return "thick_sludge"
	if unit is Archer:
		return "archer"
	if unit is Wizard:
		return "wizard"
	if unit is Captive:
		return "captive"
	return ""


static func _entity_name(unit: Unit) -> String:
	if unit is Sludge and not (unit is ThickSludge):
		return "Sludge"
	if unit is ThickSludge:
		return "Sludge Espesso"
	if unit is Archer:
		return "Arqueiro"
	if unit is Wizard:
		return "Mago"
	if unit is Captive:
		return "Cativo"
	return "Entidade"


static func _entity_description(unit: Unit) -> String:
	if unit is Sludge and not (unit is ThickSludge):
		return "Corpo-a-corpo. HP %d, dano %d/turno." % [unit.max_health, unit.attack_power]
	if unit is ThickSludge:
		return (
			"Corpo-a-corpo reforçado. HP %d, dano %d/turno." % [unit.max_health, unit.attack_power]
		)
	if unit is Archer:
		return (
			"Atirador a distância (alcance %d). HP %d, dano %d/tiro."
			% [unit.attack_range, unit.max_health, unit.attack_power]
		)
	if unit is Wizard:
		return (
			"Feiticeiro letal a distância. HP %d, dano %d/feitiço."
			% [unit.max_health, unit.attack_power]
		)
	if unit is Captive:
		return "Prisioneiro inerte. Resgate com rescue() para ganhar 20 pts."
	return ""
