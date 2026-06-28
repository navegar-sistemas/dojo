class_name WarriorFacade
extends RefCounted
## A ÚNICA superfície exposta ao código do jogador. Oferece os sentidos (consultas
## sobre um snapshot, delegadas a Senses) e as ações (que apenas REGISTRAM a 1ª
## escolha do turno). Não expõe o LevelState nem as unidades — isola o estado interno.

var _senses: Senses
var _chosen_action: Action


func _init(state: LevelState) -> void:
	_senses = Senses.new(state)
	_chosen_action = null


func feel(direction: Direction = Direction.forward()) -> Space:
	return _senses.feel(direction)


func look(direction: Direction = Direction.forward()) -> Array:
	return _senses.look(direction)


func listen() -> Array:
	return _senses.listen()


func health() -> int:
	return _senses.health()


func direction_of_stairs() -> Direction:
	return _senses.direction_of_stairs()


func direction_of(space: Space) -> Direction:
	return _senses.direction_of_position(space.position())


func feel_2d(direction: Direction) -> Space:
	return _senses.feel_2d(direction)


func look_2d(direction: Direction) -> Array:
	return _senses.look_2d(direction)


func direction_of_stairs_2d() -> Direction:
	return _senses.direction_of_stairs_2d()


func direction_of_2d(space: Space) -> Direction:
	return _senses.direction_of_2d(space.position_2d())


func walk(direction: Direction = Direction.forward()) -> void:
	_record(WalkAction.new(direction))


func attack(direction: Direction = Direction.forward()) -> void:
	_record(AttackAction.new(direction))


func rest() -> void:
	_record(RestAction.new())


func rescue(direction: Direction = Direction.forward()) -> void:
	_record(RescueAction.new(direction))


func pivot(direction: Direction = Direction.backward()) -> void:
	_record(PivotAction.new(direction))


func shoot(direction: Direction = Direction.forward()) -> void:
	_record(ShootAction.new(direction))


## null = o jogador não agiu neste turno (no-op).
func chosen_action() -> Action:
	return _chosen_action


func _record(action: Action) -> void:
	if _chosen_action == null:
		_chosen_action = action
