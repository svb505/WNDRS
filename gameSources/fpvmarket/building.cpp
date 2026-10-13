#define NOMINMAX
#include "windows.h"
#include "svbmath.h"
#include "glad/glad.h"
#include "texture.h"
#include <vector>
#include "bounds.h"
#include "building.h"

void Building::DrawWallOpeningThickness( svbmath::Vec3 wallStart,svbmath::Vec3 wallEnd, float height,
    float openingStart,float openingEnd,float thickness, bool horizontal, GLuint texture){
    float length = horizontal
        ? wallEnd.x - wallStart.x
        : wallEnd.z - wallStart.z;

    auto getPoint = [&](float offset, float y, float depth)
        -> svbmath::Vec3
        {
            if (horizontal)
                return { wallStart.x + offset, y, wallStart.z + depth };

            return { wallStart.x + depth, y, wallStart.z + offset };
        };

    // Нижняя грань всей стены
    DrawQuad(
        getPoint(0, 0, 0),
        getPoint(length, 0, 0),
        getPoint(length, 0, thickness),
        getPoint(0, 0, thickness),
        texture
    );

    // Верхняя грань всей стены
    DrawQuad(
        getPoint(0, height, 0),
        getPoint(length, height, 0),
        getPoint(length, height, thickness),
        getPoint(0, height, thickness),
        texture
    );

    // Торец начала стены
    DrawQuad(
        getPoint(0, 0, 0),
        getPoint(0, 0, thickness),
        getPoint(0, height, thickness),
        getPoint(0, height, 0),
        texture
    );

    // Торец конца стены
    DrawQuad(
        getPoint(length, 0, thickness),
        getPoint(length, 0, 0),
        getPoint(length, height, 0),
        getPoint(length, height, thickness),
        texture
    );

    // Торцы прохода — только на его боковых границах
    DrawQuad(
        getPoint(openingStart, 0, 0),
        getPoint(openingStart, 0, thickness),
        getPoint(openingStart, 2.2f, thickness),
        getPoint(openingStart, 2.2f, 0),
        texture
    );

    DrawQuad(
        getPoint(openingEnd, 0, thickness),
        getPoint(openingEnd, 0, 0),
        getPoint(openingEnd, 2.2f, 0),
        getPoint(openingEnd, 2.2f, thickness),
        texture
    );
}
std::vector<Shelf>& Building::getShelves() {
    return shelves;
}
CashRegister& Building::getCashRegister() {
    return cashRegister;
}
BuildingSettings& Building::getBuildSettings() {
    return build;
}
void Building::DrawQuad(svbmath::Vec3 a, svbmath::Vec3 b, svbmath::Vec3 c, svbmath::Vec3 d,
    GLuint texture) {

    glColor3f(1.0f, 1.0f, 1.0f);

    if (texture != 0) {
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, texture);
    }
    else glDisable(GL_TEXTURE_2D);

    glBegin(GL_QUADS);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(a.x, a.y, a.z);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(b.x, b.y, b.z);

    glTexCoord2f(1.0f, 1.0f);
    glVertex3f(c.x, c.y, c.z);

    glTexCoord2f(0.0f, 1.0f);
    glVertex3f(d.x, d.y, d.z);

    glEnd();

    glDisable(GL_TEXTURE_2D);
}
void Building::DrawWallWithOpening(svbmath::Vec3 wallStart, svbmath::Vec3 wallEnd, float height,
    float openingStart, float openingEnd, bool horizontal, GLuint texture) {

    float length;

    if (horizontal) length = wallEnd.x - wallStart.x;
    else length = wallEnd.z - wallStart.z;

    if (openingStart > 0.0f) {
        if (horizontal) {
            DrawQuad(
                { wallStart.x, 0.0f, wallStart.z },
                { wallStart.x + openingStart, 0, wallStart.z },
                { wallStart.x + openingStart, height, wallStart.z },
                { wallStart.x, height, wallStart.z },
                texture
            );
        }
        else
        {
            DrawQuad(
                { wallStart.x, 0, wallStart.z },
                { wallStart.x, 0, wallStart.z + openingStart },
                { wallStart.x, height, wallStart.z + openingStart },
                { wallStart.x, height, wallStart.z },
                texture
            );
        }
    }


    // --------------------------------------------------------
    // Часть стены ПОСЛЕ отверстия
    // --------------------------------------------------------

    if (openingEnd < length)
    {
        if (horizontal)
        {
            DrawQuad(
                { wallStart.x + openingEnd, 0, wallStart.z },
                { wallEnd.x, 0, wallEnd.z },
                { wallEnd.x, height, wallEnd.z },
                { wallStart.x + openingEnd, height, wallStart.z },
                texture
            );
        }
        else
        {
            DrawQuad(
                { wallStart.x, 0, wallStart.z + openingEnd },
                { wallStart.x, 0, wallEnd.z },
                { wallStart.x, height, wallEnd.z },
                { wallStart.x, height, wallStart.z + openingEnd },
                texture
            );
        }
    }


    // --------------------------------------------------------
    // Верхняя часть над дверью
    // --------------------------------------------------------

    if (horizontal)
    {
        DrawQuad(
            {
                wallStart.x + openingStart,
                2.2f,
                wallStart.z
            },
            {
                wallStart.x + openingEnd,
                2.2f,
                wallStart.z
            },
            {
                wallStart.x + openingEnd,
                height,
                wallStart.z
            },
            {
                wallStart.x + openingStart,
                height,
                wallStart.z
            },
            texture
        );
    }
    else
    {
        DrawQuad(
            {
                wallStart.x,
                2.2f,
                wallStart.z + openingStart
            },
            {
                wallStart.x,
                2.2f,
                wallStart.z + openingEnd
            },
            {
                wallStart.x,
                height,
                wallStart.z + openingEnd
            },
            {
                wallStart.x,
                height,
                wallStart.z + openingStart
            },
            texture
        );
    }
}
void Building::DrawFloor(float minX, float maxX, float minZ, float maxZ) {
    DrawQuad( { minX, 0.01f, minZ }, { maxX, 0.01f, minZ }, { maxX, 0.01f, maxZ }, { minX, 0.01f, maxZ },
        allTextures["FLOOR"]);
}
void Building::DrawCeiling(float minX, float maxX, float minZ, float maxZ, float height) {
    DrawQuad(
        { minX, height, minZ },
        { minX, height, maxZ },
        { maxX, height, maxZ },
        { maxX, height, minZ },
        allTextures["CEILING"]
    );
}
void Building::DrawBox(svbmath::Vec3 center, float width, float height, float depth, GLuint texture) {
    float x1 = center.x - width / 2.0f;
    float x2 = center.x + width / 2.0f;

    float y1 = center.y - height / 2.0f;
    float y2 = center.y + height / 2.0f;

    float z1 = center.z - depth / 2.0f;
    float z2 = center.z + depth / 2.0f;


    // Front
    DrawQuad(
        { x1, y1, z1 },
        { x2, y1, z1 },
        { x2, y2, z1 },
        { x1, y2, z1 },
        texture
    );

    // Back
    DrawQuad(
        { x2, y1, z2 },
        { x1, y1, z2 },
        { x1, y2, z2 },
        { x2, y2, z2 },
        texture
    );

    // Left
    DrawQuad(
        { x1, y1, z2 },
        { x1, y1, z1 },
        { x1, y2, z1 },
        { x1, y2, z2 },
        texture
    );

    // Right
    DrawQuad(
        { x2, y1, z1 },
        { x2, y1, z2 },
        { x2, y2, z2 },
        { x2, y2, z1 },
        texture
    );

    // Top
    DrawQuad(
        { x1, y2, z1 },
        { x2, y2, z1 },
        { x2, y2, z2 },
        { x1, y2, z2 },
        texture
    );

    // Bottom
    DrawQuad(
        { x1, y1, z2 },
        { x2, y1, z2 },
        { x2, y1, z1 },
        { x1, y1, z1 },
        texture
    );
}
void Building::DrawShelf(const Shelf& shelf) {
    DrawBox(shelf.position, shelf.width, shelf.height, shelf.depth, shelf.texture);
}
void Building::DrawCashRegister(const CashRegister& cash) {
    glDisable(GL_TEXTURE_2D);

    DrawBox(cash.position, cash.width, cash.height, cash.depth, allTextures["METAL"]);
}
void Building::CreateBuilding() {
    build.storeWidth = 12.0f;
    build.storeLength = 10.0f;
    build.storeHeight = 4.0f;

    build.storeCenter = { 0.0f,0.1f,0.0f };

    build.warehouseWidth = 4.0f;
    build.warehouseLength = 5.0f;
    build.warehouseHeight = 4.0f;

    build.warehouseCenter = { 8.0f,2.0f,-2.5f };

    build.min = { -6.0f,-1.0f,-5.0f };

    build.max = { 10.0f,4.0f,5.0f };

    shelves.clear();

    Shelf shelf1;

    shelf1.position = { -1.0f,1.0f,-3.8f };

    shelf1.width = 7.0f;
    shelf1.height = 1.2f;
    shelf1.depth = 0.7f;

    shelf1.texture = allTextures["WOOD"];

    Bounds aabb1 = MakeAABB(shelf1.position, shelf1.width + 0.3f, shelf1.height + 0.2f, shelf1.depth + 0.3f);

    shelf1.min = aabb1.min;
    shelf1.max = aabb1.max;

    shelves.push_back(shelf1);

    Shelf shelf2;

    shelf2.position = { 4.8f,1.0f,-0.8f };

    shelf2.width = 0.7f;
    shelf2.height = 1.2f;
    shelf2.depth = 5.0f;

    shelf2.texture = allTextures["WOOD"];

    Bounds aabb2 = MakeAABB( shelf2.position, shelf2.width + 0.3f, shelf2.height + 0.2f,shelf2.depth + 0.3f );

    shelf2.min = aabb2.min;
    shelf2.max = aabb2.max;

    shelves.push_back(shelf2);

    cashRegister.position = { -4.0f,0.7f, 3.7f };

    cashRegister.width = 1.5f;
    cashRegister.height = 1.6f;
    cashRegister.depth = 2.2f;

    Bounds cashAABB = MakeAABB(cashRegister.position,cashRegister.width + 0.3f,
        cashRegister.height + 0.2f, cashRegister.depth + 0.3f);

    cashRegister.min = cashAABB.min;
    cashRegister.max = cashAABB.max;
}
void Building::DrawBuilding() {
    float wallThickness = 0.2f;

    GLuint wall1Texture = allTextures["WALL1"];
    GLuint wall2Texture = allTextures["WALL2"];

    float sx1 = -6.0f;
    float sx2 = 6.0f;

    float sz1 = -5.0f;
    float sz2 = 5.0f;

    float h = 4.0f;

    DrawQuad({ sx1, 0.0f, sz1 }, { sx2, 0.0f, sz1 }, { sx2, h, sz1 },{ sx1, h, sz1 },
        wall1Texture);
    DrawQuad({ sx1, 0.0f, sz2 }, { sx1, 0.0f, sz1 }, { sx1, h, sz1 }, { sx1, h, sz2 },
        wall1Texture);

    DrawWallWithOpening({ sx1, 0.0f, sz2 }, { sx2, 0.0f, sz2 }, h, 5.0f, 7.0f, true,
        wall1Texture);

    DrawWallWithOpening({ sx2, 0.0f, sz1 }, { sx2, 0.0f, sz2 }, h, 1.0f, 3.0f, false,
        wall1Texture);

    DrawWallOpeningThickness(
        { sx1, 0.001f, sz2 - 0.2f },
        { sx2, 0.001f, sz2 },
        h, 5.0f, 7.0f, wallThickness, true,
        wall1Texture
    );

    DrawWallOpeningThickness(
        { sx2 - 0.2f, 0.001f, sz1},
        { sx2, 0.001f, sz2 },
        h, 1.0f, 3.0f, wallThickness, false,
        wall1Texture
    );

    float wx1 = 6.0f;
    float wx2 = 10.0f;

    float wz1 = -5.0f;
    float wz2 = 0.0f;

    DrawQuad({ wx1, 0.0f, wz1 },{ wx2, 0.0f, wz1 }, { wx2, h,wz1 }, { wx1, h, wz1 }, 
        wall2Texture);
    DrawQuad({ wx2, 0.0f, wz1 }, { wx2, 0.0f, wz2 },{ wx2, h,wz2 },{ wx2, h, wz1 },
        wall2Texture);
    DrawQuad( { wx2, 0.0f, wz2 },{ wx1, 0.0f, wz2 }, { wx1, h,wz2 },{ wx2, h,wz2 }, 
        wall2Texture);
    
    DrawFloor(-6.0f, 10.0f, -5.0f, 5.0f);

    DrawCeiling(-6.0f, 10.0f, -5.0f, 5.0f, h);

    for (const Shelf& shelf : shelves) DrawShelf(shelf);

    DrawCashRegister(cashRegister);
}
bool Building::checkCollision(Camera& cam) {
    svbmath::Vec3 pos = cam.getCamPos();

    // Склад
    float wx1 = 6.0f;
    float wx2 = 10.0f;

    float wz1 = -5.0f;
    float wz2 = 0.0f;

    // Магазин
    float sx1 = -6.0f;
    float sx2 = 6.0f;

    float sz1 = -5.0f;
    float sz2 = 5.0f;

    float h = 4.0f;

    // Задняя стена магазина
    if (checkAABBCollision({{ sx1, 0.0f, sz2 - 0.2f },{ -1.0f, h, sz2 + 0.2f }}, pos)) return true;
    if (checkAABBCollision({{ 1.0f, 0.0f, sz2 - 0.2f },{ sx2, h, sz2 + 0.2f }}, pos)) return true;
    // Левая стена магазина
    if (checkAABBCollision({{ sx1 - 0.2f, 0.0f, sz1 },{ sx1 + 0.2f, h, sz2 }}, pos)) return true;
    // Правая стена магазина, до двери
    if (checkAABBCollision({{ sx2 - 0.2f, 0.0f, sz1 },{ sx2 + 0.2f, h, -4.0f }}, pos)) return true;
    // Правая стена магазина, после двери
    if (checkAABBCollision({{ sx2 - 0.2f, 0.0f, -2.0f },{ sx2 + 0.2f, h, sz2 }}, pos)) return true;
    if (checkAABBCollision({{ sx1, 0.0f, sz1 - 0.2f },{ sx2, h,sz1 + 0.2f } }, pos)) return true;

    if (checkAABBCollision({{ wx1 - 0.2f, 0.0f, wz1 - 0.2f },{ wx2 + 0.2f, h, wz1 + 0.2f }}, pos)) return true;
    if (checkAABBCollision({{ wx2 - 0.2f, 0.0f, wz1 - 0.2f },{ wx2 + 0.2f, h, wz2 + 0.2f }}, pos)) return true;
    if (checkAABBCollision({{ wx1 - 0.2f, 0.0f, wz2 - 0.2f },
 { wx2 + 0.2f, h,    wz2 + 0.2f }}, pos)) return true;
    
    for (const Shelf& shelf : shelves) {
        if (checkAABBCollision({ shelf.min, shelf.max }, pos)) return true;
    }

    if (checkAABBCollision({ cashRegister.min, cashRegister.max }, pos)) return true;

    return false;
}