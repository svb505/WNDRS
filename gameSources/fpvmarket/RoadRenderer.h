#pragma once
#include <glad/glad.h>
#include <string>
#include <vector>
#include "model.h"
#include "DecorationRenderer.h"
#include <nlohmann//json.hpp>

class RoadRenderer {
public:
    bool Initialize(const std::string& shaderDirectory);

    void drawRoad( float startX, float startZ,float endX, float endZ, float y, float width, GLuint texture);

    void drawRoadsFromJson(const nlohmann::json& levelJson,GLuint roadTexture);

    void SetLights( const std::vector<PointLight>& lights, const svbmath::Vec3& ambient);

    void Shutdown();

private:
    GLuint roadProgram = 0;
    GLuint vao = 0;
    GLuint vbo = 0;
    GLuint ebo = 0;

    std::vector<PointLight> pointLights;

    svbmath::Vec3 ambientColor{ 0.15f, 0.15f, 0.15f };

    void SetMat4(const char* name, const float* matrix);
};