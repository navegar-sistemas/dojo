shader_type canvas_item;
render_mode unshaded;

uniform float intensity : hint_range(0.0, 1.0) = 0.0;
uniform float time_val : hint_range(0.0, 100000.0) = 0.0;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

void fragment() {
	if (intensity < 0.005) {
		COLOR = vec4(0.0);
		return;
	}
	vec2 uv = SCREEN_UV;

	// Aberração cromática / RGB split
	float split = intensity * 0.007;
	float r = texture(screen_texture, uv + vec2(split, 0.0)).r;
	float g = texture(screen_texture, uv).g;
	float b = texture(screen_texture, uv - vec2(split, 0.0)).b;

	// Scanlines
	float line = fract(uv.y * 250.0 + time_val * 0.03);
	float scan = 1.0 - step(0.5, line) * intensity * 0.25;

	// Ruído de bloco leve (determinístico por frame)
	float noise_x = fract(sin(uv.x * 127.1 + time_val * 0.01) * 43758.5453);
	float noise_y = fract(sin(uv.y * 311.7 + time_val * 0.007) * 43758.5453);
	float noise = (noise_x * noise_y) * intensity * 0.08;

	COLOR = vec4((r + noise) * scan, g * scan, b * scan, intensity * 0.85);
}
