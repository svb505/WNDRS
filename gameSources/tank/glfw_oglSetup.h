#define NOMINMAX
#include <windows.h>
#include "glad/glad.h"
#include <GLFW/glfw3.h>
#include "texture.h"

void setMatrix(float left, float right, float bottom, float top, float nearP, float farP) {
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glFrustum(left, right, bottom, top, nearP, farP);

    glMatrixMode(GL_MODELVIEW);
}