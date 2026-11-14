#pragma once

#include <windows.h>
#include <psapi.h>
#include <iostream>
#include <vector>
#include <format>

#pragma comment(lib, "psapi.lib")

class Profiler {
public:
    static SIZE_T getRAM();
    static SIZE_T getCPU();
    static std::vector<std::string> getMemoryUsage();
};
