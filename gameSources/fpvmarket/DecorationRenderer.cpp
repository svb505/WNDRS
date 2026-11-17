
#include "DecorationRenderer.h"

#include <fstream>
#include <sstream>
#include <iostream>
#include <cmath>
#include <cstddef>
#include "LoadingWin.h"

namespace {
    constexpr float PI = 3.14159265358979323846f;

    svbmath::Vec3 NormalizeSafe(const svbmath::Vec3& v){
        float length = svbmath::Length(v);

        if (length < 0.00001f) return { 0.0f, -1.0f, 0.0f };

        return v / length;
    }
}
void DecorationRenderer::initWindow(GLFWwindow* win) {
    window = win;
}
void DecorationRenderer::SetNightMode(bool enabled){
    nightMode = enabled;
}
void DecorationRenderer::UpdateStreetLights(const Decorations& decorations){
    pointLights.clear();

    if (!nightMode) return;

    constexpr float lampHeightOffset = 5.0f;
    constexpr int MAX_POINT_LIGHTS = 100;

    for (const DecorationInstance& instance : decorations.GetInstances()) {
        if (instance.type != DecType::LAMP) continue;

        if (pointLights.size() >= MAX_POINT_LIGHTS) break;

        PointLight light;

        light.position = {
            instance.position.x,
            instance.position.y + lampHeightOffset,
            instance.position.z
        };

        light.color = { 1.0f, 0.82f, 0.55f };
        light.intensity = 3.0f;
        light.radius = 12.0f;

        pointLights.push_back(light);
    }
}

DecorationRenderer::Mat4 DecorationRenderer::Mat4::Identity(){
    Mat4 result{};

    result.m[0] = 1.0f;
    result.m[5] = 1.0f;
    result.m[10] = 1.0f;
    result.m[15] = 1.0f;

    return result;
}
DecorationRenderer::Mat4 DecorationRenderer::Mat4::Translation( float x, float y, float z){
    Mat4 result = Identity();

    result.m[12] = x;
    result.m[13] = y;
    result.m[14] = z;

    return result;
}

DecorationRenderer::Mat4 DecorationRenderer::Mat4::Scale(float x, float y, float z){
    Mat4 result{};

    result.m[0] = x;
    result.m[5] = y;
    result.m[10] = z;
    result.m[15] = 1.0f;

    return result;
}
DecorationRenderer::Mat4 DecorationRenderer::Mat4::RotationY(float degrees){
    float angle = degrees * 3.14159265358979323846f / 180.0f;

    float c = cosf(angle);
    float s = sinf(angle);

    Mat4 result = Identity();

    result.m[0] = c;
    result.m[2] = -s;
    result.m[8] = s;
    result.m[10] = c;

    return result;
}
DecorationRenderer::Mat4 DecorationRenderer::Mat4::operator*( const Mat4& other) const{
    Mat4 result{};

    for (int col = 0; col < 4; ++col) {
        for (int row = 0; row < 4; ++row) {
            for (int k = 0; k < 4; ++k) {
                result.m[col * 4 + row] += m[k * 4 + row] * other.m[col * 4 + k];
            }
        }
    }

    return result;
}

DecorationRenderer::Mat4 DecorationRenderer::Mat4::LookAt( const svbmath::Vec3& eye,
    const svbmath::Vec3& center,const svbmath::Vec3& up){

    svbmath::Vec3 f = NormalizeSafe(center - eye);
    svbmath::Vec3 s = NormalizeSafe(svbmath::Cross(f, up));
    svbmath::Vec3 u = svbmath::Cross(s, f);

    Mat4 result = Identity();

    result.m[0] = s.x;
    result.m[1] = u.x;
    result.m[2] = -f.x;

    result.m[4] = s.y;
    result.m[5] = u.y;
    result.m[6] = -f.y;

    result.m[8] = s.z;
    result.m[9] = u.z;
    result.m[10] = -f.z;

    result.m[12] = -svbmath::Dot(s, eye);
    result.m[13] = -svbmath::Dot(u, eye);
    result.m[14] = svbmath::Dot(f, eye);

    return result;
}
DecorationRenderer::Mat4 DecorationRenderer::Mat4::Ortho(float left, float right,
    float bottom, float top,float nearPlane, float farPlane){
    Mat4 result = Identity();

    result.m[0] = 2.0f / (right - left);
    result.m[5] = 2.0f / (top - bottom);
    result.m[10] = -2.0f / (farPlane - nearPlane);

    result.m[12] = -(right + left) / (right - left);
    result.m[13] = -(top + bottom) / (top - bottom);
    result.m[14] = -(farPlane + nearPlane) / (farPlane - nearPlane);

    return result;
}

