#define NOMINMAX
#include "windows.h"
#include "camera.h"
#include <GL/glu.h>

svbmath::Vec3& Camera::getCamForward() {
    return cameraForward;
}
svbmath::Vec3& Camera::getCamPos() {
    return cameraPos;
}
svbmath::Vec3& Camera::getOldCamPos() {
    return oldCameraPos;
}
CameraParams& Camera::getCamParams() {
    return camParams;
}
void Camera::setupCamera() {
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Ограничение pitch
    if (camParams.cameraPitch > 89.0f) camParams.cameraPitch = 89.0f;
    if (camParams.cameraPitch < -89.0f) camParams.cameraPitch = -10.0f;
    if (cameraPos.y < 0.0f) cameraPos.y = 0.0f;

    float yawRad = camParams.cameraYaw * 3.1415926f / 180.0f;
    float pitchRad = camParams.cameraPitch * 3.1415926f / 180.0f;

    cameraForward = { cos(pitchRad) * sin(yawRad), sin(pitchRad), cos(pitchRad) * cos(yawRad) };

    gluLookAt(cameraPos.x, cameraPos.y, cameraPos.z, cameraPos.x + cameraForward.x, 
        cameraPos.y + cameraForward.y, cameraPos.z + cameraForward.z, 0, 1, 0);
    
}
svbmath::Vec3 Camera::returnForwardVector() {
    float radYaw = camParams.cameraYaw * 3.14159265f / 180.0f;
    float radPitch = camParams.angle * 3.14159265f / 180.0f;
    float fx = cos(radPitch) * sin(radYaw);
    float fy = sin(radPitch);
    float fz = -cos(radPitch) * cos(radYaw);

    return { fx,fy,fz };
}
