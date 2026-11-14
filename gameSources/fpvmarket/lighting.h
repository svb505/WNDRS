#pragma once
#include <map>
#include <glad//glad.h>

struct LightingSettings{
    GLfloat ambient[4];
    GLfloat diffuse[4];
    GLfloat specular[4];
};

extern LightingSettings indoorLight;
extern LightingSettings outdoorDayLight;
extern LightingSettings outdoorNightLight;

void initLighting();
void setLighting(const LightingSettings& light);