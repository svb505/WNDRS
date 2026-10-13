#include "actions.h"
#include "svbmath.h"
#include <cmath>
#include <iostream>
#include "building.h"

bool getCashRegisterLookPoint(const svbmath::Vec3& cameraPos,const svbmath::Vec3& cameraForward,
    const CashRegister& cash,svbmath::Vec3& hitPoint){
    const float topY = cash.position.y + cash.height / 2.0f;

    if (std::fabs(cameraForward.y) < 0.0001f)
        return false;

    const float t = (topY - cameraPos.y) / cameraForward.y;

    if (t <= 0.0f)
        return false;

    const svbmath::Vec3 p = cameraPos + cameraForward * t;

    const float minX = cash.position.x - cash.width / 2.0f;
    const float maxX = cash.position.x + cash.width / 2.0f;
    const float minZ = cash.position.z - cash.depth / 2.0f;
    const float maxZ = cash.position.z + cash.depth / 2.0f;

    if (p.x < minX || p.x > maxX ||
        p.z < minZ || p.z > maxZ)
        return false;

    hitPoint = p;
    return true;
}

bool canInteract(svbmath::Vec3 cameraPos,svbmath::Vec3 cameraForward,svbmath::Vec3 objectPos,
    float radius){
    svbmath::Vec3 diff = objectPos - cameraPos;

    if (svbmath::Dot(diff, diff) > radius * radius) return false;

    svbmath::Vec3 direction = svbmath::Normalize(diff);

    float dot = svbmath::Dot(cameraForward, direction);

    // 60 degres
    if (dot < 0.5f) return false;

    return true;
}

bool getLookPointOnHeight(const svbmath::Vec3& cameraPos,const svbmath::Vec3& cameraForward,
    float height,svbmath::Vec3& hitPoint){

    if (fabs(cameraForward.y) < 0.0001f) return false;

    float t = (height - cameraPos.y) / cameraForward.y;

    if (t < 0.0f) return false;

    hitPoint = cameraPos + cameraForward * t;

    return true;
}