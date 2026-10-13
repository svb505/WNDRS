#pragma once
#include <cstdint>
#include "svbmath.h"


struct Bounds {
    svbmath::Vec3 min;
    svbmath::Vec3 max;
};
struct checkCol {
    bool checked;
    uint32_t id;
};

Bounds MakeAABB(svbmath::Vec3 center, float width, float height, float depth);
bool RayIntersectsAABB(const svbmath::Vec3& rayOrigin, const svbmath::Vec3& rayDir,
    const Bounds& b, float& tNear, float& tFar);
bool checkAABBCollision(const Bounds& target, svbmath::Vec3& pos);
