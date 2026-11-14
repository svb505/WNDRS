#pragma once
#define GLFW_INCLUDE_NONE
#include <GLFW/glfw3.h>
#include <glad/glad.h>
#include <cmath>
#include <vector>
#include <map>
#include <string>
#include "svbmath.h"
#include "building.h"
#include "model.h"
#include "jsonParcer.h"
#include <memory>
#include "variables.h"

struct ShelfSetting {
    svbmath::Vec3 pos;
    bool busy = false;
};
struct Package {
    std::vector<std::string> equip;
    svbmath::Vec3 pos;

    GLuint texture;

    int currentIndex = 0;
    bool render = false;
};
struct PlacedObject {
    std::string name;
    svbmath::Vec3 pos;
};
struct Components {
    int frame = 0, camera = 0, battery = 0, motor = 0, propeller = 0, controller = 0, goggles = 0, fc = 0;
};

struct ModelPaths {
    std::string model, texture;
    float scale;
};

enum class CompType{
    TYPE1,
    TYPE2,
    TYPE3
};

class FPVDrone {
private:
    Components comp;
    std::string name = getStringFromJson("DRONE_Achetee");

    OBJModel fpv;

    std::vector<std::string> baseEquipment = { lang[currLang]["FRAME1"].get<std::string>(),
        lang[currLang]["CAM1"].get<std::string>(),
        lang[currLang]["BAT450"].get<std::string>(), lang[currLang]["MTR1"].get<std::string>(),
        lang[currLang]["PROP1"].get<std::string>(),lang[currLang]["CNTRL1"].get<std::string>(), lang[currLang]["GGLS1"].get<std::string>(),
        name,
        lang[currLang]["BAT550"].get<std::string>(),
        lang[currLang]["BAT500"].get<std::string>(),
        lang[currLang]["PROP2"].get<std::string>(), lang[currLang]["PROP3"].get<std::string>(),lang[currLang]["FC1"].get<std::string>(),
        lang[currLang]["FC2"].get<std::string>(),
        lang[currLang]["CNTRL2"].get<std::string>(),lang[currLang]["GGLS2"].get<std::string>(),
        lang[currLang]["FRAME2"].get<std::string>(),
        lang[currLang]["MTR2"].get<std::string>(), lang[currLang]["MTR3"].get<std::string>(),
        lang[currLang]["CAM2"].get<std::string>(), lang[currLang]["CAM3"].get<std::string>() };

    std::map<std::string, float> equipmentPrice = { {baseEquipment[0],100.0f},{baseEquipment[1],300.0f},
        {baseEquipment[2],250.0f} ,{baseEquipment[3],350.0f} ,{baseEquipment[4],150.0f},
        {baseEquipment[5],100.0f},
        {baseEquipment[6],250.0f},{name,1000.0f} ,{baseEquipment[10],120.0f},{baseEquipment[11],120.0f},
        {baseEquipment[8],450.0f} ,{baseEquipment[9],350.0f} ,{baseEquipment[12],150.0f}, {baseEquipment[13],100.0f},
        {baseEquipment[15],270.0f},{baseEquipment[14],90.0f},{baseEquipment[16],130.0f},{baseEquipment[17],400.0f},
        {baseEquipment[18],320.0f},{baseEquipment[19],270.0f},{baseEquipment[20],330.0f} };

