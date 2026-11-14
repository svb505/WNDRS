#pragma once
#include <vector>
#include <string>
#include <glad/glad.h>
#include "svbmath.h"
#include "bounds.h"

struct Vertex {
    float x, y, z;       // position
    float nx, ny, nz;    // normal
    float u, v;          // UV
};
struct Material {
    std::string name;

    float Ka[3] = { 1.0f, 1.0f, 1.0f };
    float Kd[3] = { 1.0f, 1.0f, 1.0f };
    float Ks[3] = { 1.0f, 1.0f, 1.0f };

    float Ns = 0.0f;
    float d = 1.0f;

    std::string texturePath;
    GLuint textureID = 0;
};
struct LimbRig {
    size_t start = 0, count = 0;
    float px = 0, py = 0, pz = 0;   // точка вращения (бедро)
    float side = 1.0f;              // +1 левая, -1 правая
};
struct ObjPart {
    std::string name;
    Bounds bounds;
    size_t startVertex = 0;
    size_t vertexCount = 0;
};

struct MaterialGroup {
    Material material;
    size_t startVertex = 0;
    size_t vertexCount = 0;
};

class OBJModel {
private:
    std::vector<Vertex> vertices;
    std::vector<MaterialGroup> materialGroups;
    std::vector<Material> materials;
    std::vector<LimbRig> legRig;

    GLuint vbo = 0;
    GLuint texture = 0;
    bool LoadFromCache(const std::string& objPath, const std::string& cachePath);
    bool SaveCache(const std::string& objPath, const std::string& cachePath,
        const std::string& mtlPath) const;

    void BuildLegRig();
    void SetupArrays();
    void TeardownArrays();
    void ApplyMaterial(const MaterialGroup& g);
    void DrawRange(size_t begin, size_t end);
public:
    std::vector<ObjPart> parts;
    Bounds bounds;
    float scale = 0.0f;

    GLuint LoadTextureFromFile(const std::string& filename);
    bool LoadMTL(const std::string& filename);
    bool LoadOBJ(const std::string& filename, float scale);
    bool LoadTexture(const std::string& filename);

    void CreateVBO();
    void Draw(svbmath::Vec3 pos, float yaw, float pitch);

    void DrawWalking(svbmath::Vec3 pos, float yaw, float pitch,
        float walkPhase, float intensity = 1.0f, float swingDeg = 35.0f);

    ~OBJModel();
};