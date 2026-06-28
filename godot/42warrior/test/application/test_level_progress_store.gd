extends GutTest
## Cobre LevelProgressStore: status, max score, ace, desbloqueio.

var _store: LevelProgressStore


func before_each() -> void:
	_store = LevelProgressStore.new()
	_store.reset()


func after_all() -> void:
	LevelProgressStore.new().reset()


func test_status_inicial_e_locked() -> void:
	assert_eq(_store.level_status(1), LevelProgressStore.STATUS_LOCKED)


func test_unlock_level_muda_para_unlocked() -> void:
	_store.unlock_level(1)
	assert_eq(_store.level_status(1), LevelProgressStore.STATUS_UNLOCKED)


func test_save_result_won_muda_para_won() -> void:
	_store.save_result(1, 50, true, false)
	assert_eq(_store.level_status(1), LevelProgressStore.STATUS_WON)


func test_save_result_lost_nao_muda_status() -> void:
	_store.save_result(1, 0, false, false)
	assert_eq(_store.level_status(1), LevelProgressStore.STATUS_LOCKED)


func test_score_maximo_preservado_ao_perder_run_pior() -> void:
	_store.save_result(1, 80, true, false)
	_store.save_result(1, 40, true, false)
	assert_eq(_store.best_score_for(1), 80, "score pior nao sobrescreve o maximo")


func test_score_maximo_atualizado_ao_ganhar_run_melhor() -> void:
	_store.save_result(1, 50, true, false)
	_store.save_result(1, 90, true, false)
	assert_eq(_store.best_score_for(1), 90, "score melhor atualiza o maximo")


func test_ace_preservado_se_nova_run_nao_e_ace() -> void:
	_store.save_result(1, 100, true, true)
	_store.save_result(1, 60, true, false)
	assert_true(_store.is_ace_for(1), "ace nao e perdido por run pior")


func test_unlock_nivel_invalido_nao_causa_erro() -> void:
	_store.unlock_level(0)
	_store.unlock_level(10)
	assert_true(true, "sem crash em indices invalidos")


func test_all_levels_summary_retorna_9_itens() -> void:
	var summary: Array = _store.all_levels_summary()
	assert_eq(summary.size(), 9)


func test_all_levels_summary_tem_campos_obrigatorios() -> void:
	var item: Dictionary = _store.all_levels_summary()[0]
	assert_has(item, "index")
	assert_has(item, "status")
	assert_has(item, "score_best")
	assert_has(item, "is_ace")
	assert_has(item, "description")


func test_sandbox_nivel_0_sempre_desbloqueado() -> void:
	assert_eq(
		_store.level_status(0),
		LevelProgressStore.STATUS_UNLOCKED,
		"sandbox (nivel 0) deve ser sempre unlocked"
	)
