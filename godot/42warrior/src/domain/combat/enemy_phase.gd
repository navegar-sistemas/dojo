class_name EnemyPhase
extends RefCounted
## Fase de reação dos inimigos. Espelha o turno de 2 etapas do Ruby Warrior
## (prepare_turn → perform_turn): cada inimigo DECIDE seu dano sobre o snapshot do
## INÍCIO do turno (`perception`, antes da ação do warrior e das mortes deste turno) e
## o dano é APLICADO sobre o estado corrente (`current`). Assim a percepção à distância
## (linha de tiro) não enxerga a linha que o warrior abriu neste turno; e uma unidade
## morta no mesmo turno (ausente em `current`) não age.


## Retorna { "state": LevelState, "events": Array }.
func react(perception: LevelState, current: LevelState) -> Dictionary:
	var working := current
	var events: Array = []
	for position in perception.unit_positions():
		var deciding := perception.unit_at(position)
		if deciding == null or not deciding.is_alive():
			continue
		var live := working.unit_at(position)
		if live == null or not live.is_alive():
			continue
		var damage := deciding.create_behavior().damage_to_warrior(perception, position, deciding)
		if damage <= 0:
			continue
		working = working.with_warrior(working.warrior().damaged_by(damage))
		var actor: String = deciding.get_script().get_global_name()
		events.append(
			TurnEvent.new(TurnEvent.Kind.DAMAGED, actor, damage, working.warrior_position())
		)
		if not working.warrior().is_alive():
			break
	return {"state": working, "events": events}
