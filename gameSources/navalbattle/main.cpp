#include <GLFW/glfw3.h>
#include <iostream>
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include <format>
#include "field.h"
#include "text.h"
#include "GUI.h"
#include <string>

#define ECRANW 1100
#define ECRANH 500

bool gameStarted = false;

GUI gui;

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}

inline bool isPressed(GLFWwindow* w, int key, bool& prev) {
    bool curr = glfwGetKey(w, key) == GLFW_PRESS;
    bool result = curr && !prev;
    prev = curr;
    return result;
}

bool isDown(GLFWwindow* window, int key) {
    return glfwGetKey(window, key) == GLFW_PRESS;
}
void processInput(GLFWwindow* window) {
    if (isDown(window, GLFW_KEY_ESCAPE)) glfwSetWindowShouldClose(window, true);
}

int main(){
    if (!glfwInit()) {
        std::cout << "Failed to initialize GLFW\n";
        return -1;
    }

    GLFWwindow* window = glfwCreateWindow(ECRANW,ECRANH, "Naval Battle", NULL, NULL);

    if (!window) {
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);

    InitFont();

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-1100, 1100, -550, 550, -1, 1);    
    glMatrixMode(GL_MODELVIEW);

    double lastTime = glfwGetTime();
    double deltaTime = 0.0;

    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    Field fieldPlayer;
    fieldPlayer.setupField();   

    gui.setupGui(window);

    while (!glfwWindowShouldClose(window)) {
        double currentTime = glfwGetTime();
        deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        processInput(window);

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        gui.renderGui(gameStarted,fieldPlayer);

        ImGui::Render();

        glClear(GL_COLOR_BUFFER_BIT);

        fieldPlayer.draw();

        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    gui.destroyGui();
    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}

