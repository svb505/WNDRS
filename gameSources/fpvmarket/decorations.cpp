#include "bounds.h"
#include "decorations.h"
#include "model.h"
#include "svbmath.h"
#include "camera.h"
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <map>
#include "logger.h"
#include <format>

std::map<DecType, float> scales = {
    { DecType::BUILD1, 1.0f },
    { DecType::BUILD2, 1.0f },
    { DecType::TREE,  0.25f },
    { DecType::LAMP,  1.25f },
    { DecType::STREET,  0.7f }
};


static float getModelScale(DecType type) {
    auto it = scales.find(type);

    if (it == scales.end()) return 1.0f;

    return it->second;
}
void Decorations::addDecoration(DecType type, svbmath::Vec3 pos, float rotationY) {
    DecorationInstance decoration;

    decoration.type = type;
    decoration.position = pos;
    decoration.rotationY = rotationY;

    decorations.push_back(decoration);
}
void Decorations::initPositions() {
    decorations.clear();

    //addBuildings();
    //addEndBuildings();
    addDecoration(DecType::STREET, { 18.0f, 0.001f, 5.0f }, 0.0f);
    addDecoration(DecType::STREET, { -120.0f, 0.001f, 5.0f }, 0.0f);
    addTrees();
    addLamps();
}
void Decorations::addBuildings() {
    for (int i = 0; i < buildsCount; ++i) {
        float x;

        if (i < 3) x = buildBasePos.x + buildXStep * (i + 1);
        else x = buildBasePos.x - buildXStep * (i - 2);

        addDecoration(DecType::BUILD2, { x, buildBasePos.y + 2.5f, buildBasePos.z }, 0.0f);
    }

    for (int i = 0; i < buildsCount; ++i) {
        float x;

        if (i < 3) x = buildBasePos.x + buildXStep * (i + 1);
        else if (i == 3)  x = -10.0f;
        else x = buildBasePos.x - buildXStep * (i - 2);

        addDecoration(DecType::BUILD2, { x, buildBasePos.y + 2.5f,35.0f }, 0.0f);
    }
}
void Decorations::addEndBuildings() {
    addDecoration(DecType::BUILD2, { -35.0f, buildBasePos.y + 2.5f,10.0f }, 0.0f);
    addDecoration(DecType::BUILD2, { 80.0f, buildBasePos.y + 2.5f,10.0f }, 0.0f);
}
void Decorations::addTrees() {
    for (int i = 0; i < treesCount; ++i) {
        float x;

        if (i < 3) x = buildBasePos.x + buildXStep * (i + 1);
        else x = buildBasePos.x - buildXStep * (i - 2);

        addDecoration(DecType::TREE, { x,buildBasePos.y, 16.0f }, 0.0f);
    }
}
void Decorations::addLamps() {
    for (int i = 0; i < lampsCount; ++i) {
        float x;

        if (i < 3) x = buildBasePos.x + buildXStep * (i + 1);
        else x = buildBasePos.x - buildXStep * (i - 2);

        addDecoration(DecType::LAMP, { x,buildBasePos.y,6.5f }, 0.0f);
    }
}
void Decorations::initDecoration(const std::string& modelPath, DecType decType,
    const std::string& texturePath) {

    float scale = getModelScale(decType);

    auto model = std::make_unique<OBJModel>();

    if (!model->LoadOBJ(modelPath, scale)) {
        LOG_ERROR(std::format("Failed to load decoration model: {}", modelPath));

        return;
    }

    if (!texturePath.empty())  model->LoadTexture(texturePath);

    model->CreateVBO();

    models[decType] = std::move(model);
}
void Decorations::drawAllDecorations(DecType decType) {
    auto modelIt = models.find(decType);

    if (modelIt == models.end()) return;

    OBJModel* model = modelIt->second.get();

    if (!model) return;

    glEnable(GL_CULL_FACE);
    glCullFace(GL_BACK);
    glFrontFace(GL_CCW);


    for (const DecorationInstance& decoration : decorations) {
        if (decoration.type != decType) continue;

        model->Draw(decoration.position, decoration.rotationY, 0.0f);
    }


    glDisable(GL_CULL_FACE);
}

static Bounds transformBounds(const Bounds& local, float scale,
    const DecorationInstance& decoration) {
    Bounds worldBounds = local;

    const svbmath::Vec3& position = decoration.position;
    float rotation = decoration.rotationY;

    while (rotation < 0.0f) rotation += 360.0f;
    while (rotation >= 360.0f) rotation -= 360.0f;


    if (rotation == 90.0f) {
        worldBounds.min.x = -local.max.z * scale + position.x;
        worldBounds.max.x = -local.min.z * scale + position.x;

        worldBounds.min.z = local.min.x * scale + position.z;
        worldBounds.max.z = local.max.x * scale + position.z;
    }
    else {
        worldBounds.min.x = local.min.x * scale + position.x;
        worldBounds.max.x = local.max.x * scale + position.x;

        worldBounds.min.z = local.min.z * scale + position.z;
        worldBounds.max.z = local.max.z * scale + position.z;
    }

    worldBounds.min.y = local.min.y * scale + position.y;
    worldBounds.max.y = local.max.y * scale + position.y;

    return worldBounds;
}

// Какие части модели твёрдые. Всё, что здесь вернёт false, не блокирует игрока.
// rue_sol - пол улицы; magasin_* - интерьер магазина, чтобы можно было зайти внутрь
// (magasin_etages_toit начинается выше роста игрока, поэтому оставлен твёрдым).
static bool isSolidPart(const std::string& name) {
    if (name == "rue_sol") return false;

    if (name.rfind("magasin_", 0) == 0 && name != "magasin_etages_toit")
        return false;

    return true;
}

Bounds Decorations::getWorldBounds(const OBJModel& model, const DecorationInstance& decoration) {
    return transformBounds(model.bounds, model.scale, decoration);
}
bool Decorations::checkCollision(Camera& cam, DecType decType) {
    auto modelIt = models.find(decType);

    if (modelIt == models.end()) return false;

    OBJModel* model = modelIt->second.get();

    if (!model) return false;

    for (const DecorationInstance& decoration : decorations) {
        if (decoration.type != decType)continue;

        // Модель без объектов ("o") - как раньше, одна общая коробка.
        if (model->parts.empty()) {
            if (checkAABBCollision(getWorldBounds(*model, decoration), cam.getCamPos()))
                return true;

            continue;
        }

        // Иначе проверяем каждое здание отдельно - проходы между ними свободны.
        for (const ObjPart& part : model->parts) {
            if (!isSolidPart(part.name)) continue;

            Bounds worldBounds = transformBounds(part.bounds, model->scale, decoration);

            if (checkAABBCollision(worldBounds, cam.getCamPos())) return true;
        }
    }

    return false;
}

