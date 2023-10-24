from glumpy import app, gloo, gl
from compyl.compyl3 import *
glsl_code_example = '''void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Define the camera position and direction
    vec3 camPos = vec3(0.0, 0.0, 3.0);
    vec3 camDir = normalize(vec3(fragCoord - iResolution.xy / 2.0, -iResolution.y));

    // Define vertices of a triangle
    vec3 vertexA = vec3(0.0, 1.0, 0.0);
    vec3 vertexB = vec3(-1.0, -1.0, 0.0);
    vec3 vertexC = vec3(1.0, -1.0, 0.0);

    // Ray-triangle intersection
    vec3 rayOrigin = camPos;
    vec3 rayDirection = camDir;

    vec3 edge1 = vertexB - vertexA;
    vec3 edge2 = vertexC - vertexA;
    vec3 h = cross(rayDirection, edge2);
    float a = dot(edge1, h);

    if (abs(a) > 0.0001) {
        float f = 1.0 / a;
        vec3 s = rayOrigin - vertexA;
        float u = f * dot(s, h);
        if (u >= 0.0 && u <= 1.0) {
            vec3 q = cross(s, edge1);
            float v = f * dot(rayDirection, q);
            if (v >= 0.0 && u + v <= 1.0) {
                float t = f * dot(edge2, q);

                if (t > 0.0) {
                    // Ray intersects the triangle

                    // Phong shading parameters
                    vec3 lightPos = vec3(-8.0, 7.0, 5.0);
                    vec3 normal = normalize(cross(edge1, edge2));
                    vec3 lightDir = normalize(lightPos - rayOrigin);
                    vec3 viewDir = normalize(camPos - rayOrigin);
                    vec3 reflectDir = reflect(-lightDir, normal);
                    float ambientStrength = 0.1;
                    float diffuseStrength = max(dot(normal, lightDir), 0.0);
                    float specularStrength = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

                    vec3 ambientColor = vec3(0.2, 0.2, 0.2);
                    vec3 diffuseColor = vec3(1.0, 0.0, 0.0); // Red color
                    vec3 specularColor = vec3(1.0, 1.0, 1.0);

                    vec3 finalColor = ambientStrength * ambientColor +
                                     diffuseStrength * diffuseColor +
                                     specularStrength * specularColor;

                    fragColor = vec4(finalColor, 1.0);
                    return;
                }
            }
        }
    }

    // Ray misses the triangle
    fragColor = vec4(0.0, 0.0, 0.0, 1.0); // Background color
}'''
