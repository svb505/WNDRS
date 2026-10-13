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

void FPVDrone::consumeComponents() {
    struct Need { std::vector<int> idx; int count; };
    const std::vector<Need> needs = {
        {{0, 16}, 1},      // frame
        {{1}, 1},          // camera
        {{2, 8, 9}, 1},    // battery
        {{3}, 4},          // motors
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
void FPVDrone::init() {
    fpv.LoadOBJ("res/models/fpv_assemblee/fpv_drone.obj", 6.0f);
    fpv.LoadTexture("res/models/fpv_assemblee/fpv_drone_texture.png");
    fpv.CreateVBO();

    for (const auto& [objName, paths] : allCompPaths) {
        auto model = std::make_unique<OBJModel>();

        model->LoadOBJ(paths.model, paths.scale);
        model->LoadTexture(paths.texture);
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

        if (!shelf.busy && !occupied)
            drawQuad(0.4f, 0.4f, 0.4f, shelf.pos);
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
void FPVDrone::drawCube(float sx, float sy, float sz) {
    sx /= 2.0f;
    sy /= 2.0f;
    sz /= 2.0f;

    glBegin(GL_QUADS);

    // Front (+Z)
    glNormal3f(0, 0, 1);
    glVertex3f(-sx, -sy, sz);
    glVertex3f(sx, -sy, sz);
    glVertex3f(sx, sy, sz);
    glVertex3f(-sx, sy, sz);

    // Back (-Z)
    glNormal3f(0, 0, -1);
    glVertex3f(sx, -sy, -sz);
    glVertex3f(-sx, -sy, -sz);
    glVertex3f(-sx, sy, -sz);
    glVertex3f(sx, sy, -sz);

    // Left (-X)
    glNormal3f(-1, 0, 0);
    glVertex3f(-sx, -sy, -sz);
    glVertex3f(-sx, -sy, sz);
    glVertex3f(-sx, sy, sz);
    glVertex3f(-sx, sy, -sz);

    // Right (+X)
    glNormal3f(1, 0, 0);
    glVertex3f(sx, -sy, sz);
    glVertex3f(sx, -sy, -sz);
    glVertex3f(sx, sy, -sz);
    glVertex3f(sx, sy, sz);

    // Top
    glNormal3f(0, 1, 0);
    glVertex3f(-sx, sy, sz);
    glVertex3f(sx, sy, sz);
    glVertex3f(sx, sy, -sz);
    glVertex3f(-sx, sy, -sz);

    // Bottom
    glNormal3f(0, -1, 0);
    glVertex3f(-sx, -sy, -sz);
    glVertex3f(sx, -sy, -sz);
    glVertex3f(sx, -sy, sz);
    glVertex3f(-sx, -sy, sz);

    glEnd();
}
void FPVDrone::drawCylinder(float radius, float height, int segments) {
    float half = height / 2.0f;

    // Боковая поверхность
    glBegin(GL_QUAD_STRIP);

    for (int i = 0; i <= segments; i++)
    {
        float a = 2.0f * 3.14159265f * i / segments;
        float x = cosf(a) * radius;
        float z = sinf(a) * radius;

        glNormal3f(x, 0, z);

        glVertex3f(x, -half, z);
        glVertex3f(x, half, z);
    }

    glEnd();

    // Верх
    glBegin(GL_TRIANGLE_FAN);
    glNormal3f(0, 1, 0);
    glVertex3f(0, half, 0);

    for (int i = 0; i <= segments; i++)
    {
        float a = 2.0f * 3.14159265f * i / segments;
        glVertex3f(
            cosf(a) * radius,
            half,
            sinf(a) * radius
        );
    }

    glEnd();

    // Низ
    glBegin(GL_TRIANGLE_FAN);
    glNormal3f(0, -1, 0);
    glVertex3f(0, -half, 0);

    for (int i = 0; i <= segments; i++)
    {
        float a = -2.0f * 3.14159265f * i / segments;

        glVertex3f(
            cosf(a) * radius,
            -half,
            sinf(a) * radius
        );
    }

    glEnd();
}
void FPVDrone::drawDroneFrame(const svbmath::Vec3& pos) {
    glPushMatrix();

    glTranslatef(pos.x, pos.y, pos.z);

    glColor3f(0.08f, 0.08f, 0.08f);

    drawCube(1.8f, 0.12f, 2.1f);

    glTranslatef(0.0f, 0.22f, 0.0f);
    drawCube(1.6f, 0.10f, 1.8f);

    // Четыре луча
    glColor3f(0.12f, 0.12f, 0.12f);

    glPushMatrix();
    glTranslatef(-0.9f, 0.0f, 0.95f);
    glRotatef(-45.0f, 0, 1, 0);
    drawCube(1.8f, 0.14f, 0.18f);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0.9f, 0.0f, 0.95f);
    glRotatef(45.0f, 0, 1, 0);
    drawCube(1.8f, 0.14f, 0.18f);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(-0.9f, 0.0f, -0.95f);
    glRotatef(45.0f, 0, 1, 0);
    drawCube(1.8f, 0.14f, 0.18f);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0.9f, 0.0f, -0.95f);
    glRotatef(-45.0f, 0, 1, 0);
    drawCube(1.8f, 0.14f, 0.18f);
    glPopMatrix();

    glPopMatrix();
}
void FPVDrone::drawDroneCamera(const svbmath::Vec3& pos) {
    glPushMatrix();

    glTranslatef(pos.x, pos.y, pos.z);

    // Камера спереди
    glTranslatef(0.0f, 0.28f, 1.12f);

    glColor3f(0.06f, 0.06f, 0.06f);
    drawCube(0.65f, 0.45f, 0.55f);

    glTranslatef(0.0f, -0.02f, 0.28f);

    glColor3f(0.02f, 0.02f, 0.02f);

    glRotatef(90.0f, 1, 0, 0);
    drawCylinder(0.17f, 0.18f);

    glTranslatef(0.0f, 0.0f, 0.1f);

    glColor3f(0.02f, 0.08f, 0.12f);
    drawCylinder(0.13f, 0.05f);

    glPopMatrix();
}
void FPVDrone::drawDroneBattery(const svbmath::Vec3& pos) {
    glPushMatrix();

    glTranslatef(pos.x, pos.y, pos.z);

    glTranslatef(0.0f, 0.42f, -0.05f);

    glColor3f(0.03f, 0.03f, 0.03f);

    drawCube(0.95f, 0.42f, 1.5f);

    glColor3f(0.15f, 0.15f, 0.15f);

    glPushMatrix();
    glTranslatef(0.0f, 0.23f, 0.0f);
    drawCube(1.05f, 0.05f, 0.12f);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0.0f, 0.23f, 0.5f);
    drawCube(1.05f, 0.05f, 0.12f);
    glPopMatrix();

    glColor3f(0.08f, 0.08f, 0.08f);

    glPushMatrix();
    glTranslatef(0.25f, 0.55f, -0.78f);
    glRotatef(90.0f, 1, 0, 0);
    drawCylinder(0.025f, 0.4f);
    glPopMatrix();

    glPopMatrix();
}
void FPVDrone::drawMotor(const svbmath::Vec3& pos) {
    glPushMatrix();

    glTranslatef(pos.x, pos.y, pos.z);

    glColor3f(0.16f, 0.16f, 0.16f);

    drawCylinder(0.20f, 0.20f);

    glTranslatef(0.0f, 0.14f, 0.0f);

    glColor3f(0.25f, 0.25f, 0.25f);

    drawCylinder(0.14f, 0.08f);

    glPopMatrix();
}
void FPVDrone::drawPropeller(const svbmath::Vec3& pos, bool reversed) {
    glPushMatrix();

    glTranslatef(pos.x, pos.y, pos.z);

    glColor3f(0.02f, 0.02f, 0.02f);

    // Центральная втулка
    drawCylinder(0.06f, 0.05f);

    glTranslatef(0.0f, 0.04f, 0.0f);

    // Первый лепесток
    glPushMatrix();

    if (reversed)
        glRotatef(180.0f, 0, 1, 0);

    glBegin(GL_QUADS);

    glVertex3f(0.0f, 0.0f, 0.0f);
    glVertex3f(0.75f, 0.0f, 0.08f);
    glVertex3f(0.95f, 0.0f, 0.02f);
    glVertex3f(0.25f, 0.0f, -0.08f);

    glEnd();

    glPopMatrix();

    // Второй лепесток
    glPushMatrix();

    glRotatef(180.0f, 0, 1, 0);

    glBegin(GL_QUADS);

    glVertex3f(0.0f, 0.0f, 0.0f);
    glVertex3f(0.75f, 0.0f, 0.08f);
    glVertex3f(0.95f, 0.0f, 0.02f);
    glVertex3f(0.25f, 0.0f, -0.08f);

    glEnd();

    glPopMatrix();

    glPopMatrix();
}
void FPVDrone::drawFPVDrone(const svbmath::Vec3& pos) {

    // Рама
    drawDroneFrame(pos);

    // Камера
    drawDroneCamera(pos);

    // Аккумулятор
    drawDroneBattery(pos);


    // -------------------------
    // Моторы + пропеллеры
    // -------------------------

    // Front Left
    glPushMatrix();

    glTranslatef(pos.x - 1.30f,
        pos.y + 0.05f,
        pos.z + 1.30f);

    drawMotor(pos);

    glTranslatef(0.0f, 0.20f, 0.0f);
    drawPropeller(pos,false);

    glPopMatrix();


    // Front Right
    glPushMatrix();

    glTranslatef(pos.x + 1.30f,
        pos.y + 0.05f,
        pos.z + 1.30f);

    drawMotor(pos);

    glTranslatef(0.0f, 0.20f, 0.0f);
    glRotatef(30.0f, 0, 1, 0);
    drawPropeller(pos,true);

    glPopMatrix();


    // Rear Left
    glPushMatrix();

    glTranslatef(pos.x - 1.30f,
        pos.y + 0.05f,
        pos.z - 1.30f);

    drawMotor(pos);

    glTranslatef(0.0f, 0.20f, 0.0f);
    glRotatef(30.0f, 0, 1, 0);
    drawPropeller(pos,true);

    glPopMatrix();


    // Rear Right
    glPushMatrix();

    glTranslatef(pos.x + 1.30f,
        pos.y + 0.05f,
        pos.z - 1.30f);

    drawMotor(pos);

    glTranslatef(0.0f, 0.20f, 0.0f);
    drawPropeller(pos,false);

    glPopMatrix();


    // -------------------------
    // Радиоантенны
    // -------------------------

    glColor3f(0.05f, 0.05f, 0.05f);

    float antennaX[] = { -0.3f, 0.3f };

    for (float x : antennaX) {

        glPushMatrix();

        glTranslatef(pos.x + x,
            pos.y + 0.35f,
            pos.z - 1.0f);

        glRotatef(-20.0f, 1, 0, 0);

        drawCylinder(0.025f, 0.7f);

        glPopMatrix();
    }


    // -------------------------
    // Радиоприёмник
    // -------------------------

    glPushMatrix();

    glTranslatef(pos.x,
        pos.y + 0.4f,
        pos.z - 0.8f);

    glColor3f(0.05f, 0.08f, 0.05f);

    drawCube(0.40f, 0.15f, 0.55f);

    glPopMatrix();
}
void FPVDrone::drawRemoteController(const svbmath::Vec3& pos) {
    glPushMatrix();

    glTranslatef(pos.x, pos.y, pos.z);

    glColor3f(0.08f, 0.08f, 0.08f);

    drawCube(2.2f, 0.35f, 1.3f);

    glPushMatrix();

    glTranslatef(-0.55f, 0.25f, 0.1f);

    glColor3f(0.15f, 0.15f, 0.15f);
    drawCylinder(0.13f, 0.12f);

    glTranslatef(0.0f, 0.12f, 0.0f);

    glColor3f(0.25f, 0.25f, 0.25f);
    drawCylinder(0.05f, 0.25f);

    glPopMatrix();


    glPushMatrix();

    glTranslatef(0.55f, 0.25f, 0.1f);

    glColor3f(0.15f, 0.15f, 0.15f);
    drawCylinder(0.13f, 0.12f);

    glTranslatef(0.0f, 0.12f, 0.0f);

    glColor3f(0.25f, 0.25f, 0.25f);
    drawCylinder(0.05f, 0.25f);

    glPopMatrix();


    glPushMatrix();

    glTranslatef(0.0f, 0.23f, -0.30f);

    glColor3f(0.02f, 0.07f, 0.08f);

    drawCube(0.65f, 0.08f, 0.35f);

    glPopMatrix();


    glColor3f(0.12f, 0.12f, 0.12f);

    float antenaX[] = { -0.45f, 0.45f };

    for (float x : antenaX) {

        glPushMatrix();

        glTranslatef(x, 0.45f, -0.45f);

        glRotatef(-20.0f, 1, 0, 0);

        drawCylinder(0.035f, 0.8f);

        glPopMatrix();
    }

    glPopMatrix();
}
void FPVDrone::drawFPVGoggles(const svbmath::Vec3& pos) {
    glPushMatrix();

    glTranslatef(pos.x, pos.y, pos.z);

    // Левая часть
    glPushMatrix();

    glTranslatef(-0.48f, 0.0f, 0.0f);

    glColor3f(0.06f, 0.06f, 0.06f);

    drawCube(0.9f, 0.55f, 0.55f);

    glTranslatef(0.0f, 0.0f, 0.30f);

    glColor3f(0.03f, 0.10f, 0.14f);

    drawCube(0.6f, 0.32f, 0.03f);

    glPopMatrix();


    // Правая часть
    glPushMatrix();

    glTranslatef(0.48f, 0.0f, 0.0f);

    glColor3f(0.06f, 0.06f, 0.06f);

    drawCube(0.9f, 0.55f, 0.55f);

    glTranslatef(0.0f, 0.0f, 0.30f);

    glColor3f(0.03f, 0.10f, 0.14f);

    drawCube(0.6f, 0.32f, 0.03f);

    glPopMatrix();


    // Перемычка
    glColor3f(0.08f, 0.08f, 0.08f);

    glPushMatrix();

    glTranslatef(0.0f, 0.0f, -0.05f);

    drawCube(0.45f, 0.25f, 0.5f);

    glPopMatrix();


    // Ремень
    glColor3f(0.03f, 0.03f, 0.03f);

    glPushMatrix();

    glTranslatef(0.0f, 0.0f, -0.45f);

    glRotatef(90.0f, 1, 0, 0);

    drawCube(1.8f, 0.1f, 0.15f);

    glPopMatrix();

    glPopMatrix();
}
void FPVDrone::drawFPVEquipment() {
    glDisable(GL_TEXTURE_2D);

    // Дрон
    glPushMatrix();

    glTranslatef(0.0f, 0.5f, 7.0f);
    glScalef(0.4f, 0.4f, 0.4f);

    drawFPVDrone({ 0.0f, 0.0f, 0.0f });

    glPopMatrix();


    // Пульт
    glPushMatrix();

    glTranslatef(5.0f, 0.5f, 7.0f);
    glRotatef(25.0f, 0, 1, 0);

    drawRemoteController({ 0.0f, 0.0f, 0.0f });

    glPopMatrix();


    // Очки
    glPushMatrix();

    glTranslatef(-5.0f, 0.5f, 7.0f);
    glRotatef(-20.0f, 0, 1, 0);

    drawFPVGoggles({ 0.0f, 0.0f, 0.0f });

    glPopMatrix();

    glEnable(GL_TEXTURE_2D);
}