/* vim: set ft=c: */
#version 330 core

uniform mat4 uPVM;
uniform mat4 uM;
uniform mat4 uV;
uniform mat4 uVM;
uniform vec3 uLightDir=vec3(1, 1, -1);

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec4 aColor;
layout(location = 3) in vec2 aUV;

out vec4 vColor;
out vec2 vUV;

void main() {
    gl_Position = uPVM * vec4(aPosition, 1);

    /*
    vec3 fNormal = normalize((uM * vec4(aNormal, 0)).xyz);
    float diffuse = max(dot(-uLightDir, fNormal), 0);
    */
    
    vColor = aColor;
    vUV=aUV;
}