const std::vector<PointLight>& DecorationRenderer::GetPointLights(){
    return pointLights;
}
std::string DecorationRenderer::ReadFile(const std::string& path){
    std::ifstream file(path);

    if (!file.is_open()) {
        std::cerr << "Shader file not found: " << path << '\n';
        return {};
    }

    std::stringstream buffer;
    buffer << file.rdbuf();

    return buffer.str();
}

GLuint DecorationRenderer::CompileShader(GLenum type,const std::string& source){
    LoadingScreen::Show(window, "Compile shaders");

    GLuint shader = glCreateShader(type);

    const char* src = source.c_str();

    glShaderSource(shader, 1, &src, nullptr);
    glCompileShader(shader);

    GLint success = GL_FALSE;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);

    if (!success) {
        GLint length = 0;
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &length);

        std::string log(length > 0 ? length : 1, '\0');

        glGetShaderInfoLog(shader, length, nullptr, log.data());

        std::cerr << "Shader compilation failed:\n"  << log << '\n';

        glDeleteShader(shader);
        return 0;
    }

    return shader;
}
GLuint DecorationRenderer::LoadShader( const std::string& vertexPath, const std::string& fragmentPath){
    std::string vertexSource = ReadFile(vertexPath);
    std::string fragmentSource = ReadFile(fragmentPath);

    if (vertexSource.empty() || fragmentSource.empty()) return 0;

    GLuint vertex = CompileShader(GL_VERTEX_SHADER, vertexSource);
    GLuint fragment = CompileShader(GL_FRAGMENT_SHADER, fragmentSource);

    if (!vertex || !fragment) {
        if (vertex) glDeleteShader(vertex);
        if (fragment) glDeleteShader(fragment);

        return 0;
    }

    GLuint program = glCreateProgram();

    glAttachShader(program, vertex);
    glAttachShader(program, fragment);

    glLinkProgram(program);

    GLint success = GL_FALSE;
    glGetProgramiv(program, GL_LINK_STATUS, &success);

    if (!success) {
        GLint length = 0;
        glGetProgramiv(program, GL_INFO_LOG_LENGTH, &length);

        std::string log(length > 0 ? length : 1, '\0');

        glGetProgramInfoLog(program, length, nullptr, log.data());

        std::cerr << "Shader linking failed:\n" << log << '\n';

        glDeleteProgram(program);
        program = 0;
    }

    glDeleteShader(vertex);
    glDeleteShader(fragment);

    return program;
}
bool DecorationRenderer::Initialize( const std::string& shaderDirectory, int resolution){
    shadowResolution = resolution > 0 ? resolution : 1024;

    sceneProgram = LoadShader(
        shaderDirectory + "/decoration.vert",
        shaderDirectory + "/decoration.frag"
    );

    shadowProgram = LoadShader(
        shaderDirectory + "/decoration_shadow.vert",
        shaderDirectory + "/decoration_shadow.frag"
    );

    if (!sceneProgram || !shadowProgram)  return false;

    if (!CreateShadowMap()) return false;

    if (!CreateWhiteTexture()) return false;

    UpdateLightMatrix();

    return true;
}

