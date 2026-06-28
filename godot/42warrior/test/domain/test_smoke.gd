extends GutTest
## Teste de fumaça: prova que o runner GUT está configurado e executa asserções.


func test_runner_executa_assercao() -> void:
	assert_eq(2 + 2, 4, "aritmética básica deve funcionar")
