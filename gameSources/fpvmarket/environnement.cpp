#include <windows.h>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include "environnement.h"
#include <cmath>
#include <string>
#include <format>
#include "text.h"
#include "texture.h"


const float size = 50.0f;

void drawRoadsFromJson(const nlohmann::json& levelJson) {
    if (!levelJson.contains("roads") || !levelJson["roads"].is_array())  return;

    for (const auto& road : levelJson["roads"]) {
        auto start = road["start"];
        auto end = road["end"];

        float startX = start[0].get<float>();
        float startY = start[1].get<float>() + 0.01f;
        float startZ = start[2].get<float>();

        float endX = end[0].get<float>();
        float endY = end[1].get<float>();
        float endZ = end[2].get<float>();

        float width = road.value("width", 6.0f);

        drawRoad(startX, startZ, endX, endZ, startY, width);
    }
}
void drawRoad(float startX, float startZ,float endX, float endZ,float y, float width) {
    GLuint roadTex = allTextures["ROAD"];

    float dx = endX - startX;
    float dz = endZ - startZ;

    float length = sqrt(dx * dx + dz * dz);

    if (length <= 0.001f)
        return;

    float offsetX = -dz / length * (width / 2.0f);
    float offsetZ = dx / length * (width / 2.0f);

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, roadTex);

    glBegin(GL_QUADS);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(startX + offsetX, y, startZ + offsetZ);

    glTexCoord2f(1.0f, length / 10.0f);
    glVertex3f(endX + offsetX, y, endZ + offsetZ);

    glTexCoord2f(0.0f, length / 10.0f);
    glVertex3f(endX - offsetX, y, endZ - offsetZ);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(startX - offsetX, y, startZ - offsetZ);

    glEnd();

    glDisable(GL_TEXTURE_2D);
}
void drawGridText(float camX, float camZ) {
    float baseX = camX;
    float baseZ = camZ;
    float step = 50.0f;

    for (float i = -size / 100; i <= size / 100; i += step) {
        for (float j = -size / 100; j <= size / 100; j += step) {
            float x = baseX + i;
            float z = baseZ + j;

            std::string text = std::format("(X:{:.0f}; Z:{:.0f})", x, -z);
            float y = 1.5f;
            RenderTextWorld(x, y, z, 0.8f, 0.8f, 0.8f, text.c_str());
        }
    }
}
void drawGrid(float camX, float camZ) {
    float baseX = camX;
    float baseZ = camZ;
    float step = 50.0f;

    glColor4f(0.8f, 0.8f, 0.8f, 0.3f);
    glBegin(GL_LINES);

    for (float i = -size; i <= size; i += step) {

        for (float j = -size; j <= size; j += step) {
            float x = baseX + i;
            float z = baseZ + j;

            float y = 0.2f;

            // X lines
            if (j < size) {
                float z2 = baseZ + j + step;
                float y2 = 0.2f;

                glVertex3f(x, y, z);
                glVertex3f(x, y2, z2);
            }

            // Z lines
            if (i < size) {
                float x2 = baseX + i + step;
                float y2 = 0.2f;

                glVertex3f(x, y, z);
                glVertex3f(x2, y2, z);
            }
        }
    }

    glEnd();
}
void drawSky() {
    GLuint skyTex = allTextures["SKY"];

    glDisable(GL_DEPTH_TEST);

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, skyTex);

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    glOrtho(-1, 1, -1, 1, -1, 1);

    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();

    glBegin(GL_QUADS);

    glColor3f(1, 1, 1);

    glTexCoord2f(0, 0); glVertex2f(-1, 1);
    glTexCoord2f(1, 0); glVertex2f(1, 1);
    glTexCoord2f(1, 1); glVertex2f(1, -1);
    glTexCoord2f(0, 1); glVertex2f(-1, -1);

    glEnd();

    glPopMatrix();

    glMatrixMode(GL_PROJECTION);
    glPopMatrix();

    glMatrixMode(GL_MODELVIEW);

    glDisable(GL_TEXTURE_2D);
    glEnable(GL_DEPTH_TEST);
}
void drawGround() {
    GLuint grassTex = allTextures["ASPHALT"];

    float step = 3.0f;

    glColor3f(1.0f, 1.0f, 1.0f);

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, grassTex);

    for (float x = -100.0f; x < 100.0f; x += step) {
        for (float z = -100.0f; z < 100.0f; z += step) {

            float x1 = x;
            float z1 = z;

            float x2 = x + step;
            float z2 = z + step;

            glBegin(GL_QUADS);

            glNormal3f(0, 1, 0);

            glTexCoord2f(0.0f, 0.0f);
            glVertex3f(x1, 0.0f, z1);

            glTexCoord2f(1.0f, 0.0f);
            glVertex3f(x2, 0.0f, z1);

            glTexCoord2f(1.0f, 1.0f);
            glVertex3f(x2, 0.0f, z2);

            glTexCoord2f(0.0f, 1.0f);
            glVertex3f(x1, 0.0f, z2);

            glEnd();
        }
    }

    glDisable(GL_TEXTURE_2D);
}


