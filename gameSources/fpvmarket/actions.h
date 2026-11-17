#pragma once
#include "svbmath.h"
#include "building.h"

bool getCashRegisterLookPoint(const svbmath::Vec3& cameraPos,const svbmath::Vec3& cameraForward,
    const CashRegister& cash,svbmath::Vec3& hitPoint);
bool canInteract(svbmath::Vec3 cameraPos, svbmath::Vec3 cameraForward, svbmath::Vec3 objectPos,
    float radius);

bool getLookPointOnHeight(const svbmath::Vec3& cameraPos, const svbmath::Vec3& cameraForward,
    float height, svbmath::Vec3& hitPoint);