bool DecorationRenderer::CreateShadowMap(){
    glGenFramebuffers(1, &shadowFBO);

    glGenTextures(1, &shadowTexture);

    glBindTexture(GL_TEXTURE_2D, shadowTexture);

    glTexImage2D( GL_TEXTURE_2D,  0, GL_DEPTH_COMPONENT24,shadowResolution, 
        shadowResolution, 0, GL_DEPTH_COMPONENT, GL_FLOAT, nullptr);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER);

    float borderColor[] = { 1.0f, 1.0f, 1.0f, 1.0f };

    glTexParameterfv( GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor);

    glBindFramebuffer(GL_FRAMEBUFFER, shadowFBO);

    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, shadowTexture, 0);

    glDrawBuffer(GL_NONE);
    glReadBuffer(GL_NONE);

    bool complete = glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE;

    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    glBindTexture(GL_TEXTURE_2D, 0);

    if (!complete) std::cerr << "Decoration shadow framebuffer is incomplete\n";

    return complete;
}
bool DecorationRenderer::CreateWhiteTexture(){
    const unsigned char white[] = { 255, 255, 255, 255 };

    glGenTextures(1, &whiteTexture);
    glBindTexture(GL_TEXTURE_2D, whiteTexture);

    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA, 1, 1,0, GL_RGBA, GL_UNSIGNED_BYTE, white);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

    glBindTexture(GL_TEXTURE_2D, 0);

    return whiteTexture != 0;
}
void DecorationRenderer::UploadModel(DecType type,const OBJModel& model){
    const auto& vertices = model.GetVertices();

    if (vertices.empty()) return;

    GPUModel gpu{};

    gpu.vertexCount = static_cast<GLsizei>(vertices.size());

    glGenVertexArrays(1, &gpu.vao);
    glGenBuffers(1, &gpu.vbo);

    glBindVertexArray(gpu.vao);

    glBindBuffer(GL_ARRAY_BUFFER, gpu.vbo);

    glBufferData( GL_ARRAY_BUFFER, vertices.size() * sizeof(Vertex),vertices.data(),GL_STATIC_DRAW);

    glEnableVertexAttribArray(0);

    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex),reinterpret_cast<void*>(offsetof(Vertex, x)));

    glEnableVertexAttribArray(1);

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), reinterpret_cast<void*>(offsetof(Vertex, nx)));

    glEnableVertexAttribArray(2);

    glVertexAttribPointer( 2, 2, GL_FLOAT, GL_FALSE,sizeof(Vertex),reinterpret_cast<void*>(offsetof(Vertex, u)));

    glBindVertexArray(0);
    glBindBuffer(GL_ARRAY_BUFFER, 0);

    gpuModels[type] = gpu;
}

DecorationRenderer::Mat4 DecorationRenderer::GetModelMatrix(const OBJModel& model,const DecorationInstance& decoration) const{
    float s = model.scale;

    return Mat4::Translation(decoration.position.x,decoration.position.y,decoration.position.z)
        * Mat4::RotationY(decoration.rotationY) * Mat4::Scale(s, s, s);
}

void DecorationRenderer::UpdateLightMatrix(){
    svbmath::Vec3 direction = NormalizeSafe(lightDirection);

    // center of zone of decorations
    svbmath::Vec3 target{ 0.0f, 0.0f, 0.0f };

    svbmath::Vec3 lightPosition = target - direction * 40.0f;

    Mat4 lightView = Mat4::LookAt(
        lightPosition,
        target,
        { 0.0f, 1.0f, 0.0f }
    );

    Mat4 lightProjection = Mat4::Ortho(
        -35.0f, 35.0f,
        -35.0f, 35.0f,
        0.1f, 100.0f
    );

    lightSpaceMatrix = lightProjection * lightView;
}
void DecorationRenderer::SetMat4( GLuint program,const char* name, const Mat4& matrix){
    GLint location = glGetUniformLocation(program, name);

    if (location != -1)  glUniformMatrix4fv(location, 1, GL_FALSE, matrix.m);
}
void DecorationRenderer::SetVec3(GLuint program,const char* name,const svbmath::Vec3& value){
    GLint location = glGetUniformLocation(program, name);

    if (location != -1) glUniform3f(location,value.x,value.y, value.z);
}

