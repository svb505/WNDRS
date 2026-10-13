#pragma once
#include <windows.h>
#include "glad/glad.h"
#include <GLFW/glfw3.h>
#include "shells.h"
#include "models.h"

OBJModel shellModel;

void setupShellModel() {
    shellModel.LoadOBJ("models/tank_shell.obj",3.0f);
    shellModel.CreateVBO();
}
void drawShell(float yaw, float pitch) {
    shellModel.Draw({0.0f,0.0f,0.0f},yaw,pitch);
};
void drawBullet() {
    glPointSize(1.0f); 
    glColor3f(255.0f / 255.0f, 128.0f / 255.0f, 0.0f);
    glBegin(GL_POINTS);
    glVertex3f(0.0f, 0.0f, 0.0f);
    glEnd();
};
