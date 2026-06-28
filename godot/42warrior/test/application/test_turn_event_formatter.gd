extends GutTest
## Cobre o TurnEventFormatter: converte TurnEvents em texto legível por turno.

var _fmt: TurnEventFormatter


func before_each() -> void:
	_fmt = TurnEventFormatter.new()


func _evt(
	kind: TurnEvent.Kind, actor: String = "warrior", amount: int = 0, pos: int = -1
) -> TurnEvent:
	return TurnEvent.new(kind, actor, amount, pos)


func test_sem_eventos_retorna_sem_acao() -> void:
	assert_eq(_fmt.format_turn([], ""), "sem ação")


func test_sem_eventos_com_erro_retorna_mensagem_de_erro() -> void:
	var result := _fmt.format_turn([], "Script:1: erro de sintaxe")
	assert_true(result.begins_with("erro:"), "deve começar com 'erro:'")
	assert_true(result.contains("Script:1"), "deve incluir primeira linha do erro")


func test_moved_retorna_andou() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.MOVED)], "")
	assert_eq(result, "andou")


func test_attacked_inclui_dano() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.ATTACKED, "warrior", 5)], "")
	assert_true(result.contains("atacou"), "deve conter 'atacou'")
	assert_true(result.contains("5"), "deve conter o dano")


func test_damaged_inclui_dano_e_ator() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.DAMAGED, "Sludge", 3)], "")
	assert_true(result.contains("3"), "deve conter o dano")
	assert_true(result.contains("Sludge"), "deve conter o nome do ator")


func test_rested_inclui_cura() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.RESTED, "warrior", 2)], "")
	assert_true(result.contains("descansou"), "deve conter 'descansou'")
	assert_true(result.contains("2"), "deve conter o valor de cura")


func test_rescued_retorna_resgatou() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.RESCUED)], "")
	assert_eq(result, "resgatou cativo")


func test_shot_inclui_dano() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.SHOT, "warrior", 4)], "")
	assert_true(result.contains("disparou"), "deve conter 'disparou'")
	assert_true(result.contains("4"), "deve conter o dano")


func test_enemy_defeated_inclui_nome_do_inimigo() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.ENEMY_DEFEATED, "Sludge")], "")
	assert_true(result.contains("Sludge"), "deve conter o nome do inimigo")
	assert_true(result.contains("derrotado"), "deve conter 'derrotado'")


func test_won_retorna_vitoria() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.WON)], "")
	assert_eq(result, "vitória!")


func test_died_retorna_derrota() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.DIED)], "")
	assert_eq(result, "derrota")


func test_multiplos_eventos_separados_por_bullet() -> void:
	var events := [
		_evt(TurnEvent.Kind.ATTACKED, "warrior", 5),
		_evt(TurnEvent.Kind.ENEMY_DEFEATED, "Sludge"),
	]
	var result := _fmt.format_turn(events, "")
	assert_true(result.contains(" • "), "eventos separados por bullet")


func test_erro_em_turno_com_eventos_aparece_no_final() -> void:
	var result := _fmt.format_turn([_evt(TurnEvent.Kind.MOVED)], "linha de erro")
	assert_true(result.begins_with("andou"), "evento vem antes do erro")
	assert_true(result.contains("[erro:"), "erro aparece ao final")


func test_erro_multilinhas_usa_so_primeira_linha() -> void:
	var result := _fmt.format_turn([], "linha1\nlinha2\nlinha3")
	assert_false(result.contains("linha2"), "não deve conter segunda linha")
	assert_true(result.contains("linha1"), "deve conter primeira linha")
