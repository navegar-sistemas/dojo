extends GutTest
## Cobre atributos iniciais, classificação e imutabilidade das unidades.


func test_warrior_atributos() -> void:
	var w := Warrior.new()
	assert_eq(w.max_health, 20)
	assert_eq(w.health, 20)
	assert_eq(w.attack_power, 5)
	assert_false(w.is_enemy())
	assert_false(w.is_captive())


func test_inimigos_sao_enemy() -> void:
	assert_true(Sludge.new().is_enemy())
	assert_true(ThickSludge.new().is_enemy())
	assert_true(Archer.new().is_enemy())
	assert_true(Wizard.new().is_enemy())


func test_hp_inicial_por_tipo() -> void:
	assert_eq(Sludge.new().max_health, 12)
	assert_eq(ThickSludge.new().max_health, 24)
	assert_eq(Archer.new().max_health, 7)
	assert_eq(Wizard.new().max_health, 3)
	assert_eq(Captive.new().max_health, 1)


func test_archer_e_wizard_sao_a_distancia() -> void:
	assert_eq(Archer.new().attack_range, 3)
	assert_eq(Wizard.new().attack_range, 3)
	assert_eq(Sludge.new().attack_range, 1)


func test_captive_e_inerte() -> void:
	var c := Captive.new()
	assert_true(c.is_captive())
	assert_false(c.is_enemy())
	assert_eq(c.attack_power, 0)


func test_dano_produz_nova_unidade_sem_mutar() -> void:
	var s := Sludge.new()
	var ferido := s.damaged_by(5)
	assert_eq(s.health, 12, "original não muta")
	assert_eq(ferido.health, 7)
	assert_true(ferido is Sludge, "preserva o tipo")


func test_dano_faz_clamp_em_zero() -> void:
	var w := Wizard.new()
	assert_eq(w.damaged_by(99).health, 0)
	assert_false(w.damaged_by(99).is_alive())
