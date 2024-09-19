#version 330 core

layout (location = 0) in vec2 in_texture_coord_0;
layout (location = 1) in vec3 in_position;

// sends uv variable to fragment shader
out vec2 uv_0;

uniform mat4 model_matrix;


void main() {
    uv_0 = in_texture_coord_0;
    gl_Position = model_matrix * vec4(in_position, 1.0);
}
