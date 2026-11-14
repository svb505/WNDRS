#ifndef GL_MULTISAMPLE
#define GL_MULTISAMPLE 0x809D
#endif
#include <windows.h>
#include "glad/glad.h"
#define GLFW_INCLUDE_NONE
#include <GLFW/glfw3.h>

#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"

#include <iostream>
#include <cmath>
#include "camera.h"
#include "text.h"
#include "texture.h"
#include "lighting.h"
#include "environnement.h"
#include "building.h"
#include "bounds.h"
#include "variables.h"
#include "input.h"
#include "model.h"
#include <algorithm>
#include "decorations.h"
#include "text.h"
#include <format>
#include "GUI.h"
#include "drone.h"
#include "actions.h"
#include "database.h"
#include "sound.h"
#include "bot.h"
#include "renders.h"
#include "logger.h"
#include "stb_image.h"
#include "localization.h"
#include "days.h"
#include "LoadingWin.h"
#include <nlohmann//json.hpp>
#include <fstream>

using json = nlohmann::json;

json mapJson;

Camera cam;
Building build;
OBJModel base;
Decorations decor;
Sound sound;
Bot bot;

void loadMap(const std::string& path){
    std::ifstream file(path);

    if (!file.is_open()) return;

    file >> mapJson;
    file.close();
}
void updateCursorMode(GLFWwindow* window){
    if (hideCursor)  glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
    else glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
}
void setMatrix(float left, float right, float bottom, float top, float nearP, float farP) {
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glFrustum(left, right, bottom, top, nearP, farP);

    glMatrixMode(GL_MODELVIEW);
}
void countFps(FPS& fpsVars, double& lastTime, double& currentTime) {
    fpsVars.deltaTime = currentTime - lastTime;
    lastTime = currentTime;

    fpsVars.fpsTimer += fpsVars.deltaTime;
    fpsVars.frames++;

    if (fpsVars.fpsTimer >= 1.0f) {
        if (fpsVars.fps < fpsVars.minFps || fpsVars.minFps == 0.0f) fpsVars.minFps = fpsVars.fps;
        if (fpsVars.fps > fpsVars.maxFps) fpsVars.maxFps = fpsVars.fps;

        fpsVars.fps = fpsVars.frames / fpsVars.fpsTimer;
        fpsVars.frames = 0;
        fpsVars.fpsTimer = 0.0f;
    }
}
void mouse_callback(GLFWwindow* window, double xpos, double ypos) {
    if (!hideCursor) return;

    CameraParams& params = cam.getCamParams();

    static bool first = true;
    static double lastX = 0.0;
    static double lastY = 0.0;

    if (first) {
        lastX = xpos;
        lastY = ypos;
        first = false;
        return;
    }

    double xoffset = xpos - lastX;
    double yoffset = ypos - lastY;

    lastX = xpos;
    lastY = ypos;

    xoffset *= sensitivity;
    yoffset *= sensitivity;

    params.cameraYaw += -(float)xoffset;
    params.cameraPitch -= (float)yoffset;
}
int main() {
    currLang = getStringFromJson("CURR_LANG", "config.json");

    getLangJson();

    Logger::initLogger();

    GUI gui;
    FPVDrone drone;

    CameraParams& params = cam.getCamParams();

    if (!dbIsExists()) createDb();


    for (auto& p : getDataForPlayer().players) {
        myBalance = p.balance;
        day = p.day;
        level = p.level;
        purchasesForAllTime = p.purchases;
    }

    int width, height, channels;
    unsigned char* pixels = stbi_load("icon.jpg", &width, &height, &channels, 4);


    if (!glfwInit()) {
        LOG_ERROR("Failed to initialize GLFW");
        return -1;
    }

    glfwWindowHint(GLFW_SAMPLES, 16);
    GLFWwindow* window = glfwCreateWindow(ECRAN_W, ECRAN_H, "FPV Market - V2.2.3", NULL, NULL);

    if (!window) {
        LOG_ERROR("Failed to create window");
        glfwTerminate();
        return -1;
    }

    if (pixels) {
        GLFWimage icon{ width, height, pixels };
        glfwSetWindowIcon(window, 1, &icon);
        stbi_image_free(pixels);
    }


    glfwSetWindowUserPointer(window, &cam);
    glfwMakeContextCurrent(window);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        LOG_ERROR("Failed to initialize GLAD");

        glfwDestroyWindow(window);
        glfwTerminate();

        return -1;
    }

    glClearColor(0.6f, 0.8f, 1.0f, 1.0f);;
    BuildFont();

    glEnable(GL_MULTISAMPLE);
    glEnable(GL_DEPTH_TEST);

    setMatrix(params.left, params.right, params.bottom, params.top, params.nearPlane,
        params.farPlane);

    double lastTime = glfwGetTime();
    FPS fpsVars;

    initLighting();
    LoadAllTextures();
    loadMap("maps/map.json");

    sound.setupBuffers();
    sound.createSources();

    LoadingScreen::Show(window, "Loading fpv drone...");
    base.LoadOBJ("res/models/fpv/base.obj", 1.0f);
    base.LoadTexture("res/models/fpv/texture_diffuse.png");
    base.CreateVBO();

    build.CreateBuilding(window);

    LoadingScreen::Show(window, "Loading buildings...");
    decor.initDecoration("res/models/builds/rue_2_cotes_complete.obj", DecType::STREET, "");
    
    LoadingScreen::Show(window, "Loading fences...");
    decor.initDecoration("res/models/fence/city_fence.obj", DecType::FENCE, "");

    LoadingScreen::Show(window, "Loading trees...");
    decor.initDecoration("res/models/trees/tree.obj", DecType::TREE,
        "res/models/trees/tex.jpg");

    LoadingScreen::Show(window, "Loading street lamps...");
    decor.initDecoration("res/models/streetlamp/streetlamp.obj", DecType::LAMP,
        "res/models/streetlamp/texture.png");

    decor.initPositions("maps/map.json");

    glfwSetCursorPosCallback(window, mouse_callback);

    gui.setupGui(window);

    svbmath::Vec3 point;

    drone.init(window);
    drone.initCoordinatesForShelves(build);

    bot.init(window);

    for (auto& p : getDataForPlayer().players) ratings.push_back(p.rating);

    while (!glfwWindowShouldClose(window)) {
        updateCursorMode(window);

        double currentTime = glfwGetTime();

        countFps(fpsVars, lastTime, currentTime);

        if (!bot.isActive()) bot.spawn(drone, build);

        bot.update(fpsVars.deltaTime, cam, drone, build, sound, true);

        processInput(window, cam, drone, fpsVars.deltaTime, point, sound);

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        gui.renderAll(fpsVars, drone, build.getBuildSettings(),build);

        ImGui::Render();

        cam.setupCamera();

        drawSky();
        drawGround();
        drawRoadsFromJson(mapJson);

        glEnable(GL_POLYGON_OFFSET_FILL);
        glPolygonOffset(-2.0f, -2.0f);

        drone.delivery(fpsVars.deltaTime);
        drone.drawAllBoxes();
        drone.checkIfCanPlaceInShelf(cam);

        bot.draw();

        if (canDrawEquipModel && !objName.empty()) drone.drawEquipModel(objName, cam, false, base);

        drone.drawAllPlacedObjects(base);
        drone.drawAvaibleShelfPos();

        build.DrawBuilding();
        if (build.checkCollision(cam)) cam.getCamPos() = cam.getOldCamPos();

        if (build.isInsideBuilding(cam.getCamPos())) setLighting(indoorLight);
        else {
            if (heure > 4 && heure < 20) setLighting(outdoorDayLight);
            else setLighting(outdoorNightLight);
        }

        placeObj = false;

        if (canDrawEquipModel && !objName.empty()) {
            svbmath::Vec3 lookPoint;

            if (getCashRegisterLookPoint(cam.getCamPos(), cam.getCamForward(), build.getCashRegister(), lookPoint)) {
                float size = 64.0f;
                float x = ECRAN_W / 2.0f;
                float y = ECRAN_H / 2.0f;

                render2DIcon("HAND", { x, y }, size);

                RenderTextHUD(x - 30.0f, y - 30.0f, 1.0f, 1.0f, 1.0f, "E", ECRAN_W, ECRAN_H);

                point = lookPoint;
                placeObj = true;
            }
        }


        drone.checkBoxesIntersection(cam);
        drone.checkIfCanCreateDrone(cam, build.getCashRegister());

        decor.drawAllDecorations(DecType::STREET);
        decor.drawAllDecorations(DecType::TREE);
        decor.drawAllDecorations(DecType::LAMP);
        decor.drawAllDecorations(DecType::FENCE);

        if (decor.checkCollision(cam, DecType::STREET)) cam.getCamPos() = cam.getOldCamPos();
        if (decor.checkCollision(cam, DecType::TREE)) cam.getCamPos() = cam.getOldCamPos();
        if (decor.checkCollision(cam, DecType::LAMP)) cam.getCamPos() = cam.getOldCamPos();
        if (decor.checkCollision(cam, DecType::FENCE)) cam.getCamPos() = cam.getOldCamPos();

        if (drone.getShowText()) {
            RenderTextHUD(ECRAN_W / 2, ECRAN_H / 2, 1.0f, 0.0f, 0.0f,
                "Your package has arrived", ECRAN_W, ECRAN_H);
        }

        countDays(fpsVars.deltaTime);

        drawPointInCenter();

        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    saveDayToDb(day);
    saveLevelAndPurchasesToDb(level,purchasesForSession);

    Logger::shutDown();

    gui.destroyGui();

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}

