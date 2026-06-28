# 02 — Referência do domínio (com paralelo em TypeScript)

Cada classe do domínio explicada. Os trechos em **TypeScript** são *analogias* para
facilitar a leitura — o código real está em GDScript, em `src/domain/`.

> Em GDScript, `extends RefCounted` ≈ uma `class` normal de TypeScript;
> `class_name X` é o que registra o nome global da classe.

---

## Direction — `world/direction.gd`

Direção **relativa** ao warrior: para frente ou para trás. (A beginner tower só usa essas
duas; o jogo completo teria esquerda/direita.)

```typescript
class Direction {
  private constructor(private kind: "FORWARD" | "BACKWARD") {}
  static forward()  { return new Direction("FORWARD"); }
  static backward() { return new Direction("BACKWARD"); }
  relativeSign(): number { return this.kind === "FORWARD" ? 1 : -1; }
  opposite(): Direction { /* troca FORWARD↔BACKWARD (usado pelo pivot) */ }
  equals(other: Direction): boolean { return other?.kind === this.kind; }
}
```

Por que "relativa"? O warrior **olha** para um lado (o *facing*). "Frente" é para onde ele
olha. O passo absoluto na grade = `facing × relativeSign()` — calculado pelo `LevelState`,
que é quem conhece o facing.

---

## Unit e os 6 tipos — `units/`

A base de toda unidade (herói, inimigos, refém) e seus atributos.

```typescript
abstract class Unit {
  maxHealth: number;
  health: number;
  attackPower: number;
  attackRange: number;     // 1 = corpo-a-corpo; >1 = à distância

  isAlive(): boolean { return this.health > 0; }
  isEnemy(): boolean { return false; }
  isCaptive(): boolean { return false; }

  // imutável: devolve uma NOVA unidade com menos vida
  damagedBy(amount: number): Unit { /* clamp em [0, max] */ }

  // qual comportamento de turno esta unidade tem (polimorfismo)
  createBehavior(): UnitBehavior { return new InertBehavior(); }
}
```

Os tipos concretos só configuram seus números e (quando inimigos) seu comportamento:

| Classe | HP | Ataque | Alcance | Papel |
|---|---:|---:|---:|---|
| `Warrior` | 20 | 5 | 1 | o herói do jogador |
| `Sludge` | 12 | 3 | 1 | inimigo básico corpo-a-corpo |
| `ThickSludge` | 24 | 3 | 1 | inimigo resistente |
| `Archer` | 7 | 3 | 3 | atira de longe |
| `Wizard` | 3 | 11 | 3 | frágil, mas letal — matar rápido |
| `Captive` | 1 | 0 | 0 | refém: resgatar, **nunca** atacar |

> Esses números são **ajustáveis** e ficam centralizados em cada arquivo `units/*.gd`.

**Imutabilidade na prática:** atacar um sludge não "edita" o sludge — cria um novo sludge
com menos vida e um novo estado do nível apontando para ele. O original fica intacto.

---

## Space — `world/space.gd`

A visão **somente-leitura** de uma casa da grade, devolvida pelos sentidos. Encapsula o
que o jogador pode saber, sem dar acesso à unidade mutável.

```typescript
class Space {
  isWall(): boolean;       // fora da grade
  isStairs(): boolean;     // é a escada (saída)?
  isEmpty(): boolean;      // sem parede e sem unidade
  isEnemy(): boolean;      // tem inimigo?
  isCaptive(): boolean;    // tem refém?
  unitType(): string;      // "Sludge", "Archer", ... ou ""
}
```

---

## LevelState — `world/level_state.gd`

A "fotografia" **imutável** do nível: largura, posição da escada, o warrior (e para onde
olha), as demais unidades por posição, e o número do turno.

```typescript
class LevelState {
  // CONSULTAS (puras, não mudam nada)
  spaceAt(position: number): Space;
  unitAt(position: number): Unit | null;
  warriorPosition(): number;
  stepOf(direction: Direction): number;            // passo absoluto na grade
  positionToward(direction: Direction, dist: number): number;

  // "MUDANÇAS" devolvem um NOVO estado (imutável)
  withWarriorPosition(p: number): LevelState;
  withWarrior(w: Warrior): LevelState;
  withUnitAt(pos: number, unit: Unit | null): LevelState; // null remove
  withTurn(t: number): LevelState;
}
```

A grade é 1×N (um corredor). Posições fora de `[0, largura-1]` são **parede**.

---

## Senses — `senses/senses.gd`

Tudo que o jogador pode "perceber" sobre um snapshot do nível — **sem gastar o turno**.

