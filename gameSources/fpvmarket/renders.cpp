#include "renders.h"
#include "texture.h"
#include <glad/glad.h>
#include "svbmath.h"
#include "variables.h"

void drawPointInCenter() {
    glPushAttrib(GL_ALL_ATTRIB_BITS);

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();

    glOrtho(0, ECRAN_W, ECRAN_H, 0, -1, 1);

    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();

    glDisable(GL_DEPTH_TEST);
    glDisable(GL_TEXTURE_2D);
    glDisable(GL_LIGHTING);

    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    float centerX = ECRAN_W / 2.0f;
    float centerY = ECRAN_H / 2.0f;
    float pointSize = 10.0f;

    glColor4f(1.0f, 1.0f, 1.0f, 1.0f);

    glBegin(GL_QUADS);
    glVertex2f(centerX - pointSize / 2.0f, centerY - pointSize / 2.0f);
    glVertex2f(centerX + pointSize / 2.0f, centerY - pointSize / 2.0f);
    glVertex2f(centerX + pointSize / 2.0f, centerY + pointSize / 2.0f);
    glVertex2f(centerX - pointSize / 2.0f, centerY + pointSize / 2.0f);
    glEnd();

    glMatrixMode(GL_MODELVIEW);
    glPopMatrix();

    glMatrixMode(GL_PROJECTION);
    glPopMatrix();

    glPopAttrib();
}
void render2DIcon(std::string iconName, svbmath::Vec2 pos, float size) {
    glDisable(GL_DEPTH_TEST);

    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();

    glOrtho(0, ECRAN_W, ECRAN_H, 0, -1, 1);

    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();

    GLuint icon = allTextures[iconName];

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, icon);

    glColor4f(1.0f, 1.0f, 1.0f, 1.0f);

    glBegin(GL_QUADS);

    glTexCoord2f(0, 0);
    glVertex2f(pos.x, pos.y);

    glTexCoord2f(1, 0);
    glVertex2f(pos.x + size, pos.y);

    glTexCoord2f(1, 1);
    glVertex2f(pos.x + size, pos.y + size);

    glTexCoord2f(0, 1);
    glVertex2f(pos.x, pos.y + size);

    glEnd();

    glDisable(GL_TEXTURE_2D);

    glMatrixMode(GL_MODELVIEW);
    glPopMatrix();

    glMatrixMode(GL_PROJECTION);
    glPopMatrix();

    glDisable(GL_BLEND);

    glEnable(GL_DEPTH_TEST);
}
void drawQuad(float width, float height, float depth, svbmath::Vec3 pos) {
    width /= 2.0f;
    height /= 2.0f;
    depth /= 2.0f;

    glPushMatrix();
    glTranslatef(pos.x, pos.y, pos.z);

    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUADS);

    // Front (+Z)
    glNormal3f(0, 0, 1);
    glVertex3f(-width, -height, depth);
    glVertex3f(width, -height, depth);
    glVertex3f(width, height, depth);
    glVertex3f(-width, height, depth);

    // Back (-Z)
    glNormal3f(0, 0, -1);
    glVertex3f(width, -height, -depth);
    glVertex3f(-width, -height, -depth);
    glVertex3f(-width, height, -depth);
    glVertex3f(width, height, -depth);

    // Left (-X)
    glNormal3f(-1, 0, 0);
    glVertex3f(-width, -height, -depth);
    glVertex3f(-width, -height, depth);
    glVertex3f(-width, height, depth);
    glVertex3f(-width, height, -depth);

    // Right (+X)
    glNormal3f(1, 0, 0);
    glVertex3f(width, -height, depth);
    glVertex3f(width, -height, -depth);
    glVertex3f(width, height, -depth);
    glVertex3f(width, height, depth);

    // Top
    glNormal3f(0, 1, 0);
    glVertex3f(-width, height, depth);
    glVertex3f(width, height, depth);
    glVertex3f(width, height, -depth);
    glVertex3f(-width, height, -depth);

    // Bottom
    glNormal3f(0, -1, 0);
    glVertex3f(-width, -height, -depth);
    glVertex3f(width, -height, -depth);
    glVertex3f(width, -height, depth);
    glVertex3f(-width, -height, depth);

    glEnd();

    glPopMatrix();
}
void drawBox(float width, float height, float depth, svbmath::Vec3 pos, GLuint texture) { 
    width /= 2.0f;
    height /= 2.0f;
    depth /= 2.0f;

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, texture);

    glPushMatrix();
    glTranslatef(pos.x, pos.y, pos.z);

    glBegin(GL_QUADS);

    // Front (+Z)
    glNormal3f(0, 0, 1);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(-width, -height, depth);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(width, -height, depth);

    glTexCoord2f(1.0f, 1.0f);
    glVertex3f(width, height, depth);

    glTexCoord2f(0.0f, 1.0f);
    glVertex3f(-width, height, depth);


    // Back (-Z)
    glNormal3f(0, 0, -1);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(width, -height, -depth);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(-width, -height, -depth);

    glTexCoord2f(1.0f, 1.0f);
    glVertex3f(-width, height, -depth);

    glTexCoord2f(0.0f, 1.0f);
    glVertex3f(width, height, -depth);


    // Left (-X)
    glNormal3f(-1, 0, 0);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(-width, -height, -depth);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(-width, -height, depth);

    glTexCoord2f(1.0f, 1.0f);
    glVertex3f(-width, height, depth);

    glTexCoord2f(0.0f, 1.0f);
    glVertex3f(-width, height, -depth);


    // Right (+X)
    glNormal3f(1, 0, 0);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(width, -height, depth);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(width, -height, -depth);

    glTexCoord2f(1.0f, 1.0f);
    glVertex3f(width, height, -depth);

    glTexCoord2f(0.0f, 1.0f);
    glVertex3f(width, height, depth);


    // Top
    glNormal3f(0, 1, 0);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(-width, height, depth);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(width, height, depth);

    glTexCoord2f(1.0f, 1.0f);
    glVertex3f(width, height, -depth);

    glTexCoord2f(0.0f, 1.0f);
    glVertex3f(-width, height, -depth);


    // Bottom
    glNormal3f(0, -1, 0);

    glTexCoord2f(0.0f, 0.0f);
    glVertex3f(-width, -height, -depth);

    glTexCoord2f(1.0f, 0.0f);
    glVertex3f(width, -height, -depth);

    glTexCoord2f(1.0f, 1.0f);
    glVertex3f(width, -height, depth);

    glTexCoord2f(0.0f, 1.0f);
    glVertex3f(-width, -height, depth);

    glEnd();

    glPopMatrix();

    glBindTexture(GL_TEXTURE_2D, 0);
    glDisable(GL_TEXTURE_2D);
}