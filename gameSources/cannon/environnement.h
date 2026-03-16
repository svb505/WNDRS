#pragma once
#include <windows.h>
#include <GL/gl.h>
#include <GLFW/glfw3.h>
#include "camera.h"
#include "text.h"

const float size = 100.0f;

void drawGridText(float camX, float camZ) {
    float baseX = floor(camX / size) * size;
    float baseZ = floor(camZ / size) * size;
    float step = 10.0f;

    for (float i = -size / 2; i <= size / 2; i += step){
        for (float j = -size / 2; j <= size / 2; j += step){
            float x = baseX + i;
            float z = baseZ + j;

            std::string text = std::format("({},{})", x, -z);
            RenderTextWorld(x,1.5f,z,1.0f, 1.0f, 1.0f,text.c_str());
        }
    }
}
void drawGrid(float camX, float camZ) {
    float baseX = floor(camX / size) * size;
    float baseZ = floor(camZ / size) * size;
    float step = 20.0f;

    glColor4f(1.0f, 1.0f, 1.0f,0.1f);
    glBegin(GL_LINES);

    for (float i = -size; i <= size; i += step) {
        glVertex3f(baseX + i, 0.2f, baseZ - size);
        glVertex3f(baseX + i, 0.2f, baseZ + size);

        glVertex3f(baseX - size, 0.2f, baseZ + i);
        glVertex3f(baseX + size, 0.2f, baseZ + i);
    }

    glEnd();
}
void drawSky(){
    glDisable(GL_DEPTH_TEST);

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    glOrtho(-1, 1, -1, 1, -1, 1);

    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();

    glBegin(GL_QUADS);
    glColor3f(51.0f / 255, 151.0f / 255, 255.0f / 255);
    glVertex2f(-1, 1);
    glVertex2f(1, 1);

    glColor3f(51.0f / 255, 151.0f / 255, 255.0f / 255);
    glVertex2f(1, -1);
    glVertex2f(-1, -1);
    glEnd();

    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);

    glEnable(GL_DEPTH_TEST);
}
void drawGround(float camX, float camZ){
    float x = floor(camX / size) * size;
    float z = floor(camZ / size) * size;

    glColor3f(0.0f, 102.0f / 255, 0.0f);
    glBegin(GL_QUADS);
    glNormal3f(0.0f, 1.0f, 0.0f);
    glVertex3f(x - size, 0.0f, z - size);
    glVertex3f(x + size, 0.0f, z - size);
    glVertex3f(x + size, 0.0f, z + size);
    glVertex3f(x - size, 0.0f, z + size);
    glEnd();
}


