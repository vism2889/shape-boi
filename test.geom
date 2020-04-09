// Name: Morgan Visnesky
// AndrewID: mvisnesk
// File: test.geom
//
// Citation: default for kodelife GLSL IDE
// plan on writing my own if I can get this to work


#version 150

layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;

in VertexData
{
    vec4 v_position;
    vec3 v_normal;
    vec2 v_texcoord;
} inData[];

out VertexData
{
    vec4 v_position;
    vec3 v_normal;
    vec2 v_texcoord;
} outData;

uniform float time;
uniform vec2 resolution;
uniform vec2 mouse;
uniform vec3 spectrum;
uniform mat4 mvp;

void main()
{
    outData.v_texcoord = inData[0].v_texcoord;
    outData.v_normal = inData[0].v_normal;
    gl_Position = gl_in[0].gl_Position;
    EmitVertex();

    outData.v_texcoord = inData[1].v_texcoord;
    outData.v_normal = inData[1].v_normal;
    gl_Position = gl_in[1].gl_Position;
    EmitVertex();

    outData.v_texcoord = inData[2].v_texcoord;
    outData.v_normal = inData[2].v_normal;
    gl_Position = gl_in[2].gl_Position;
    EmitVertex();

    EndPrimitive();
}
