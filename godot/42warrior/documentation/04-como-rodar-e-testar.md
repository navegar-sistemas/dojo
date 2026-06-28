# 04 — Como rodar e testar

> Lembrete: **ainda não há jogo visual** para "jogar". O que dá para rodar agora são os
> **testes automatizados** que provam que as regras funcionam.

## Pré-requisitos (já instalados nesta máquina)

- **Godot 4.7** — encontrado em `~/Downloads/Godot.app`.
- **gdtoolkit** (gdformat/gdlint) — instalado via `pip3 install --user gdtoolkit`,
  fica em `~/Library/Python/3.9/bin`.
- **GUT 9.4.0** — framework de testes, vendorizado em `addons/gut/`.

Se o Godot estiver em outro lugar, exporte o caminho antes de rodar:
```bash
export GODOT_BIN=/caminho/para/o/binario/Godot
```

## Os scripts (em `scripts/`)

| Comando | O que faz |
|---|---|
| `bash scripts/test.sh` | Roda os **51 testes** de domínio (headless, via GUT). |
| `bash scripts/lint.sh` | Verifica **formatação** (gdformat) e **estilo** (gdlint). |
| `bash scripts/arch_guard.sh` | Garante que o **domínio não usa a engine** (Clean Architecture). |
| `bash scripts/check.sh` | Roda **tudo acima** de uma vez (a verificação completa). |

Exemplo:
```bash
cd ~/Documents/dojo/godot/42warrior/.worktrees/001-beginner-tower-completa
bash scripts/check.sh
```

Saída esperada (resumida):
```
Guard de arquitetura: OK (Domain/Application puros).
Lint OK.
...
Tests    51
  Passing 51
---- All tests passed! ----
== check.sh: tudo verde ==
```

## Rodar os testes dentro da IDE Godot (opcional)

1. Abra o projeto (`project.godot`) no Godot.
2. A primeira abertura importa os recursos automaticamente.
3. O GUT tem um painel próprio na IDE; também dá para usar a versão de linha de comando
   acima — é a mais simples e a que usamos no desenvolvimento.

## Como os testes estão organizados (`test/domain/`)

Um arquivo por área, espelhando as regras:

| Arquivo | Cobre |
|---|---|
| `test_direction.gd` | sinal relativo e oposto da direção |
| `test_units.gd` | atributos de cada unidade e imutabilidade do dano |
| `test_space_and_level_state.gd` | consultas e imutabilidade do estado |
| `test_senses.gd` | feel / look / listen / direction_of_stairs |
| `test_actions.gd` | os objetos de comando |
| `test_behaviors.gd` | IA de melee / ranged / inert (com bloqueio de linha) |
| `test_turn_resolver.gd` | o turno completo: efeitos, vitória, derrota, determinismo |
| `test_smoke.gd` | teste mínimo que confirma que o runner funciona |

## Nota técnica (um detalhe que pode confundir)

Há um pequeno **patch local comentado** em `addons/gut/gut_loader.gd`: o GUT 9.4.0 tinha
um bug ao rodar headless no Godot 4.7 (lia uma configuração inexistente e quebrava). O
patch troca a leitura por uma versão com valor padrão. Está documentado no próprio arquivo.