void DecorationRenderer::DrawShadow( const OBJModel& model, const DecorationInstance& decoration){
    auto it = gpuModels.find(decoration.type);

    if (it == gpuModels.end()) return;

    const GPUModel& gpu = it->second;

    Mat4 modelMatrix = GetModelMatrix(model, decoration);

    SetMat4(shadowProgram, "model", modelMatrix);

    glBindVertexArray(gpu.vao);

    glDrawArrays(GL_TRIANGLES,0,gpu.vertexCount);

    glBindVertexArray(0);
}
void DecorationRenderer::DrawLit(const OBJModel& model,const DecorationInstance& decoration,const svbmath::Vec3& cameraPosition){
    auto it = gpuModels.find(decoration.type);

    if (it == gpuModels.end())  return;

    const GPUModel& gpu = it->second;

    Mat4 modelMatrix = GetModelMatrix(model, decoration);

    SetMat4(sceneProgram, "model", modelMatrix);

    SetVec3(sceneProgram, "viewPosition", cameraPosition);


    GLint lampLocation =  glGetUniformLocation(sceneProgram, "isLamp");

    GLint emissiveColorLocation = glGetUniformLocation(sceneProgram, "emissiveColor");

    GLint emissiveStrengthLocation = glGetUniformLocation(sceneProgram, "emissiveStrength");

    bool isEmissive = decoration.type == DecType::LAMP && nightMode;

    glUniform1i(lampLocation, isEmissive ? 1 : 0);
    glUniform3f(emissiveColorLocation, 1.0f, 0.75f, 0.4f);
    glUniform1f(emissiveStrengthLocation,2.5f);

    glBindVertexArray(gpu.vao);

    const auto& groups = model.GetMaterialGroups();

    if (groups.empty()) {
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, whiteTexture);

        SetVec3(sceneProgram, "materialDiffuse", { 1.0f, 1.0f, 1.0f });

        glUniform1f( glGetUniformLocation(sceneProgram, "materialSpecular"), 0.2f);

        glUniform1f( glGetUniformLocation(sceneProgram, "materialShininess"), 32.0f );
        glUniform1f( glGetUniformLocation(sceneProgram, "materialAlpha"), 1.0f);

        glDrawArrays( GL_TRIANGLES,0,gpu.vertexCount);
    }
    else {
        for (const MaterialGroup& group : groups) {

            const Material& material = group.material;

            SetVec3(sceneProgram,"materialDiffuse", { material.Kd[0], material.Kd[1], material.Kd[2] } );

            GLint specularLocation = glGetUniformLocation(sceneProgram, "materialSpecular");

            if (specularLocation != -1) glUniform1f(specularLocation, material.Ks[0]);

            GLint shininessLocation = glGetUniformLocation(sceneProgram, "materialShininess");

            if (shininessLocation != -1)
                glUniform1f( shininessLocation, material.Ns > 0.0f ? material.Ns : 32.0f);

            GLint alphaLocation = glGetUniformLocation(sceneProgram, "materialAlpha");

            if (alphaLocation != -1)  glUniform1f(alphaLocation, material.d);

            GLuint texture = material.textureID;

            if (!texture) texture = model.GetTexture();

            if (!texture) texture = whiteTexture;

            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_2D, texture);

            glDrawArrays( GL_TRIANGLES,static_cast<GLint>(group.startVertex),static_cast<GLsizei>(group.vertexCount));
        }
    }

    glBindVertexArray(0);
}

