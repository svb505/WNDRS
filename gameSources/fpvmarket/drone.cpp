#include "drone.h"
#include "text.h"
#include <glad/glad.h>
#include "variables.h"
#include "building.h"
#include "svbRandom.h"
#include "renders.h"
#include "actions.h"
#include "model.h"
#include <iostream>
#include "jsonParcer.h"
#include "text.h"
#include <memory>
#include <utility>
#include "logger.h"
#include "LoadingWin.h"
#include <future>

GLuint FPVDrone::returnCompPreview(const std::string& key) {
    static const std::unordered_map<std::string, std::string> compTextures = {
        {"FRAME1", "FRM1"},
        {"FRAME2", "FRM2"},
        {"CAM1", "CAM1"},
        {"CAM2", "CAM2"},
        {"CAM3", "CAM3"},
        {"BAT450", "BAT1"},
        {"BAT550", "BAT2"},
        {"BAT500", "BAT3"},
        {"MTR1", "MOT1"},
        {"MTR2", "MOT2"},
        {"MTR3", "MOT3"},
        {"PROP1", "PRP1"},
        {"PROP2", "PRP2"},
        {"PROP3", "PRP3"},
        {"CNTRL1", "CTRL1"},
        {"CNTRL2", "CTRL2"},
        {"GGLS1", "GGLS1"},
        {"GGLS2", "GGLS2"},
        {"FC1", "FC1"},
        {"FC2", "FC2"}
    };

    std::string componentKey;

    for (auto it = lang[currLang].begin(); it != lang[currLang].end(); ++it) {
        if (it.value().is_string() &&
            it.value().get<std::string>() == key) {
            componentKey = it.key();
            break;
        }
    }

    if (componentKey.empty()) componentKey = key;

    auto it = compTextures.find(componentKey);
    if (it == compTextures.end()) {
        LOG_ERROR(std::format("Preview not found for component: {}", key));
        return 0;
    }

    auto textureIt = texturesNamesAndPaths.find(it->second);
    if (textureIt == texturesNamesAndPaths.end()) {
        LOG_ERROR(std::format("Texture path not found: {}", it->second));
        return 0;
    }

    return LoadTexture(textureIt->second.c_str());
}
std::map<CompType, std::vector<std::string>>& FPVDrone::getEquipTypes() {
    return equipTypes;
}

void FPVDrone::reloadCompModels() {
    allCompModels.clear();

    for (const auto& [objName, paths] : allCompPaths) {
        auto model = std::make_unique<OBJModel>();

        model->LoadOBJ(paths.model, paths.scale);
        model->LoadTexture(paths.texture);
        model->CreateVBO();

        allCompModels.emplace(objName, std::move(model));
    }
}

