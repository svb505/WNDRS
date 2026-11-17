#include "RoadRenderer.h"

#include <cmath>
#include <iostream>
#include <cstddef>

#include "logger.h"

struct RoadVertex {
    float x, y, z;
    float u, v;
};

bool RoadRenderer::Initialize(const std::string& shaderDirectory){
    auto loadShader = [](GLenum type, const std::string& path) -> GLuint{
            std::string source = DecorationRenderer::ReadFile(path);

            if (source.empty()) return 0;

            GLuint shader = glCreateShader(type);

            const char* src = source.c_str();

            glShaderSource(shader, 1, &src, nullptr);
            glCompileShader(shader);

            GLint success = GL_FALSE;
            glGetShaderiv(shader, GL_COMPILE_STATUS, &success);

            if (!success){
                char log[2048]{};
                glGetShaderInfoLog(shader, sizeof(log), nullptr, log);

                LOG_ERROR(std::format("Road shader error: {}",log));

                glDeleteShader(shader);
                return 0;
            }

            return shader;
        };

    GLuint vertex = loadShader( GL_VERTEX_SHADER, shaderDirectory + "/road.vert");

    GLuint fragment = loadShader( GL_FRAGMENT_SHADER, shaderDirectory + "/road.frag");

    if (!vertex || !fragment) return false;

    roadProgram = glCreateProgram();

    glAttachShader(roadProgram, vertex);
    glAttachShader(roadProgram, fragment);

    glLinkProgram(roadProgram);

    GLint success = GL_FALSE;

    glGetProgramiv(roadProgram, GL_LINK_STATUS, &success);

    glDeleteShader(vertex);
    glDeleteShader(fragment);

    if (!success){
        glDeleteProgram(roadProgram);
        roadProgram = 0;
        return false;
    }

    glGenVertexArrays(1, &vao);
    glGenBuffers(1, &vbo);
    glGenBuffers(1, &ebo);

    glBindVertexArray(vao);

    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData( GL_ARRAY_BUFFER, sizeof(RoadVertex) * 4,nullptr, GL_DYNAMIC_DRAW);

    GLuint indices[] = {
        0, 1, 2,
        0, 2, 3
    };

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);

    glBufferData(GL_ELEMENT_ARRAY_BUFFER,sizeof(indices),indices, GL_STATIC_DRAW);

    glEnableVertexAttribArray(0);

    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, sizeof(RoadVertex), (void*)offsetof(RoadVertex, x) );

    glEnableVertexAttribArray(1);

    glVertexAttribPointer( 1, 2, GL_FLOAT, GL_FALSE, sizeof(RoadVertex),(void*)offsetof(RoadVertex, u));

    glBindVertexArray(0);

    return true;
}
void RoadRenderer::SetMat4(const char* name, const float* matrix){
    GLint location = glGetUniformLocation(roadProgram, name);

    if (location != -1) glUniformMatrix4fv(location,1,GL_FALSE,matrix);
}
void RoadRenderer::SetLights(const std::vector<PointLight>& lights,const svbmath::Vec3& ambient){
    pointLights = lights;
    ambientColor = ambient;
}
void RoadRenderer::drawRoad(float startX,float startZ,float endX,float endZ,float y,float width, GLuint texture){
    float dx = endX - startX;
    float dz = endZ - startZ;

    float length = std::sqrt(dx * dx + dz * dz);

    if (length <= 0.001f) return;

    float offsetX = -dz / length * (width / 2.0f);
    float offsetZ = dx / length * (width / 2.0f);

    RoadVertex vertices[] = {
        { startX + offsetX, y, startZ + offsetZ, 1.0f, 0.0f },
        { endX + offsetX, y, endZ + offsetZ, 1.0f, length / 10.0f },
        { endX - offsetX, y, endZ - offsetZ, 0.0f, length / 10.0f },
        { startX - offsetX, y, startZ - offsetZ, 0.0f, 0.0f }
    };

    glUseProgram(roadProgram);

    // Матрицы камеры.
    float view[16]{};
    float projection[16]{};

    glGetFloatv(GL_MODELVIEW_MATRIX, view);
    glGetFloatv(GL_PROJECTION_MATRIX, projection);

    SetMat4("view", view);
    SetMat4("projection", projection);

    glUniform1i( glGetUniformLocation(roadProgram, "roadTexture"), 0);

    glUniform3f( glGetUniformLocation(roadProgram, "ambientColor"),
        ambientColor.x,ambientColor.y,ambientColor.z);

    constexpr int MAX_POINT_LIGHTS = 100;

    int count = static_cast<int>(std::min(pointLights.size(), size_t(MAX_POINT_LIGHTS)));

    glUniform1i(glGetUniformLocation(roadProgram, "pointLightCount"),count);

    for (int i = 0; i < count; ++i){
        const PointLight& light = pointLights[i];

        std::string pos ="pointLightPositionRadius[" + std::to_string(i) + "]";

        std::string color ="pointLightColorIntensity[" + std::to_string(i) + "]";

        glUniform4f(glGetUniformLocation(roadProgram, pos.c_str()),light.position.x,
            light.position.y,light.position.z,light.radius);

        glUniform4f(glGetUniformLocation(roadProgram, color.c_str()), light.color.x, 
            light.color.y,light.color.z, light.intensity);
    }

    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, texture);

    glBindVertexArray(vao);

    glBindBuffer(GL_ARRAY_BUFFER, vbo);

    glBufferSubData(GL_ARRAY_BUFFER,0,sizeof(vertices),vertices);

    glDrawElements(GL_TRIANGLES,6, GL_UNSIGNED_INT,nullptr);

    glBindVertexArray(0);

    glBindTexture(GL_TEXTURE_2D, 0);

    glUseProgram(0);
}

void RoadRenderer::drawRoadsFromJson(const nlohmann::json& levelJson, GLuint roadTexture){
    if (!levelJson.contains("roads") || !levelJson["roads"].is_array()) return;

    for (const auto& road : levelJson["roads"]){
        try{
            const auto& start = road.at("start");
            const auto& end = road.at("end");

            if (!start.is_array() || !end.is_array() || start.size() < 3 || end.size() < 3)
                continue;

            float startX = start[0].get<float>();
            float startY = start[1].get<float>() + 0.01f;
            float startZ = start[2].get<float>();

            float endX = end[0].get<float>();
            float endZ = end[2].get<float>();

            float width = road.value("width", 6.0f);

            drawRoad( startX,startZ,endX,endZ,startY,width,roadTexture );
        }
        catch (const std::exception& e){ LOG_ERROR(std::format("Invalid road JSON: {}", e.what()));
        }
    }
}

void RoadRenderer::Shutdown(){
    if (vbo) glDeleteBuffers(1, &vbo);
    if (ebo) glDeleteBuffers(1, &ebo);
    if (vao) glDeleteVertexArrays(1, &vao);
    if (roadProgram) glDeleteProgram(roadProgram);

    vbo = ebo = vao = roadProgram = 0;
}