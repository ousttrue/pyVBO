/* vim: set ft=c: */
#version 330 core

uniform mat4 PVM;
uniform mat4 M;
uniform mat4 V;
uniform mat4 VM;
uniform vec3 LightDir=vec3(1, 1, -1);

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inNormal;
layout(location = 2) in vec4 inColor;
layout(location = 3) in vec2 inUV;


out vec4 fColor;
out vec2 fUV;

void main() {
    gl_Position = PVM * vec4(inPosition, 1);

    vec3 fNormal = normalize((M * vec4(inNormal, 0)).xyz);
    float diffuse = max(dot(-LightDir, fNormal), 0);

    fColor = inColor * diffuse;
    fUV=inUV;
}
