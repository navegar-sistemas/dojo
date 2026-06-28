class_name CodeEditorPanel
extends PanelContainer

signal run_pressed(source: String)
signal debug_toggled(open: bool)

var _level_index := 1
var _store := PlayerCodeStore.new()
var _skeleton_provider := LevelSkeletonProvider.new()
var _ref_source := ""
var _player_source := ""
var _debug_open := false

@onready var _editor: CodeEdit = $VBox/Tabs/Editor/CodeArea
@onready var _run_btn: Button = $VBox/Tabs/Editor/Buttons/RunBtn
@onready var _reset_btn: Button = $VBox/Tabs/Editor/Buttons/ResetBtn
@onready var _ref_btn: Button = $VBox/Tabs/Editor/Buttons/RefBtn
@onready var _debug_btn: Button = $VBox/Tabs/Editor/Buttons/DebugBtn
@onready var _error_view: ErrorView = $VBox/Tabs/Editor/ErrorView
@onready var _api_tab: ApiReferenceTab = $VBox/Tabs/API
@onready var _glossary_tab: GlossaryTab = $VBox/Tabs/Glossario


func _ready() -> void:
	_run_btn.pressed.connect(_on_run)
	_reset_btn.pressed.connect(_on_reset)
	_ref_btn.pressed.connect(_on_view_ref)
	_debug_btn.pressed.connect(_on_debug_toggle)
	_setup_editor_style()


func setup_level(level_index: int, ref_source: String) -> void:
	_level_index = level_index
	_ref_source = ref_source
	var saved := _store.load_or_empty(level_index)
	if saved != "":
		_editor.text = saved
	else:
		_editor.text = _skeleton_provider.skeleton(level_index)
	_player_source = _editor.text
	_error_view.clear()
	_api_tab.populate(WarriorApiCatalog.entries_for_level(level_index))
	_glossary_tab.populate(GlossaryCatalog.entries_for_level(level_index))


func show_compile_error(msg: String) -> void:
	_error_view.show_error(msg)


func clear_error() -> void:
	_error_view.clear()


func _on_run() -> void:
	_player_source = _editor.text
	_store.save(_level_index, _player_source)
	_error_view.clear()
	run_pressed.emit(_player_source)


func _on_reset() -> void:
	_editor.text = _skeleton_provider.skeleton(_level_index)
	_player_source = _editor.text
	_error_view.clear()


func _on_view_ref() -> void:
	if _editor.text == _ref_source:
		_editor.text = _player_source
	else:
		_player_source = _editor.text
		_editor.text = _ref_source


func _on_debug_toggle() -> void:
	_debug_open = not _debug_open
	debug_toggled.emit(_debug_open)


func _setup_editor_style() -> void:
	_editor.syntax_highlighter = CodeHighlighter.new()
	var highlighter := _editor.syntax_highlighter as CodeHighlighter
	highlighter.add_keyword_color("func", Color(0.5, 0.7, 1.0))
	highlighter.add_keyword_color("var", Color(0.5, 0.7, 1.0))
	highlighter.add_keyword_color("if", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("else", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("elif", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("while", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("for", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("return", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("true", Color(0.4, 0.9, 0.5))
	highlighter.add_keyword_color("false", Color(0.4, 0.9, 0.5))
	highlighter.add_keyword_color("null", Color(0.7, 0.7, 0.7))
	highlighter.add_keyword_color("pass", Color(0.7, 0.7, 0.7))
	highlighter.add_keyword_color("extends", Color(0.5, 0.7, 1.0))
	highlighter.add_keyword_color("and", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("or", Color(0.8, 0.5, 0.8))
	highlighter.add_keyword_color("not", Color(0.8, 0.5, 0.8))
	highlighter.symbol_color = Color(0.8, 0.8, 0.5)
	highlighter.number_color = Color(0.6, 1.0, 0.6)
	highlighter.add_color_region('"', '"', Color(0.9, 0.7, 0.5))
	highlighter.add_color_region("'", "'", Color(0.9, 0.7, 0.5))
	highlighter.add_color_region("#", "", Color(0.5, 0.8, 0.5), true)
	_editor.add_theme_font_size_override("font_size", 14)
	_editor.gutters_draw_line_numbers = true
	_editor.highlight_current_line = true
