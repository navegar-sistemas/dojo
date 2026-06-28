class_name UnitBehavior
extends RefCounted
## Estratégia de turno de uma unidade. Devolve o dano que ela causa ao warrior
## neste turno (0 = não ataca). Base inerte; subclasses especializam.


func damage_to_warrior(_state: LevelState, _self_position: int, _unit: Unit) -> int:
	return 0