void DecorationRenderer::Render(Decorations& decorations, const svbmath::Vec3& cameraPosition,int viewportWidth,int viewportHeight){
    if (!sceneProgram || !shadowProgram || viewportWidth <= 0 || viewportHeight <= 0) return;

    // loading GPU-geometry
    for (const auto& [type, model] : decorations.GetModels()) {
        if (!model) continue;

        if (gpuModels.find(type) == gpuModels.end()) UploadModel(type, *model);
    }

    // saving OpenGL state
    GLint oldFramebuffer = 0;
    GLint oldViewport[4]{};

    glGetIntegerv(GL_FRAMEBUFFER_BINDING, &oldFramebuffer);
    glGetIntegerv(GL_VIEWPORT, oldViewport);

    GLboolean oldCull = glIsEnabled(GL_CULL_FACE);
    GLboolean oldBlend = glIsEnabled(GL_BLEND);
    GLboolean oldDepth = glIsEnabled(GL_DEPTH_TEST);

    GLboolean oldDepthMask = GL_TRUE;
    glGetBooleanv(GL_DEPTH_WRITEMASK, &oldDepthMask);

    // taking current camera martix after cam.setupCamera().
    Mat4 view{};
    Mat4 projection{};

    glGetFloatv(GL_MODELVIEW_MATRIX, view.m);
    glGetFloatv(GL_PROJECTION_MATRIX, projection.m);

    UpdateLightMatrix();

    const auto& instances = decorations.GetInstances();
    const auto& models = decorations.GetModels();

    // Shadow map

    glBindFramebuffer(GL_FRAMEBUFFER, shadowFBO);

    glViewport( 0, 0,shadowResolution,shadowResolution);

    glClear(GL_DEPTH_BUFFER_BIT);

    glEnable(GL_DEPTH_TEST);
    glDepthMask(GL_TRUE);

    glEnable(GL_CULL_FACE);
    glCullFace(GL_FRONT);

    glDisable(GL_BLEND);

    glUseProgram(shadowProgram);

    SetMat4(shadowProgram,"lightSpaceMatrix", lightSpaceMatrix );

    for (const DecorationInstance& decoration : instances) {

        auto modelIt = models.find(decoration.type);

        if (modelIt == models.end() || !modelIt->second) continue;

        DrawShadow(*modelIt->second, decoration);
    }

    glCullFace(GL_BACK);

    //Normal rendering

    glBindFramebuffer(GL_FRAMEBUFFER, static_cast<GLuint>(oldFramebuffer));

    glViewport(oldViewport[0],oldViewport[1],oldViewport[2],oldViewport[3]);

    glEnable(GL_DEPTH_TEST);
    glDepthMask(GL_TRUE);

    glUseProgram(sceneProgram);

    SetMat4(sceneProgram, "view", view);
    SetMat4(sceneProgram, "projection", projection);
    SetMat4(sceneProgram, "lightSpaceMatrix", lightSpaceMatrix);

    SetVec3(sceneProgram, "lightDirection", lightDirection);
    SetVec3(sceneProgram, "lightColor", lightColor);
    SetVec3(sceneProgram, "ambientColor", ambientColor);
    SetVec3(sceneProgram, "viewPosition", cameraPosition);

    glUniform1i( glGetUniformLocation(sceneProgram, "diffuseTexture"), 0);

    glUniform1i(glGetUniformLocation(sceneProgram, "shadowMap"),1);

    glUniform1i(glGetUniformLocation(sceneProgram, "pointLightCount"),static_cast<GLint>(pointLights.size()));

    for (size_t i = 0; i < pointLights.size(); ++i){
        const PointLight& light = pointLights[i];

        std::string positionName = "pointLightPositionRadius[" + std::to_string(i) + "]";

        std::string colorName = "pointLightColorIntensity[" + std::to_string(i) + "]";

        GLint positionLocation = glGetUniformLocation( sceneProgram, positionName.c_str());

        GLint colorLocation = glGetUniformLocation( sceneProgram, colorName.c_str());

        glUniform4f(positionLocation,light.position.x, light.position.y,light.position.z,light.radius);

        glUniform4f( colorLocation,light.color.x,light.color.y,light.color.z,light.intensity);
    }

    glActiveTexture(GL_TEXTURE1);
    glBindTexture(GL_TEXTURE_2D, shadowTexture);

    glActiveTexture(GL_TEXTURE0);

    glEnable(GL_CULL_FACE);
    glCullFace(GL_BACK);
    glFrontFace(GL_CCW);

    for (const DecorationInstance& decoration : instances) {

        auto modelIt = models.find(decoration.type);

        if (modelIt == models.end() || !modelIt->second) continue;

        DrawLit( *modelIt->second,decoration, cameraPosition);
    }

    // Restore OpenGL state

    glUseProgram(0);

    glBindVertexArray(0);

    glActiveTexture(GL_TEXTURE1);
    glBindTexture(GL_TEXTURE_2D, 0);

    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, 0);

    if (!oldCull) glDisable(GL_CULL_FACE);
    if (!oldBlend) glDisable(GL_BLEND);
    if (!oldDepth) glDisable(GL_DEPTH_TEST);

    glDepthMask(oldDepthMask);

    glBindFramebuffer( GL_FRAMEBUFFER, static_cast<GLuint>(oldFramebuffer) );
}
void DecorationRenderer::SetLightDirection( const svbmath::Vec3& direction){
    lightDirection = NormalizeSafe(direction);
    UpdateLightMatrix();
}
void DecorationRenderer::SetLightColor(const svbmath::Vec3& color){
    lightColor = color;
}
void DecorationRenderer::SetAmbientColor(const svbmath::Vec3& color){
    ambientColor = color;
}

DecorationRenderer::~DecorationRenderer(){
    Shutdown();
}
void DecorationRenderer::Shutdown(){
    for (auto& [type, gpu] : gpuModels) {
        if (gpu.vbo) glDeleteBuffers(1, &gpu.vbo);
        if (gpu.vao) glDeleteVertexArrays(1, &gpu.vao);
    }

    gpuModels.clear();

    if (shadowTexture) glDeleteTextures(1, &shadowTexture);
    if (shadowFBO) glDeleteFramebuffers(1, &shadowFBO);
    if (whiteTexture) glDeleteTextures(1, &whiteTexture);
    if (sceneProgram) glDeleteProgram(sceneProgram);
    if (shadowProgram) glDeleteProgram(shadowProgram);

    shadowTexture = 0;
    shadowFBO = 0;
    whiteTexture = 0;
    sceneProgram = 0;
    shadowProgram = 0;
}