```typescript
class Senses {
  feel(dir: Direction): Space;        // a casa ao lado naquela direção
  look(dir: Direction): Space[];      // as 3 casas à frente (perto → longe)
  listen(): Space[];                  // todas as casas com unidades
  health(): number;                   // a vida do warrior
  directionOfStairs(): Direction;     // pra onde fica a escada
  directionOfPosition(pos: number): Direction;
}
```

São o "input" do raciocínio do jogador: ele sente, decide, e então escolhe **uma** ação.

---

## Actions — `turn/actions/`

Os comandos que o warrior pode executar (e que gastam o turno). Cada um é uma classe
simples (um "objeto de comando"):

```typescript
class WalkAction   { constructor(public direction: Direction) {} }
class AttackAction { constructor(public direction: Direction) {} }
class RestAction   { /* sem direção */ }
```

Modelar como tipos (em vez de uma string `"walk"`) permite o "despacho por tipo" no
`ActionApplier`, sem `if`-cadeia de strings mágicas.

---

## Behaviors — `combat/`

A "IA" de cada unidade, escolhida por polimorfismo. Cada comportamento responde a uma só
pergunta: *quanto de dano esta unidade causa ao warrior neste turno?*

```typescript
abstract class UnitBehavior {
  damageToWarrior(state, selfPosition, unit): number { return 0; }
}
class MeleeBehavior  { /* ataca se o warrior está a 1 casa (sludge, thick) */ }
class RangedBehavior { /* ataca dentro do alcance, se a linha não estiver bloqueada
                          por outra unidade (archer, wizard) */ }
class InertBehavior  { /* não faz nada (cativo) — herda o 0 da base */ }
```

`Sludge.createBehavior()` devolve `MeleeBehavior`, `Archer` devolve `RangedBehavior`, e
assim por diante. Adicionar um novo inimigo = uma nova classe, sem mexer no resto.

---

## ActionApplier — `turn/action_applier.gd`

Aplica a ação **do warrior** ao estado, devolvendo o novo estado + os eventos. Despacha
por tipo e cada ação tem seu método privado (responsabilidade única).

```typescript
class ActionApplier {
  apply(state, action): { state: LevelState, events: TurnEvent[] } {
    if (action instanceof WalkAction)   return this.walk(state, action.direction);
    if (action instanceof AttackAction) return this.attack(state, action.direction);
    if (action instanceof RestAction)   return this.rest(state);
    return { state, events: [] };       // desconhecida = não faz nada
  }
}
```

Regras embutidas aqui:
- **walk**: anda 1 casa se estiver vazia; senão fica parado (bateu na parede/inimigo).
- **attack**: dano = ataque do warrior; **atacar para trás causa metade** (5 → 2). Se o
  inimigo morre, ele some da grade.
- **rest**: cura **10% da vida máxima** (2 pontos), sem ultrapassar o máximo.

---

## EnemyPhase — `combat/enemy_phase.gd`

Depois da ação do warrior, cada inimigo vivo reage (em ordem de posição, para ser
determinístico), usando seu próprio `Behavior`. Acumula o dano no warrior e gera eventos.

---

## TurnResolver — `turn/turn_resolver.gd`  ⭐ o coração

Orquestra o turno inteiro:

```typescript
class TurnResolver {
  resolve(state: LevelState, action: Action): TurnResult {
    // 1. aplica a ação do warrior
    // 2. chegou na escada?      → VITÓRIA
    // 3. inimigos reagem
    // 4. vida do warrior == 0?  → DERROTA
    // 5. incrementa o turno e devolve tudo
  }
}
```

Veja o passo a passo detalhado em [`03-fluxo-de-turno.md`](03-fluxo-de-turno.md).

---

## TurnResult e TurnEvent — `turn/turn_result.gd`, `turn/turn_event.gd`

O **resultado** de um turno e os **eventos** observáveis dentro dele.

```typescript
type Outcome = "ONGOING" | "VICTORY" | "DEFEAT";

class TurnResult {
  state: LevelState;     // o novo estado
  events: TurnEvent[];   // o que aconteceu (pra animar/pontuar)
  outcome: Outcome;      // continua / venceu / morreu
}

// kinds: MOVED, ATTACKED, DAMAGED, RESTED, RESCUED, SHOT,
//        ENEMY_DEFEATED, WON, DIED
class TurnEvent {
  kind; actor; amount; position;
}
```

Os eventos são a "ponte" entre a lógica e a futura camada visual: o Sprint 3 vai ler
`MOVED` para animar o passo, `DAMAGED` para piscar vermelho, etc.
