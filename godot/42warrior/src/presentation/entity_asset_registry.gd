class_name EntityAssetRegistry
extends RefCounted
## Registro central de assets visuais: tipo-entidade → sprite, tiles do corredor.
## Trocar arte = editar só este arquivo, sem tocar scripts de cena (RNF-060).


static func sprite_for_type(entity_type: String) -> String:
	match entity_type:
		"Warrior":
			return AssetPaths.WARRIOR_SPRITE
		"Sludge":
			return AssetPaths.SLUDGE_SPRITE
		"ThickSludge":
			return AssetPaths.THICK_SLUDGE_SPRITE
		"Archer":
			return AssetPaths.ARCHER_SPRITE
		"Wizard":
			return AssetPaths.WIZARD_SPRITE
		"Captive":
			return AssetPaths.CAPTIVE_SPRITE
		"stairs":
			return AssetPaths.STAIRS_SPRITE
	return AssetPaths.SLUDGE_SPRITE


static func floor_tile() -> String:
	return AssetPaths.FLOOR_TILE


static func wall_tile() -> String:
	return AssetPaths.WALL_TILE


static func stairs_tile() -> String:
	return AssetPaths.STAIRS_SPRITE
