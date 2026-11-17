#include "LoadingWin.h"
#include "text.h"
#include "variables.h"

void LoadingScreen::Show(GLFWwindow* window, const char* text){
    int width, height;
    glfwGetFramebufferSize(window, &width, &height);

    glViewport(0, 0, width, height);

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    RenderTextHUD(width / 2, height / 2,1.0f,1.0f, 1.0f,text,ECRAN_W,ECRAN_H);

    glfwSwapBuffers(window);
    glfwPollEvents();
}