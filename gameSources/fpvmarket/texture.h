#pragma once
#include <windows.h>
#include <glad/glad.h>
#include <string>
#include <map>
#include <unordered_map>

extern std::string texturePath;
extern std::string iconPath;
extern std::string prevPath;

extern std::map<std::string, GLuint> allTextures;
extern std::unordered_map<std::string, GLuint> loadedTextures;
extern std::unordered_map<std::string, std::string> texturesNamesAndPaths;

void LoadAllTextures();
GLuint LoadTexture(const char* filename);
