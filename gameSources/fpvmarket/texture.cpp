#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <windows.h>
#include <glad/glad.h>
#include "texture.h"
#include <map>
#include <unordered_map>
#include <format>
#include "logger.h"

std::string texturePath = "res/textures/";
std::string iconPath = "res/icons/";
std::string prevPath = "res/previews/";

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
    {"HAND", iconPath + "hand.png"},
    {"CARD", iconPath + "card.png"},
    {"FRM1", prevPath + "fr1.jpg"},
    {"FRM2", prevPath + "fr2.jpg"},
    {"CAM1", prevPath + "cam1.jpg"},
    {"CAM2", prevPath + "cam2.jpg"},
    {"CAM3", prevPath + "cam3.jpg"},
    {"BAT1", prevPath + "bat1.jpg"},
    {"BAT2", prevPath + "bat2.jpg"},
    {"BAT3", prevPath + "bat3.jpg"},
    {"MOT1", prevPath + "mot1.jpg"},
    {"MOT2", prevPath + "mot2.jpg"},
    {"MOT3", prevPath + "mot3.jpg"},
    {"PRP1", prevPath + "prop1.jpg"},
    {"PRP2", prevPath + "prop2.jpg"},
    {"PRP3", prevPath + "prop3.jpg"},
    {"CTRL1",prevPath + "cntrlr1.jpg"},
    {"CTRL2",prevPath + "cntrlr2.jpg"},
     {"GGLS1",prevPath + "g1.jpg"},
    {"GGLS2",prevPath + "g2.jpg"},
     {"FC1",prevPath + "fc1.jpg"},
    {"FC2",prevPath + "fc2.jpg"},

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
        LOG_ERROR(std::format("Cannot load texture: {}",filename));
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
