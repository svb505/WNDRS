#pragma once
#include "svbmath.h"
#include <glad/glad.h>
#include <string>

void drawQuad(float width, float height, float depth, svbmath::Vec3 pos);
void render2DIcon(std::string iconName, svbmath::Vec2 pos, float size);
void drawBox(float width, float height, float depth, svbmath::Vec3 pos, GLuint texture);
void drawPointInCenter();
