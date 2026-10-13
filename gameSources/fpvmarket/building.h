#pragma once
#define NOMINMAX
#include "windows.h"
#include "svbmath.h"
#include "glad/glad.h"
#include "texture.h"
#include <vector>
#include "bounds.h"
#include "camera.h"

struct BuildingSettings{
    svbmath::Vec3 storeCenter;
    svbmath::Vec3 warehouseCenter;

    float storeWidth;
    float storeLength;
    float storeHeight;

    float warehouseWidth;
    float warehouseLength;
    float warehouseHeight;

    svbmath::Vec3 min;
    svbmath::Vec3 max;
};
struct Shelf{
    svbmath::Vec3 position;

    float width;
    float height;
    float depth;

    svbmath::Vec3 min;
    svbmath::Vec3 max;

    GLuint texture;
};
struct CashRegister{
    svbmath::Vec3 position;

    float width;
    float height;
    float depth;

    svbmath::Vec3 min;
    svbmath::Vec3 max;
};

class Building {
private:
    BuildingSettings build;
    std::vector<Shelf> shelves;

    CashRegister cashRegister;
public:
    void DrawWallOpeningThickness(svbmath::Vec3 wallStart, svbmath::Vec3 wallEnd, float height,
        float openingStart, float openingEnd, float thickness, bool horizontal, GLuint texture);
    CashRegister& getCashRegister();
    BuildingSettings& getBuildSettings();
    std::vector<Shelf>& getShelves();

    void DrawQuad(svbmath::Vec3 a, svbmath::Vec3 b, svbmath::Vec3 c, svbmath::Vec3 d,
        GLuint texture = 0);
    void DrawWallWithOpening(svbmath::Vec3 wallStart, svbmath::Vec3 wallEnd, float height,
        float openingStart, float openingEnd, bool horizontal, GLuint texture);
    void DrawFloor(float minX, float maxX, float minZ, float maxZ);
    void DrawCeiling(float minX, float maxX, float minZ, float maxZ, float height);
    void DrawBox(svbmath::Vec3 center, float width, float height, float depth, GLuint texture);
    void DrawShelf(const Shelf& shelf);
    void DrawCashRegister(const CashRegister& cash);
    void CreateBuilding();
    void DrawBuilding();
    bool checkCollision(Camera& cam);
    
};
