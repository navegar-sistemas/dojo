extends Node
## Autoload "AudioManager" — toca SFX por TurnEvent e trilha de fundo em loop.
## Assets CC0 em assets/sfx/ e assets/music/ (trocáveis por substituição de arquivo).

const _SFX_MAP: Dictionary = {
	TurnEvent.Kind.MOVED: AssetPaths.SFX_WALK,
	TurnEvent.Kind.ATTACKED: AssetPaths.SFX_ATTACK,
	TurnEvent.Kind.DAMAGED: AssetPaths.SFX_HIT,
	TurnEvent.Kind.RESTED: AssetPaths.SFX_REST,
	TurnEvent.Kind.RESCUED: AssetPaths.SFX_RESCUE,
	TurnEvent.Kind.SHOT: AssetPaths.SFX_SHOOT,
	TurnEvent.Kind.ENEMY_DEFEATED: AssetPaths.SFX_DEFEAT_ENEMY,
	TurnEvent.Kind.WON: AssetPaths.SFX_WIN,
	TurnEvent.Kind.DIED: AssetPaths.SFX_DIE,
}

var _vol_sfx := 1.0
var _vol_music := 1.0
var _players: Array = []
var _music: AudioStreamPlayer


func _ready() -> void:
	for i: int in 4:
		var p := AudioStreamPlayer.new()
		add_child(p)
		_players.append(p)
	_music = AudioStreamPlayer.new()
	add_child(_music)
	_music.finished.connect(_on_music_finished)
	var store := ProgressStore.new()
	_vol_music = store.vol_music()
	_vol_sfx = store.vol_sfx()
	_music.volume_db = linear_to_db(_vol_music)
	for p: AudioStreamPlayer in _players:
		p.volume_db = linear_to_db(_vol_sfx)
	play_music()


func on_events(events: Array) -> void:
	# Toca o primeiro evento de cada turno com prioridade (evita pilha de sons).
	for event: TurnEvent in events:
		_play_for_kind(event.kind)
		break  # só o primeiro evento por turno; evita overlap desnecessário


func play_music() -> void:
	if _music.playing:
		return
	if not ResourceLoader.exists(AssetPaths.MUSIC_BG):
		return
	_music.stream = load(AssetPaths.MUSIC_BG) as AudioStream
	_music.play()


func set_vol_music(value: float) -> void:
	_vol_music = clampf(value, 0.0, 1.0)
	_music.volume_db = linear_to_db(_vol_music)


func set_vol_sfx(value: float) -> void:
	_vol_sfx = clampf(value, 0.0, 1.0)
	for p: AudioStreamPlayer in _players:
		p.volume_db = linear_to_db(_vol_sfx)


func _on_music_finished() -> void:
	_music.play()


func _play_for_kind(kind: TurnEvent.Kind) -> void:
	if not _SFX_MAP.has(kind):
		return
	var path: String = _SFX_MAP[kind]
	if not ResourceLoader.exists(path):
		return  # asset ausente não é erro — silêncio gracioso
	var player := _next_free_player()
	if player == null:
		return
	player.stream = load(path) as AudioStream
	player.play()


func _next_free_player() -> AudioStreamPlayer:
	for p: AudioStreamPlayer in _players:
		if not p.playing:
			return p
	return null