    std::map<std::string, std::unique_ptr<OBJModel>> allCompModels;
    std::map<std::string, ModelPaths> allCompPaths = {
     {baseEquipment[0], {
         "res/models/fpv_frame/fpv_frame.obj",
         "res/models/fpv_frame/fpv_frame_carbon.png",
         5.0f
     }},
    {baseEquipment[1], {
         "res/models/fpv_cam/fpv_camera.obj",
         "res/models/fpv_cam/fpv_camera_texture.png",
         5.0f
     }},
        {baseEquipment[19], {
         "res/models/fpv_cam2/fpv_camera.obj",
         "res/models/fpv_cam2/tex.jpg",
         0.004f
     }},
        {baseEquipment[20], {
         "res/models/fpv_cam3/fpv_camera.obj",
         "res/models/fpv_cam3/tex.jpg",
         0.004f
     }},
        {baseEquipment[10], {
         "res/models/fpv_propeller2/prop_bi_5048.obj",
         "res/models/fpv_propeller2/tex.jpg",
         5.0f
     }},
        {baseEquipment[11], {
         "res/models/fpv_propeller3/prop_tri_5143.obj",
         "res/models/fpv_propeller3/tex.jpg",
         5.0f
     }},
        {baseEquipment[8], {
         "res/models/fpv_bat2/fpv_battery.obj",
         "res/models/fpv_bat2/tex.jpg",
         5.0f
     }},
     {baseEquipment[9], {
         "res/models/fpv_bat3/fpv_battery.obj",
         "res/models/fpv_bat3/tex.jpg",
         5.0f
     }},
        {baseEquipment[12], {
         "res/models/fpv_FC1/fc_20x20_mini.obj",
         "res/models/fpv_FC1/tex.jpg",
         0.004f
     }},
     {baseEquipment[13], {
         "res/models/fpv_FC2/fc_30x30_f4.obj",
         "res/models/fpv_FC2/tex.jpg",
          0.004f
     }},
        {baseEquipment[14], {
         "res/models/fpv_controller2/fpv_radio.obj",
         "res/models/fpv_controller2/tex.jpg",
        0.005f
     }},
     {baseEquipment[15], {
         "res/models/fpv_goggles2/fpv_goggles.obj",
         "res/models/fpv_goggles2/tex.jpg",
         5.0f
     }},
     {baseEquipment[2], {
         "res/models/fpv_bat/battery.obj",
         "res/models/fpv_bat/battery_texture.png",
         5.0f
     }},
     {baseEquipment[16], {
         "res/models/fpv_frame2/fpv_frame.obj",
         "res/models/fpv_frame2/tex.jpg",
         6.0f
     }},
     {baseEquipment[3], {
         "res/models/fpv_motor/fpv_motor.obj",
         "res/models/fpv_motor/fpv_atlas.png",
         0.07f
     }},
        {baseEquipment[17], {
         "res/models/fpv_motor2/fpv_motor.obj",
         "res/models/fpv_motor2/tex.jpg",
         0.007f
     }},
        {baseEquipment[18], {
         "res/models/fpv_motor3/fpv_motor.obj",
         "res/models/fpv_motor3/tex.jpg",
         0.007f
     }},
     {baseEquipment[4], {
         "res/models/fpv_propeller/fpv_propeller.obj",
         "res/models/fpv_propeller/fpv_atlas.png",
         0.04f
     }},
     {baseEquipment[5], {
         "res/models/fpv_controller/controller.obj",
         "res/models/fpv_controller/controller_texture.png",
         4.0f
     }},
     {baseEquipment[6], {
         "res/models/fpv_goggles/fpv_goggles.obj",
         "res/models/fpv_goggles/fpv_goggles_texture.png",
         5.0f
     }}
    };
    std::map<CompType, std::vector<std::string>> equipTypes = { {CompType::TYPE1,
        {name,lang[currLang]["FRAME1"].get<std::string>(),
        lang[currLang]["CAM1"].get<std::string>(),
        lang[currLang]["BAT450"].get<std::string>(), lang[currLang]["MTR1"].get<std::string>(),
        lang[currLang]["PROP1"].get<std::string>(),lang[currLang]["CNTRL1"].get<std::string>(),
        lang[currLang]["GGLS1"].get<std::string>(),lang[currLang]["FC1"].get<std::string>()}},
        { CompType::TYPE2,{lang[currLang]["BAT550"].get<std::string>(),lang[currLang]["PROP2"].get<std::string>(),
        lang[currLang]["FC2"].get<std::string>(),lang[currLang]["CNTRL2"].get<std::string>(),
        lang[currLang]["GGLS2"].get<std::string>(),lang[currLang]["FRAME2"].get<std::string>(),
        lang[currLang]["MTR2"].get<std::string>(),lang[currLang]["CAM2"].get<std::string>()}},
        { CompType::TYPE3,{lang[currLang]["BAT500"].get<std::string>(),
         lang[currLang]["PROP3"].get<std::string>(),lang[currLang]["MTR3"].get<std::string>(),
        lang[currLang]["CAM3"].get<std::string>()}
    } };
    

    std::vector<Package> boxesWithEquip = {};
    std::vector<PlacedObject> placedObjects;
    std::vector<ShelfSetting> positionsOnShelves;

    OBJModel markerModel;

    float deliveryTime = 10.0; //sec
    float textTime = 3.0f;

    bool showText = false;
    bool inDelivery = false;
public:
    void init(GLFWwindow* win);
    void consumeComponents();
    void reloadCompModels();

    GLuint returnCompPreview(const std::string& key);
    Components& getComp();
    bool getShowText();
    std::vector<Package>& getOrderEquip();
    std::vector<PlacedObject>& getPlacedEquip();
    const std::vector<std::string>& getBaseEquip();
    const std::map<std::string, float>& getEquipPrice();
    bool isPlaced(const std::string& name) const;
    std::vector<svbmath::Vec3> generateShelfPoints(const Shelf& shelf);
    std::vector<ShelfSetting>& getShelfPositions();
    std::map<CompType, std::vector<std::string>>& getEquipTypes();

    void reInitListes();
    void drawAvaibleShelfPos();
    void checkIfCanPlaceInShelf(Camera& cam);
    void drawAllPlacedObjects(OBJModel& objmodel);
    void addPlacedObj(std::string name, svbmath::Vec3 pos);
    void sendPackage(std::vector<std::string>& equip, BuildingSettings& build);
    void delivery(float dt);
    void drawAllBoxes();
    void checkBoxesIntersection(Camera& cam);
    void drawEquipModel(std::string model, Camera& cam, bool placed, OBJModel& objmodel);
    void checkIfCanCreateDrone(Camera& cam, CashRegister& build);
    void initCoordinatesForShelves(Building& build);
};