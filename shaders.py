vertex_shader = '''
#version 450 core

layout (location = 0 ) in vec3 position;
layout (location = 1 ) in vec2 texCoords;
layout (location = 2 ) in vec3 normals;



uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;


out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec4 newPos = vec4(position.x, position.y, position.z, 1);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;


}


'''

fragmet_shader = '''
#version 450 core

layout (binding  = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);    
    fragColor = texture(tex, UVs) * max(0, (min(1,intensity)));
}
'''



vertex_shader1 = '''
#version 450 core

layout (location = 0 ) in vec3 position;
layout (location = 1 ) in vec2 texCoords;
layout (location = 2 ) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
  
    float waveHeight = 0.5; // Ajusta la altura de la onda
    float waveSpeed = 2.0;  // Ajusta la velocidad de la onda
    float offsetY = sin(time * waveSpeed + position.x * 2.0) * waveHeight;

    vec4 newPos = vec4(position.x, position.y + offsetY, position.z, 1.0);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
}


'''

fragmet_shader1 = '''
#version 450 core

layout (binding  = 0) uniform sampler2D tex;

uniform vec3 dirLight;
uniform float time;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(normalize(outNormals), normalize(-dirLight));
    
    // Efecto de pixelación
    float pixelSize = 100.0; // Aumenta este número para más pixelación
    vec2 pixelUv = floor(UVs * pixelSize) / pixelSize;
    
    fragColor = texture(tex, pixelUv) * max(intensity, 0.1); // Usa la intensidad con un mínimo para evitar que esté demasiado oscuro
}
'''




fragmet_shader2 = '''
#version 450 core

layout (binding  = 0) uniform sampler2D tex;

uniform vec3 dirLight;
uniform float time;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    vec3 normal = normalize(outNormals);
    vec3 lightDir = normalize(-dirLight);

    float intensity = dot(normal, lightDir);
    float edgeIntensity = smoothstep(0.0, 1.0, intensity);

    vec4 texColor = texture(tex, UVs);

    vec3 glowColor = vec3(0.0, 1.0, 0.0); // verde fosforescente

  
    float glowFactor = 0.5;


    vec3 glow = glowColor * (1.0 - edgeIntensity) * glowFactor;


    vec3 finalColor = texColor.rgb * intensity + glow;

    fragColor = vec4(finalColor, texColor.a);
}

'''


vertex_shader2 = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time; // Un uniform para controlar la 'explosión' con el tiempo.

out vec2 UVs;
out vec3 outNormals;

void main() {
    float explosionIntensity = 0.5; // Controla qué tan lejos se mueven los vértices.
    float speed = 2.0; // Controla qué tan rápido sucede la explosión.


    float displacement = (1.0 + sin(time * speed)) * explosionIntensity;

  
    vec3 displaceDirection = normalize(normals);


    vec3 newPosition = position + displaceDirection * displacement;


    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPosition, 1.0);

   
    UVs = texCoords;
    outNormals = normals; // Si quieres que la luz reaccione a la explosión, deberías transformar las normales con la modelMatrix.
}


'''

vertex_shader3 = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec4 clipPlane; // Plane en forma de vec4 (a, b, c, d) donde ax + by + cz + d = 0.

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    float distance = dot(worldPosition, clipPlane); // Distancia desde el plano de corte
    
    if (distance > 0.0) { // Si la distancia es positiva, el vértice está "arriba" del plano
        // Puedes aplicar aquí la transformación que desees para los vértices "cortados"
        worldPosition.xyz += clipPlane.xyz * 0.1; // Mueve los vértices en la dirección del plano
    }

    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
}


'''


fragmet_shader3 = '''
#version 450 core

out vec4 fragColor;

uniform float time; // Se puede usar para animar el cambio de color.

void main()
{

    float r = abs(sin(gl_FragCoord.x * 0.01 + time));
    float g = abs(sin(gl_FragCoord.x * 0.01 + time + 2.09439)); // 120 grados de desfase
    float b = abs(sin(gl_FragCoord.x * 0.01 + time + 4.18879)); // 240 grados de desfase

    fragColor = vec4(r, g, b, 1.0);
}



'''