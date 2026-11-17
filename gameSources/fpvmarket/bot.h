#pragma once
#include "svbmath.h"
#include "camera.h"
#include "drone.h"
#include "building.h"
#include "sound.h"
#include "model.h"

enum class BotState {
    GoingToShelf,
    GoingToCash,
    Leaving,
    CaughtStealing
};

struct PurchasedItem {
    float basePrice;
    float sellPrice;
};

class Bot {
private:
    svbmath::Vec3 position;
    svbmath::Vec3 shelfApproachTarget;
    svbmath::Vec3 targetShelf;
    svbmath::Vec3 cashTarget;

    std::string droneModel;

    BotState state = BotState::GoingToShelf;

    OBJModel model;
    
    float yaw = 0.0f;
    float speed = 3.5f;

    float walkPhase = 0.0f;   
    float walkBlend = 0.0f; 

    bool carryingDrone = false;

    bool sirenPlaying = false;
    bool active = false;

    float globalPrice = 0.0f;

    bool findDrone(FPVDrone& drone);
    bool takeDrone(FPVDrone& drone);

    void moveTo(const svbmath::Vec3& target,
        float dt,
        Building& building);

public:
    void init(GLFWwindow* win);

    bool checkCollision(const svbmath::Vec3& newPos, Building& building);
    void update(float dt, Camera& cam,FPVDrone& drone, Building& building, Sound& sound, bool moving);

    void draw();

    bool isActive() const;

    float calculateRating(const std::vector<PurchasedItem>& items);
    void spawn(FPVDrone& drone, Building& building);
};