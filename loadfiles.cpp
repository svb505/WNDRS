// filelist.cpp
#include "filelist.h"
#include <string>
#include <vector>
#include <filesystem>
#include <sstream>

using namespace std;
namespace fs = std::filesystem;

// Вернёт JSON-строку со списком файлов
extern "C" __declspec(dllexport) int GetFiles(const char* path, char* buffer, int bufferSize) {
    try {
        fs::path p(path);
        if (!fs::exists(p)) return -1;

        ostringstream out;
        out << "[";

        bool first = true;
        for (auto& entry : fs::directory_iterator(p)) {
            if (!first) out << ",";
            first = false;

            string name = entry.path().filename().string();
            string ext = entry.path().extension().string();
            bool isDir = fs::is_directory(entry);
            uintmax_t size = isDir ? 0 : fs::file_size(entry);

            out << "{"
                << "\"name\":\"" << name << "\","
                << "\"ext\":\"" << ext << "\","
                << "\"isdir\":" << (isDir ? "true" : "false") << ","
                << "\"size\":" << size
                << "}";
        }

        out << "]";
        string result = out.str();

        if (result.size() + 1 > (size_t)bufferSize) {
            return -2; // буфер мал
        }

        strcpy_s(buffer, bufferSize, result.c_str());
        return 0; // успех
    }
    catch (...) {
        return -3;
    }
}
