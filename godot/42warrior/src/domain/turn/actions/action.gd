class_name Action
extends RefCounted
## Comando de turno do warrior. Subclasses concretas (WalkAction, AttackAction,
## RestAction, ...) carregam seus parâmetros; o TurnResolver despacha por tipo.
