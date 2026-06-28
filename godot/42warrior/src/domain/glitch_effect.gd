class_name GlitchEffect
extends RefCounted
## Value object: efeito de glitch produzido pelo GlitchRule para um turno (ADR-034).
## Campos são read-only por convenção; GlitchRule cria e popula.

## Intensidade do pós-processo de glitch (0.0 = sem glitch, 1.0 = máximo).
var post_process_intensity: float = 0.0
## O warrior exibe shader de corrupção neste turno?
var warrior_corrupted: bool = false
## Flash de corrupção de tela inteira?
var screen_glitch: bool = false
## Janela de glitch seedada está ativa neste turno (GlitchRuleModel)?
var window_active: bool = false
