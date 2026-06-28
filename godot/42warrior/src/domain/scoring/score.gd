class_name Score
extends RefCounted

var total: int
var ace_score: int


func _init(p_total: int, p_ace_score: int) -> void:
	total = p_total
	ace_score = p_ace_score


func is_ace() -> bool:
	return total >= ace_score
