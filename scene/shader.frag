#version 330 core
/*
*/

//in vec3 fPosition;
//in vec3 fNormal;
in vec4 vColor;
in vec2 vUV;

out vec4 fColor;

uniform sampler2D uTex0;
uniform vec4 uColor;

void main(){
    vec4 tex_color=texture(uTex0, vUV);
    //tex_color=vec4(1, 1, 1, 1);
    fColor = tex_color * uColor;
    //outColor = fColor;
	//outColor=vec4(fUV, 0, 1);
}
