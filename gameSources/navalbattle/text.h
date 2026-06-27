#pragma once
#include <windows.h>
#include <GL/gl.h>

extern GLuint fontBase;
void InitFont();
void drawText(float x, float y, const std::string& text);