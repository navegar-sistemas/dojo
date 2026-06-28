class_name ErrorView
extends PanelContainer

@onready var _label: Label = $Label


func show_error(msg: String) -> void:
	_label.text = msg
	visible = true


func clear() -> void:
	_label.text = ""
	visible = false
