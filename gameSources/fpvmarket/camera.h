#pragma once
#include "svbmath.h"
#include <cmath>

struct CameraParams {
    float baseFov = 70.0f;
    float fov = baseFov;
    float aspect = 1600.0f / 1000.0f;
    float nearPlane = 0.1f;
    float farPlane = 300.0f;

    float top = tan(fov * 3.1415926f / 360.0f) * nearPlane;
    float bottom = -top;
    float right = top * aspect;
    float left = -right;
    float angle = 0.0f;

    float camDistance = 6.0f;
    float camHeight = 3.5f;

    float cameraYaw = -190.0f;
    float cameraPitch = 0.0f;

    bool zoomed = false;
};

class Camera {
private:
    CameraParams camParams;

    svbmath::Vec3 cameraPos = { 0.0f, 1.6f, 5.0f };
    svbmath::Vec3 oldCameraPos = { 0.0f,1.0f,10.0f };
    svbmath::Vec3 cameraForward = {};
public:
    CameraParams& getCamParams();

    svbmath::Vec3& getCamForward();
    svbmath::Vec3& getCamPos();
    svbmath::Vec3& getOldCamPos();

    void setupCamera();
    svbmath::Vec3 returnForwardVector();
};