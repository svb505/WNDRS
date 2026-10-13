#include <string>
#include <nlohmann//json.hpp>

using json = nlohmann::json;

std::string objName = "";
int ECRAN_W = 1400;
int ECRAN_H = 900;
float sensitivity = 0.05f;
float myBalance = 3000.0f;
bool hideCursor = true;
bool canTakeObj = false;
bool canDrawEquipModel = false;
bool placeObj = false;
bool canCreateDrone = false;
float priceForT1 = 0.0f;
float priceForT2 = 0.0f;
float priceForController1 = 0.0f;
float priceForGoggles1 = 0.0f;
float priceForController2 = 0.0f;
float priceForGoggles2 = 0.0f;
bool isOpen = false;
std::string currLang = "FR";
json lang;