#pragma once
#include <GLFW/glfw3.h>

class LoadingScreen
{
public:
    static void Show(GLFWwindow* window, const char* text);
};