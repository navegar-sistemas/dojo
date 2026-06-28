# 03 — O fluxo de um turno

Este é o mecanismo central do jogo. Tudo gira em torno do `TurnResolver.resolve(estado, ação)`.

## Passo a passo

```
ENTRADA: estado atual do nível  +  a ação escolhida pelo jogador (uma só)

 1. APLICA A AÇÃO DO WARRIOR  (ActionApplier)
      walk   → anda 1 casa (se vazia)
      attack → causa dano ao adjacente (metade se for para trás)
      rest   → cura 10% da vida
    ↳ produz: estado intermediário + eventos (ex.: MOVED, ATTACKED)

 2. CHEGOU NA ESCADA?
      sim → desfecho = VITÓRIA → FIM (inimigos nem chegam a agir)

 3. INIMIGOS REAGEM  (EnemyPhase)
      cada inimigo vivo, em ordem de posição, usa seu Behavior:
        sludge/thick → bate se o warrior está ao lado
        archer/wizard → atira se o warrior está no alcance e sem bloqueio
        cativo → não faz nada
    ↳ acumula dano no warrior + eventos (ex.: DAMAGED)

 4. A VIDA DO WARRIOR ZEROU?
      sim → desfecho = DERROTA → FIM

 5. INCREMENTA O TURNO
      desfecho = ONGOING (continua)

SAÍDA: TurnResult { novo estado, lista de eventos, desfecho }
```

## Por que essa ordem importa

- **O warrior age primeiro.** Se ele alcança a escada, vence — não toma dano "injusto"
  de inimigos no mesmo turno (passo 2 antes do passo 3).
- **Sentidos não entram aqui.** O jogador já usou os sentidos (leitura) para *decidir* a
  ação **antes** de chamar `resolve`. O turno só processa a ação (comando). É a separação
  CQS na prática.

## Exemplo concreto

Cenário: warrior na casa 1 (olhando para a direita), um sludge na casa 2.

**Turno A — jogador manda `AttackAction(forward)`:**
1. Warrior ataca → sludge cai de 12 para 7 de vida. Evento `ATTACKED`.
2. Não está na escada.
3. Sludge (vivo, adjacente) revida → warrior cai de 20 para 17. Evento `DAMAGED`.
4. Warrior vivo.
5. Turno vira 1. Desfecho `ONGOING`.

**Turnos B, C... o jogador repete o ataque** até o sludge morrer (evento `ENEMY_DEFEATED`,
o sludge some). Depois manda `WalkAction(forward)` até chegar na escada → `VICTORY`.

Isso é exatamente o que o teste `test/domain/test_turn_resolver.gd` verifica, junto com:
- determinismo (mesma entrada → mesma saída),
- ataque para trás causar metade do dano,
- `rest` não passar do máximo de vida,
- cativo não causar dano,
- derrota quando a vida zera.

## Quem o jogador "controla" (no futuro Sprint 2)

O jogador vai escrever algo assim (a lógica de **um** turno):

```gdscript
# exemplo do que o jogador escreveria
func play_turn(warrior):
    if warrior.feel(FORWARD).is_enemy():
        warrior.attack(FORWARD)
    elif warrior.health() < 20 and not_taking_damage:
        warrior.rest()
    else:
        warrior.walk(FORWARD)
```

A peça que vai **expor isso com segurança** (sem deixar o jogador trapacear lendo o estado
interno) é a `WarriorFacade`, planejada para o Sprint 2.
