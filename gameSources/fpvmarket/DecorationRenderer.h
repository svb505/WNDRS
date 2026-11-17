
#pragma once

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <map>
#include <memory>
#include <string>
#include <vector>

#include "decorations.h"

struct PointLight {
    svbmath::Vec3 position;
    svbmath::Vec3 color{ 1.0f, 0.85f, 0.6f };

    float intensity = 2.0f;
    float radius = 12.0f;
};

class DecorationRenderer {
private:
    GLFWwindow* window = nullptr;

    struct GPUModel {
        GLuint vao = 0;
        GLuint vbo = 0;
        GLsizei vertexCount = 0;
    };

    struct Mat4 {
        float m[16]{};

        static Mat4 Identity();
        static Mat4 Translation(float x, float y, float z);
        static Mat4 RotationY(float degrees);
        static Mat4 Scale(float x, float y, float z);
        static Mat4 LookAt(const svbmath::Vec3& eye,const svbmath::Vec3& center,const svbmath::Vec3& up);
        static Mat4 Ortho( float left, float right,
            float bottom, float top,float nearPlane, float farPlane);

        Mat4 operator*(const Mat4& other) const;
    };

    GLuint sceneProgram = 0;
    GLuint shadowProgram = 0;

    GLuint shadowFBO = 0;
    GLuint shadowTexture = 0;
    GLuint whiteTexture = 0;

    int shadowResolution = 1024;

    svbmath::Vec3 lightDirection{ -0.4f, -1.0f, -0.3f };
    svbmath::Vec3 lightColor{ 1.0f, 0.96f, 0.88f };
    svbmath::Vec3 ambientColor{ 0.25f, 0.25f, 0.28f };

    Mat4 lightSpaceMatrix;

    std::map<DecType, GPUModel> gpuModels;

    GLuint LoadShader(const std::string& vertexPath,const std::string& fragmentPath);

    GLuint CompileShader(GLenum type, const std::string& source);

    bool CreateShadowMap();
    bool CreateWhiteTexture();

    void UploadModel(DecType type, const OBJModel& model);

    Mat4 GetModelMatrix(const OBJModel& model,const DecorationInstance& decoration) const;

    void DrawShadow(const OBJModel& model,const DecorationInstance& decoration);

    void DrawLit( const OBJModel& model,const DecorationInstance& decoration, const svbmath::Vec3& cameraPosition);

    void UpdateLightMatrix();

    void SetMat4(GLuint program, const char* name, const Mat4& matrix);

    void SetVec3(GLuint program,const char* name,const svbmath::Vec3& value);

    std::vector<PointLight> pointLights;

    bool nightMode = false;

public:
    const std::vector<PointLight>& GetPointLights();

    static std::string ReadFile(const std::string& path);

    void initWindow(GLFWwindow* win);

    void SetNightMode(bool enabled);
    void UpdateStreetLights(const Decorations& decorations);

    DecorationRenderer() = default;
    ~DecorationRenderer();

    DecorationRenderer(const DecorationRenderer&) = delete;
    DecorationRenderer& operator=(const DecorationRenderer&) = delete;

    bool Initialize( const std::string& shaderDirectory = "shaders",int resolution = 1024 );

    void Render(Decorations& decorations, const svbmath::Vec3& cameraPosition,int viewportWidth,int viewportHeight);

    void SetLightDirection(const svbmath::Vec3& direction);
    void SetLightColor(const svbmath::Vec3& color);
    void SetAmbientColor(const svbmath::Vec3& color);

    void Shutdown();
};
