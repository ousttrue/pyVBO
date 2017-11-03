#version 330 core

//in vec3 fPosition;
//in vec3 fNormal;
in vec4 fColor;
in vec2 fUV;

out vec4 outColor;

uniform sampler2D Tex0;

void main(){
    outColor = texture(Tex0, fUV) * fColor;
    //outColor = fColor;
	//outColor=vec4(fUV, 0, 1);
}