void FPVDrone::reInitListes() {
    baseEquipment = { lang[currLang]["FRAME1"].get<std::string>(),
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

    equipmentPrice = { {baseEquipment[0],100.0f},{baseEquipment[1],300.0f},
        {baseEquipment[2],250.0f} ,{baseEquipment[3],350.0f} ,{baseEquipment[4],150.0f},
        {baseEquipment[5],100.0f},
        {baseEquipment[6],250.0f},{name,1000.0f} ,{baseEquipment[10],120.0f},{baseEquipment[11],120.0f},
        {baseEquipment[8],450.0f} ,{baseEquipment[9],350.0f} ,{baseEquipment[12],150.0f}, {baseEquipment[13],100.0f},
        {baseEquipment[15],270.0f},{baseEquipment[14],90.0f},{baseEquipment[16],130.0f},{baseEquipment[17],400.0f},
        {baseEquipment[18],320.0f},{baseEquipment[19],270.0f},{baseEquipment[20],330.0f} };

    allCompPaths = {
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

    equipTypes = { {CompType::TYPE1,
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

    reloadCompModels();
}
void FPVDrone::consumeComponents() {
    struct Need { std::vector<int> idx; int count; };
    const std::vector<Need> needs = {
        {{0, 16}, 1},      // frame
        {{1,19,20}, 1},          // camera
        {{2, 8, 9}, 1},    // battery
        {{3,17,18}, 4},          // motors
        {{4, 10, 11}, 4},  // propellers
        {{12, 13}, 1}      // fc
    };

    auto matches = [&](const std::string& n, const std::vector<int>& idx) {
        for (int i : idx) if (n == baseEquipment[i]) return true;
        return false;
        };

    for (const auto& need : needs) {
        int left = need.count;
        for (auto it = placedObjects.begin(); it != placedObjects.end() && left > 0; ) {
            if (matches(it->name, need.idx)) {
                for (auto& s : positionsOnShelves)
                    if (svbmath::InRadius(s.pos, it->pos, 0.01f))
                        s.busy = false;   // освободить слот
                it = placedObjects.erase(it);
                --left;
            }
            else {
                ++it;
            }
        }
    }
}
void FPVDrone::init(GLFWwindow* win) {
    LoadingScreen::Show(win, "Loading assets...");

    markerModel.LoadOBJ("res/models/marker/free_slot_marker.obj", 0.08f);
    markerModel.CreateVBO();

    fpv.LoadOBJ("res/models/fpv_assemblee/fpv_drone.obj", 6.0f);
    fpv.LoadTexture("res/models/fpv_assemblee/fpv_drone_texture.png");
    fpv.CreateVBO();

    LoadingScreen::Show(win, "Loading components...");

    using ModelFuture = std::future<std::pair<std::string, std::unique_ptr<OBJModel>>>;

    std::vector<ModelFuture> futures;

    for (const auto& [objName, paths] : allCompPaths) {
        futures.push_back(std::async(std::launch::async, [objName, paths]() {
                auto model = std::make_unique<OBJModel>();

                model->LoadOBJ(paths.model, paths.scale);

                return std::make_pair(objName, std::move(model));
            }
        ));
    }

    for (auto& future : futures) {
        auto [objName, model] = future.get();

        model->LoadTexture(allCompPaths[objName].texture);
        model->CreateVBO();

        allCompModels.emplace(objName, std::move(model));
    }
}
Components& FPVDrone::getComp() {
    return comp;
}
std::vector<svbmath::Vec3> FPVDrone::generateShelfPoints(const Shelf& shelf) {
    std::vector<svbmath::Vec3> points;

    const int count = 5;
    const float edgeOffset = 0.3f;

    if (shelf.width >= shelf.depth) {

        float y = shelf.max.y;

        float minX = shelf.min.x + edgeOffset;
        float maxX = shelf.max.x - edgeOffset;

        for (int i = 0; i < count; i++) {
            float t = static_cast<float>(i) / (count - 1);

            float x = minX + (maxX - minX) * t;

            float z = shelf.position.z;

            points.push_back({ x, y, z });
        }
    }
    else {

        float y = shelf.max.y;

        float minZ = shelf.min.z + edgeOffset;
        float maxZ = shelf.max.z - edgeOffset;

        for (int i = 0; i < count; i++) {
            float t = static_cast<float>(i) / (count - 1);

            float z = minZ + (maxZ - minZ) * t;

            float x = shelf.position.x;

            points.push_back({ x, y, z });
        }
    }

    return points;
}
std::vector<PlacedObject>& FPVDrone::getPlacedEquip() {
    return placedObjects;
}
void FPVDrone::drawAvaibleShelfPos() {
    for (auto& shelf : positionsOnShelves) {

        bool occupied = false;

        for (const auto& obj : placedObjects) {
            if (svbmath::InRadius(obj.pos, shelf.pos, 0.01f)) {
                occupied = true;
                break;
            }
        }


        float shelfYaw = (shelf.pos.x == 4.8f) ? 90.0f : 0.0f;

        if (!shelf.busy && !occupied) markerModel.Draw(shelf.pos, shelfYaw, 0.0f);
    }
}
void FPVDrone::initCoordinatesForShelves(Building& build) {
    for (const auto& shelf : build.getShelves()){
        auto points = generateShelfPoints(shelf);

        for (const auto& point : points) positionsOnShelves.push_back({point,false});
    }
    
}
void FPVDrone::checkIfCanPlaceInShelf(Camera& cam) {
    for (auto& obj : positionsOnShelves) {
        if (svbmath::InRadius(cam.getCamPos(), obj.pos, 1.0f) && 
            (objName == baseEquipment[7] || objName == getStringFromJson("DRONE_Assemblee")
                || objName == baseEquipment[5] || objName == baseEquipment[6] || 
                objName == baseEquipment[14] || objName == baseEquipment[15]) && !obj.busy) {

            addPlacedObj(objName, obj.pos);

            obj.busy = true;

            objName.clear();
            placeObj = false;
            canDrawEquipModel = false;

            return;
        }
    }
}
std::vector<ShelfSetting>& FPVDrone::getShelfPositions() {
    return positionsOnShelves;
}
bool FPVDrone::isPlaced(const std::string& name) const {
    for (const auto& obj : placedObjects) {
        if (obj.name == name)
            return true;
    }
    return false;
}
bool FPVDrone::getShowText() {
    return showText;
}
const std::vector<std::string>& FPVDrone::getBaseEquip() {
    return baseEquipment;
}
const std::map<std::string, float>& FPVDrone::getEquipPrice() {
    return equipmentPrice;
}
std::vector<Package>& FPVDrone::getOrderEquip() {
    return boxesWithEquip;
}
void FPVDrone::drawAllBoxes() {
    for (auto& box : boxesWithEquip) if (box.render) 
        drawBox(0.6f, 0.6f, 0.6f, box.pos, box.texture);
}
void FPVDrone::drawAllPlacedObjects(OBJModel& objmodel) {
    for (const auto& obj : placedObjects) {
        glPushMatrix();

        glTranslatef(obj.pos.x, obj.pos.y, obj.pos.z);
        glScalef(0.25f, 0.25f, 0.25f);

        svbmath::Vec3 localPos = { 0.0f, 0.3f, 0.0f };

        if (obj.name == baseEquipment[7]) {
            RenderTextWorld(localPos.x, localPos.y + 0.2f, localPos.z, 1, 1, 1, name.c_str());
            objmodel.Draw(localPos, 0.0f, 0.0f);
        }

        if (obj.name == getStringFromJson("DRONE_Assemblee")) {
            RenderTextWorld(localPos.x, localPos.y + 0.2f, localPos.z, 1, 1, 1,
                getStringFromJson("DRONE_Assemblee").c_str());
            fpv.Draw(localPos, 0.0f, 0.0f);
        }
        if (obj.name != getStringFromJson("DRONE_Assemblee") && obj.name != baseEquipment[7]) {
            allCompModels[obj.name]->Draw(localPos, 0.0f, 0.0f);
        }

        glPopMatrix();
    }
}
void FPVDrone::checkIfCanCreateDrone(Camera& cam, CashRegister& build) {
    comp = { 0,0,0,0,0,0,0 };

    svbmath::Vec3 basePos;
    int idx = 0;

    for (auto& obj : placedObjects) {
        if (idx == 0) basePos = obj.pos;

        if (obj.name == baseEquipment[0] || obj.name == baseEquipment[16]) comp.frame++;
        if (obj.name == baseEquipment[1] || obj.name == baseEquipment[19] || obj.name == baseEquipment[20]) comp.camera++;
        if (obj.name == baseEquipment[2] || obj.name == baseEquipment[8] || obj.name == baseEquipment[9]) comp.battery++;
        if (obj.name == baseEquipment[3] || obj.name == baseEquipment[17] || obj.name == baseEquipment[18]) comp.motor++;
        if (obj.name == baseEquipment[4] || obj.name == baseEquipment[10] || obj.name == baseEquipment[11]) comp.propeller++;
        if (obj.name == baseEquipment[12] || obj.name == baseEquipment[13]) comp.fc++;

        idx++;
    }

    if (comp.battery >= 1 && comp.frame >= 1 && comp.camera >= 1 && comp.motor >= 4 && 
        comp.propeller >= 4 && comp.fc >= 1 && svbmath::InRadius(cam.getCamPos(), build.position, 5.0f)){
        
        float size = 64.0f;
        float x = ECRAN_W / 2.0f;
        float y = ECRAN_H / 2.0f;

        render2DIcon("HAND", { x, y }, size);

        RenderTextHUD(x - 30.0f, y - 30.0f, 1.0f, 1.0f, 1.0f, "E", ECRAN_W, ECRAN_H);

        canCreateDrone = true;
    }
}
void FPVDrone::drawEquipModel(std::string model,Camera& cam,bool placed,OBJModel& objmodel) {    
    if (placed) {
        for (const auto& obj : placedObjects) {
            if (obj.name != model) continue;

            glPushMatrix();
            glTranslatef(obj.pos.x, obj.pos.y, obj.pos.z);
            glScalef(0.25f, 0.25f, 0.25f);

            svbmath::Vec3 localPos = { 0.0f, 0.0f, 0.0f };

            if (model == baseEquipment[7]) {
                RenderTextWorld(localPos.x, localPos.y + 0.2f, localPos.z, 1, 1, 1, name.c_str());
                objmodel.Draw(localPos, 0.0f, 0.0f);
            }

            else if (model == getStringFromJson("DRONE_Assemblee")) {
                RenderTextWorld(localPos.x, localPos.y + 0.2f, localPos.z, 1, 1, 1,
                    getStringFromJson("DRONE_Assemblee").c_str());
                fpv.Draw(localPos, 0.0f, 0.0f);
            }
            else {
                allCompModels[model]->Draw(localPos, 0.0f, 0.0f);
            }


            glPopMatrix();
        }
        return;
    }

    svbmath::Vec3 forward = svbmath::Normalize(cam.getCamForward());
    svbmath::Vec3 objectPos = cam.getCamPos() + forward * 1.0f;
    objectPos.y -= 0.3f;

    glPushMatrix();
    glTranslatef(objectPos.x, objectPos.y, objectPos.z);
    glScalef(0.25f, 0.25f, 0.25f);

    svbmath::Vec3 localPos = { 0.0f, 0.0f, 0.0f };

    if (model == baseEquipment[7]) {
        RenderTextWorld(localPos.x, localPos.y + 0.2f, localPos.z, 1, 1, 1, name.c_str());
        objmodel.Draw(localPos, 0.0f, 0.0f);
    }

    else if (model == getStringFromJson("DRONE_Assemblee")) {
        RenderTextWorld(localPos.x, localPos.y + 0.2f, localPos.z, 1, 1, 1,
            getStringFromJson("DRONE_Assemblee").c_str());
        fpv.Draw(localPos, 0.0f, 0.0f);
    }
    else {
        allCompModels[model]->Draw(localPos, 0.0f, 0.0f);
    }

    glPopMatrix();
}
void FPVDrone::checkBoxesIntersection(Camera& cam) {
    canTakeObj = false;

    for (auto it = boxesWithEquip.begin(); it != boxesWithEquip.end(); ){
        Package& box = *it;

        if (box.currentIndex >= static_cast<int>(box.equip.size())) {
            it = boxesWithEquip.erase(it);
            continue;
        }

        if (box.render && canInteract(cam.getCamPos(),cam.getCamForward(),box.pos,4.0f)) {
            canTakeObj = true;

            float size = 64.0f;
            float x = (ECRAN_W - size) / 2.0f;
            float y = ECRAN_H - size - 60.0f;

            render2DIcon("HAND", { x, y }, size);

            RenderTextHUD( x - 30.0f, y - 30.0f, 1.0f,1.0f,1.0f,"E", ECRAN_W, ECRAN_H);
        }

        ++it;
    }
}
void FPVDrone::sendPackage(std::vector<std::string>& equip, BuildingSettings& build) {
    float step = 0.2f;

    svbmath::Vec3 boxPos = { 0.0f,0.0f,0.0f };

    float minX = build.warehouseCenter.x - build.warehouseWidth / 2.0f;
    float maxX = build.warehouseCenter.x + build.warehouseWidth / 2.0f;

    float minZ = build.warehouseCenter.z - build.warehouseLength / 2.0f;
    float maxZ = build.warehouseCenter.z + build.warehouseLength / 2.0f;

    boxPos.x = returnRandomNum(minX + step, maxX - step);
    boxPos.z = returnRandomNum(minZ + step, maxZ - step);
    
    GLuint texture = (returnRandomNum(0.0f, 1.0f) < 0.5) ? allTextures["BOX1"] : allTextures["BOX2"];

    boxesWithEquip.push_back({ equip, boxPos, texture, false, 0 });
    inDelivery = true;
}
void FPVDrone::delivery(float dt) {
    if (inDelivery) {
        if (deliveryTime > 0.0f) deliveryTime -= dt;
        else {
            deliveryTime = 10.0f;
            inDelivery = false;
            showText = true;

            for (auto& box : boxesWithEquip) box.render = true;
        }
    }
    if (showText) {
        if (textTime > 0.0f) textTime -= dt;
        else {
            textTime = 3.0f;
            showText = false;
        }
    }
}
void FPVDrone::addPlacedObj(std::string name, svbmath::Vec3 pos) {
    placedObjects.push_back({ name, pos });
}