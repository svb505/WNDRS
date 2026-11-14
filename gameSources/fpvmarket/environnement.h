#pragma once
#include <string>
#include <nlohmann//json.hpp>

void drawRoadsFromJson(const nlohmann::json& levelJson);
void drawRoad(float startX, float startZ, float endX, float endZ, float y, float width);
void drawGrid(float camX, float camZ);
void drawGridText(float camX, float camZ);
void drawSky();
void drawGround();

