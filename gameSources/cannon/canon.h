#pragma once
#include <windows.h>
#include <GL/gl.h>
#include <GLFW/glfw3.h>
#include <cmath>

class Cannon {
public:
    // ===== Параметры пушки =====
    float baseWidth = 2.0f;   // ширина корпуса
    float baseHeight = 1.0f;   // высота корпуса
    float baseDepth = 3.0f;   // глубина корпуса

    float barrelRadius = 0.2f; // радиус ствола
    float barrelLength = 3.0f; // длина ствола
    float barrelOffsetY = 0.5f; // сдвиг ствола вверх от основания
    float barrelOffsetZ = 1.0f; // сдвиг ствола вперёд перед наклоном

    float cannonYaw = 180.0f;
    float cannonPitch = 20.0f;
    float reloadTime = 3.0f;
    float reload = 0.0f;

    void drawBox(float w, float h, float d) {

        float x = w / 2;
        float y = h / 2;
        float z = d / 2;

        glBegin(GL_QUADS);

        glNormal3f(0, 0, 1);
        glVertex3f(-x, -y, z); glVertex3f(x, -y, z); glVertex3f(x, y, z); glVertex3f(-x, y, z);

        glNormal3f(0, 0, -1);
        glVertex3f(-x, -y, -z); glVertex3f(-x, y, -z); glVertex3f(x, y, -z); glVertex3f(x, -y, -z);

        glNormal3f(-1, 0, 0);
        glVertex3f(-x, -y, -z); glVertex3f(-x, -y, z); glVertex3f(-x, y, z); glVertex3f(-x, y, -z);

        glNormal3f(1, 0, 0);
        glVertex3f(x, -y, -z); glVertex3f(x, y, -z); glVertex3f(x, y, z); glVertex3f(x, -y, z);

        glNormal3f(0, 1, 0);
        glVertex3f(-x, y, -z); glVertex3f(-x, y, z); glVertex3f(x, y, z); glVertex3f(x, y, -z);

        glNormal3f(0, -1, 0);
        glVertex3f(-x, -y, -z); glVertex3f(x, -y, -z); glVertex3f(x, -y, z); glVertex3f(-x, -y, z);

        glEnd();
    }
    void drawCylinder(float radius, float length, int slices){
        glBegin(GL_QUAD_STRIP);

        for (int i = 0; i <= slices; i++){
            float a = 2.0f * 3.1415926f * i / slices;

            float x = cos(a);
            float y = sin(a);

            glNormal3f(x, y, 0);

            glVertex3f(x * radius, y * radius, 0);
            glVertex3f(x * radius, y * radius, length);
        }

        glEnd();
    }
    void drawCannon(){
        // ===== Рисуем основание =====
        glPushMatrix();
        glColor3f(0.4f, 0.4f, 0.4f);
        drawBox(baseWidth, baseHeight, baseDepth);
        glPopMatrix();

        // ===== Рисуем ствол =====
        glPushMatrix();

        // Перемещение на верх корпуса
        glTranslatef(0.0f, barrelOffsetY, 0.0f);

        // Поворот вокруг вертикальной оси (yaw)
        glRotatef(cannonYaw, 0.0f, 1.0f, 0.0f);

        // Сдвиг вперёд перед наклоном
        glTranslatef(0.0f, 0.0f, barrelOffsetZ);

        // Наклон вверх/вниз (pitch)
        glRotatef(-cannonPitch, 1.0f, 0.0f, 0.0f);

        // Цвет ствола (можно менять динамически)
        float r = (cannonYaw + 180.0f) / 360.0f;
        float g = (cannonPitch + 45.0f) / 90.0f;
        float b = 0.5f;
        glColor3f(r, g, b);

        // Рисуем цилиндр ствола
        drawCylinder(barrelRadius, barrelLength, 32);

        glPopMatrix();
    }
    void drawTrajectory(float startX, float startY, float startZ,float yaw, float pitch,
        float speed, float gravity){
        float yawRad = yaw * 3.1415926f / 180.0f;
        float pitchRad = pitch * 3.1415926f / 180.0f;

        float vx = cos(pitchRad) * sin(yawRad) * speed;
        float vy = (sin(pitchRad) * speed);
        float vz = cos(pitchRad) * cos(yawRad) * speed;

        glColor3f(1, 0, 0);

        glBegin(GL_LINE_STRIP);

        float timeStep = 0.05f;

        for (float t = 0; t < 5.0f; t += timeStep){
            float x = startX + vx * t;
            float y = startY + vy * t - 0.5f * gravity * t * t;
            float z = startZ + vz * t + 5.0f;

            if (y < 0.0f) break; 

            glVertex3f(x, y, z);
        }

        glEnd();
    }
};



