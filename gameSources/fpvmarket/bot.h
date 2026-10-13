#pragma once
#include "svbmath.h"
#include "camera.h"
#include "drone.h"
#include "building.h"

enum class BotState {
    GoingToShelf,
    GoingToCash,
    Leaving
};

class Bot {
private:
    svbmath::Vec3 position;
    svbmath::Vec3 shelfApproachTarget;
    svbmath::Vec3 targetShelf;
    svbmath::Vec3 cashTarget;

    std::string droneModel;

    BotState state = BotState::GoingToShelf;

    float speed = 3.5f;

    bool carryingDrone = false;

    bool active = false;

private:
    bool findDrone(FPVDrone& drone);
    bool takeDrone(FPVDrone& drone);

    void moveTo(const svbmath::Vec3& target,
        float dt,
        Building& building);

public:

    bool checkCollision(const svbmath::Vec3& newPos, Building& building);
    void update(float dt, FPVDrone& drone, Building& building);

    void draw();

    bool isActive() const;

    void spawn(FPVDrone& drone, Building& building);
};