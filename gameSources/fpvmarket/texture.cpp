#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <windows.h>
#include <glad/glad.h>
#include "texture.h"
#include <map>
#include <unordered_map>

std::string texturePath = "res/textures/";
std::string iconPath = "res/icons/";

std::unordered_map<std::string, GLuint> loadedTextures;
std::map<std::string, GLuint> allTextures;

std::unordered_map<std::string, std::string> texturesNamesAndPaths = {
    {"SKY", texturePath + "sky.jpg"},
    {"WALL1", texturePath + "wall1.jpg"},
    {"WALL2", texturePath + "wall2.jpg"},
    {"WOOD", texturePath + "wood.jpg"},
    {"METAL", texturePath + "metal.jpg"},
    {"CEILING", texturePath + "ceiling.jpg"},
    {"FLOOR", texturePath + "floor.jpg"},
    {"BETON", texturePath + "beton.jpg"},
    {"GRASS", texturePath + "grass.jpg"},
    {"ROAD", texturePath + "road.jpg"},
    {"ASPHALT", texturePath + "asphalt.png"},
    {"BOX1", texturePath + "box1.jpg"},
    {"BOX2", texturePath + "box2.jpg"},
    {"HAND", iconPath + "hand.png"}
};

void LoadAllTextures() {
    for (auto t : texturesNamesAndPaths) {
        allTextures[t.first] = LoadTexture(t.second.c_str());
    }
}
GLuint LoadTexture(const char* filename) {
    if (loadedTextures.contains(filename)) return loadedTextures[filename];

    int width = 0;
    int height = 0;
    int channels = 0;

    unsigned char* data = stbi_load(filename, &width, &height, &channels, 3);

    if (!data) {
        return 0;
    }

    GLenum format = GL_RGB;

    if (channels == 1) format = GL_RED;
    else if (channels == 3) format = GL_RGB;
    else if (channels == 4) format = GL_RGBA;
    else {
        stbi_image_free(data);
        return 0;
    }

    GLuint texture = 0;

    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

    glTexImage2D(GL_TEXTURE_2D,0, GL_RGB, width,height, 0,GL_RGB, GL_UNSIGNED_BYTE,data);

    stbi_image_free(data);

    loadedTextures[filename] = texture;

    return texture;
}
