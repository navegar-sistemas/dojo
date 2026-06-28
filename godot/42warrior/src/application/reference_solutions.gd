class_name ReferenceSolutions
extends RefCounted
## Código play_turn embarcado que resolve cada nível da beginner tower (RF-013).
## Cada nível recebe uma solução MÍNIMA que usa apenas a API (habilidades do warrior)
## introduzida até aquele nível — DoD de US-011, verificado por
## test_reference_api_conformance.gd contra a allowlist cumulativa de
## BeginnerTower.definition(n).abilities. As soluções operam por DIREÇÃO fixa do nível
## (forward/backward, valores sempre disponíveis), nunca usam direction_of_stairs, e
## nunca atacam cativos (só resgatam). Vitória ponta-a-ponta em test_reference_solutions.


static func for_level(index: int) -> String:
	var src := ""
	match index:
		1:
			src = _walk_only()
		2:
			src = _feel_attack()
		3:
			src = _melee_heal("Direction.forward()")
		4:
			src = _archer_tank()
		5, 6:
			src = _melee_rescue("Direction.forward()")
		7:
			src = _melee_rescue("Direction.backward()")
		9:
			src = _advance_rescue("Direction.backward()")
		8:
			src = _shoot_clearing_the_line()
		_:
			src = _walk_only()
	return src


## L1 — corredor vazio: só caminhar (única habilidade do nível).
static func _walk_only() -> String:
	return "extends RefCounted\n\nfunc play_turn(warrior):\n\twarrior.walk()\n"


## L2 — sente o inimigo e ataca, senão avança (feel/attack/walk).
static func _feel_attack() -> String:
	return (
		"extends RefCounted\n\n"
		+ "func play_turn(warrior):\n"
		+ "\tif warrior.feel().is_enemy():\n"
		+ "\t\twarrior.attack()\n"
		+ "\telse:\n"
		+ "\t\twarrior.walk()\n"
	)


## L3/L4 — luta corpo-a-corpo com cura: recua e descansa quando ferido e seguro; ataca o
## que está à frente; avança. Sem rescue (não introduzido até L4). `fwd` é a direção do nível.
static func _melee_heal(fwd: String) -> String:
	return (
		"extends RefCounted\nvar _last := 20\n\n"
		+ "func play_turn(warrior):\n"
		+ "\tvar hp = warrior.health()\n"
		+ "\tvar taking = hp < _last\n"
		+ "\t_last = hp\n"
		+ "\tvar fwd = "
		+ fwd
		+ "\n"
		+ "\tif hp <= 8 and taking:\n"
		+ "\t\twarrior.walk(fwd.opposite())\n"
		+ "\telif warrior.feel(fwd).is_enemy():\n"
		+ "\t\twarrior.attack(fwd)\n"
		+ "\telif hp < 20 and not taking:\n"
		+ "\t\twarrior.rest()\n"
		+ "\telse:\n"
		+ "\t\twarrior.walk(fwd)\n"
	)


## L5/L6/L7/L9 — como _melee_heal, mas resgata cativos à frente (rescue, L5+). `fwd` é a
## direção do nível; o recuo de cura é fwd.opposite() (afasta-se dos inimigos).
static func _melee_rescue(fwd: String) -> String:
	return (
		"extends RefCounted\nvar _last := 20\n\n"
		+ "func play_turn(warrior):\n"
		+ "\tvar hp = warrior.health()\n"
		+ "\tvar taking = hp < _last\n"
		+ "\t_last = hp\n"
		+ "\tvar fwd = "
		+ fwd
		+ "\n"
		+ "\tvar front = warrior.feel(fwd)\n"
		+ "\tif hp <= 8 and taking:\n"
		+ "\t\twarrior.walk(fwd.opposite())\n"
		+ "\telif front.is_captive():\n"
		+ "\t\twarrior.rescue(fwd)\n"
		+ "\telif front.is_enemy():\n"
		+ "\t\twarrior.attack(fwd)\n"
		+ "\telif hp < 20 and not taking:\n"
		+ "\t\twarrior.rest()\n"
		+ "\telse:\n"
		+ "\t\twarrior.walk(fwd)\n"
	)


## L4 — thick sludge + archer + thick sludge num corredor que o alcance do archer cobre
## inteiro: não há casa fora de alcance. Cura recuando só quando há inimigo À FRENTE (ele
## bloqueia a linha do archer, tornando o recuo seguro); ao tomar flecha com a frente vazia
## (linha aberta, sem fuga), AVANÇA para matar o atirador. Só walk/feel/attack/health/rest.
static func _archer_tank() -> String:
	return (
		"extends RefCounted\nvar _last := 20\nvar _broke := false\n\n"
		+ "func play_turn(warrior):\n"
		+ "\tvar hp = warrior.health()\n"
		+ "\tvar taking = hp < _last\n"
		+ "\t_last = hp\n"
		+ "\tvar front = warrior.feel()\n"
		+ "\tif taking and front.is_empty():\n"
		+ "\t\t_broke = true\n"  # dano à distância com a frente vazia: rompi o bloqueio
		+ "\tif front.is_enemy():\n"
		+ "\t\tif hp <= 12 and taking and not _broke:\n"
		+ "\t\t\twarrior.walk(Direction.backward())\n"
		+ "\t\telse:\n"
		+ "\t\t\twarrior.attack()\n"
		+ "\telif taking:\n"
		+ "\t\twarrior.walk()\n"
		+ "\telif hp < 20:\n"
		+ "\t\twarrior.rest()\n"
		+ "\telse:\n"
		+ "\t\twarrior.walk()\n"
	)


## L7/L9 — avança numa direção fixa (backward) resgatando cativos, sem recuar: nesses
## níveis o lado oposto ao avanço tem inimigos, então recuar seria andar para o perigo.
static func _advance_rescue(fwd: String) -> String:
	return (
		"extends RefCounted\nvar _last := 20\n\n"
		+ "func play_turn(warrior):\n"
		+ "\tvar hp = warrior.health()\n"
		+ "\tvar taking = hp < _last\n"
		+ "\t_last = hp\n"
		+ "\tvar fwd = "
		+ fwd
		+ "\n"
		+ "\tvar front = warrior.feel(fwd)\n"
		+ "\tif front.is_captive():\n"
		+ "\t\twarrior.rescue(fwd)\n"
		+ "\telif front.is_enemy():\n"
		+ "\t\twarrior.attack(fwd)\n"
		+ "\telif hp < 20 and not taking:\n"
		+ "\t\twarrior.rest()\n"
		+ "\telse:\n"
		+ "\t\twarrior.walk(fwd)\n"
	)


## L8 — cativo + 2 wizards em fila: resgata o cativo adjacente e atira no inimigo mais
## próximo na linha (look/shoot, L8). Mata o da frente; o de trás, bloqueado no início do
## turno, não revida no mesmo turno (fase de inimigos de 2 etapas) — um wizard por vez.
static func _shoot_clearing_the_line() -> String:
	return """extends RefCounted

func play_turn(warrior):
	var front = warrior.feel()
	if front.is_captive():
		warrior.rescue()
	elif front.is_enemy():
		warrior.attack()
	else:
		var target = null
		for space in warrior.look():
			if space.is_enemy() or space.is_captive():
				target = space
				break
		if target != null and target.is_enemy():
			warrior.shoot()
		else:
			warrior.walk()
"""
