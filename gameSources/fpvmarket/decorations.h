
#pragma once

#include "svbmath.h"
#include <vector>
#include "model.h"
#include "camera.h"
#include <map>
#include <memory>
#include <string>

enum class DecType {
    BUILD1,
    BUILD2,
    TREE,
    LAMP,
    STREET,
    FENCE,
    FLOWER_BED,
    BENCH,
    TRASH_BIN
};

struct DecorationInstance {
    int id = 0;
    DecType type;
    svbmath::Vec3 position;
    float rotationY = 0.0f;
};

extern std::map<DecType, float> scales;

class Decorations {
private:
    std::vector<DecorationInstance> decorations;

    std::map<DecType, std::unique_ptr<OBJModel>> models;

    DecType stringToDecType(const std::string& type);

public:
    const std::vector<DecorationInstance>& GetInstances() const;

    const std::map<DecType, std::unique_ptr<OBJModel>>& GetModels() const;

    void addDecoration(DecType type, svbmath::Vec3 pos, float rotationY);

    void initPositions(const std::string& jsonPath);

    void initDecoration(
        const std::string& modelPath,
        DecType decType,
        const std::string& texturePath
    );

    void drawAllDecorations(DecType decType);

    Bounds getWorldBounds(
        const OBJModel& model,
        const DecorationInstance& decoration
    );

    bool checkCollision(Camera& cam);
};
