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

class FPVDrone {
private:
    Components comp;
    std::string name = getStringFromJson("DRONE_Achetee");

    OBJModel fpv;

    std::vector<std::string> baseEquipment = {"Cadre t1","Camera CM1","Batterie 450W", "Moteur MTR1",
        "Hélice Type 1","Controlleur" ,"Lunettes",name, "Batterie 550W", "Batterie 500W",
        "Hélice Type 2", "Hélice Type 3","FC1","FC2","Controlleur  CTR1","Lunettes2","Cadre t2",
    "Moteur MTR2","Moteur MTR3","Camera CM2","Camera CM3"};

    std::map<std::string, float> equipmentPrice = { {"Cadre t1",100.0f},{"Camera CM1",300.0f},
        {"Batterie 450W",250.0f} ,{"Moteur MTR1",350.0f} ,{"Hélice Type 1",150.0f}, {"Controlleur",100.0f},
        {"Lunettes",250.0f},{name,1000.0f} ,{"Hélice Type 2",120.0f},{"Hélice Type 3",120.0f},
        {"Batterie 550W",450.0f} ,{"Batterie 500W",350.0f} ,{"FC1",150.0f}, {"FC2",100.0f},
        {"Lunettes2",270.0f},{"Controlleur  CTR1",90.0f},{"Cadre t2",130.0f},{"Moteur MTR2",400.0f},
        {"Moteur MTR3",320.0f},{"Camera CM2",270.0f},{"Camera CM3",330.0f} };

    std::map<std::string, std::unique_ptr<OBJModel>> allCompModels;
    std::map<std::string, ModelPaths> allCompPaths = {
     {"Cadre t1", {
         "res/models/fpv_frame/fpv_frame.obj",
         "res/models/fpv_frame/fpv_frame_carbon.png",
         5.0f
     }},
    {"Camera CM1", {
         "res/models/fpv_cam/fpv_camera.obj",
         "res/models/fpv_cam/fpv_camera_texture.png",
         5.0f
     }},
        {"Camera CM2", {
         "res/models/fpv_cam2/fpv_camera.obj",
         "res/models/fpv_cam2/tex.jpg",
         0.004f
     }},
        {"Camera CM3", {
         "res/models/fpv_cam3/fpv_camera.obj",
         "res/models/fpv_cam3/tex.jpg",
         0.004f
     }},
        {"Hélice Type 2", {
         "res/models/fpv_propeller2/prop_bi_5048.obj",
         "res/models/fpv_propeller2/tex.jpg",
         5.0f
     }},
        {"Hélice Type 3", {
         "res/models/fpv_propeller3/prop_tri_5143.obj",
         "res/models/fpv_propeller3/tex.jpg",
         5.0f
     }},
        {"Batterie 550W", {
         "res/models/fpv_bat2/fpv_battery.obj",
         "res/models/fpv_bat2/tex.jpg",
         5.0f
     }},
     {"Batterie 500W", {
         "res/models/fpv_bat3/fpv_battery.obj",
         "res/models/fpv_bat3/tex.jpg",
         5.0f
     }},
        {"FC1", {
         "res/models/fpv_FC1/fc_20x20_mini.obj",
         "res/models/fpv_FC1/tex.jpg",
         0.004f
     }},
     {"FC2", {
         "res/models/fpv_FC2/fc_30x30_f4.obj",
         "res/models/fpv_FC2/tex.jpg",
          0.004f
     }},
        {"Controlleur  CTR1", {
         "res/models/fpv_controller2/fpv_radio.obj",
         "res/models/fpv_controller2/tex.jpg",
        0.005f
     }},
     {"Lunettes2", {
         "res/models/fpv_goggles2/fpv_goggles.obj",
         "res/models/fpv_goggles2/tex.jpg",
         5.0f
     }},
     {"Batterie 450W", {
         "res/models/fpv_bat/battery.obj",
         "res/models/fpv_bat/battery_texture.png",
         5.0f
     }},
     {"Cadre t2", {
         "res/models/fpv_frame2/fpv_frame.obj",
         "res/models/fpv_frame2/tex.jpg",
         6.0f
     }},
     {"Moteur MTR1", {
         "res/models/fpv_motor/fpv_motor.obj",
         "res/models/fpv_motor/fpv_atlas.png",
         0.07f
     }},
        {"Moteur MTR2", {
         "res/models/fpv_motor2/fpv_motor.obj",
         "res/models/fpv_motor2/tex.jpg",
         0.007f
     }},
        {"Moteur MTR3", {
         "res/models/fpv_motor3/fpv_motor.obj",
         "res/models/fpv_motor3/tex.jpg",
         0.007f
     }},
     {"Hélice Type 1", {
         "res/models/fpv_propeller/fpv_propeller.obj",
         "res/models/fpv_propeller/fpv_atlas.png",
         0.04f
     }},
     {"Controlleur", {
         "res/models/fpv_controller/controller.obj",
         "res/models/fpv_controller/controller_texture.png",
         4.0f
     }},
     {"Lunettes", {
         "res/models/fpv_goggles/fpv_goggles.obj",
         "res/models/fpv_goggles/fpv_goggles_texture.png",
         5.0f
     }}
    };


    std::vector<Package> boxesWithEquip = {};
    std::vector<PlacedObject> placedObjects;
    std::vector<ShelfSetting> positionsOnShelves;

    float deliveryTime = 10.0; //sec
    float textTime = 3.0f;

    bool showText = false;
    bool inDelivery = false;
public:
    void init();
    void consumeComponents();

    Components& getComp();
    bool getShowText();
    std::vector<Package>& getOrderEquip();
    std::vector<PlacedObject>& getPlacedEquip();
    const std::vector<std::string>& getBaseEquip();
    const std::map<std::string, float>& getEquipPrice();
    bool isPlaced(const std::string& name) const;
    std::vector<svbmath::Vec3> generateShelfPoints(const Shelf& shelf);
    std::vector<ShelfSetting>& getShelfPositions();

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

    void drawCube(float sx, float sy, float sz);
    void drawCylinder(float radius, float height, int segments = 16);
    void drawDroneFrame(const svbmath::Vec3& pos);
    void drawDroneCamera(const svbmath::Vec3& pos);
    void drawDroneBattery(const svbmath::Vec3& pos);
    void drawMotor(const svbmath::Vec3& pos);
    void drawPropeller(const svbmath::Vec3& pos,bool reversed);
    void drawFPVDrone(const svbmath::Vec3& pos);
    void drawRemoteController(const svbmath::Vec3& pos);
    void drawFPVGoggles(const svbmath::Vec3& pos);
    void drawFPVEquipment();
};