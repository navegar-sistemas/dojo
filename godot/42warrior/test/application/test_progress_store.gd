extends GutTest
## Cobre o ProgressStore: persistência de nível alcançado e volume em user://.

var _store: ProgressStore


func before_each() -> void:
	_store = ProgressStore.new()
	_store.reset()


func test_nivel_padrao_sem_save_e_1() -> void:
	assert_eq(_store.current_level(), 1)


func test_has_save_false_sem_save() -> void:
	assert_false(_store.has_save())


func test_save_level_avanca_e_persiste() -> void:
	_store.save_level(3)
	var store2 := ProgressStore.new()
	assert_eq(store2.current_level(), 3)
	assert_true(store2.has_save())


func test_save_level_nao_regride() -> void:
	_store.save_level(5)
	_store.save_level(3)
	assert_eq(_store.current_level(), 5)


func test_vol_music_default_e_1() -> void:
	assert_eq(_store.vol_music(), 1.0)


func test_vol_sfx_default_e_1() -> void:
	assert_eq(_store.vol_sfx(), 1.0)


func test_save_volume_persiste() -> void:
	_store.save_volume(0.5, 0.8)
	var store2 := ProgressStore.new()
	assert_eq(store2.vol_music(), 0.5)
	assert_eq(store2.vol_sfx(), 0.8)


func test_reset_apaga_save() -> void:
	_store.save_level(4)
	_store.reset()
	assert_false(_store.has_save())
	assert_eq(_store.current_level(), 1)
