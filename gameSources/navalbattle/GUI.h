#pragma once
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include <GLFW/glfw3.h>
#include <vector>
#include <string>
#include "field.h"

constexpr int MAX_SHIPS = 10;

class GUI {
private:
    int idxDecks = 0;
    int idxCellules = 0;
    int idxTypes = 0;

    int placedShips = 0;

    int deckCount = 0;
    std::string startCell = "";
    std::string type;

    bool canStartGame = false;

    std::vector<std::string> decks = { "1", "2", "3", "4"};
    std::vector<std::string> types = { "Horizontal", "Vertical"};
    std::vector<const char*> cstrsDecks;
    std::vector<const char*> cstrsTypes;
    std::vector<const char*> cstrsCellules;
public:
    GUI() {
        for (auto& d : decks) cstrsDecks.push_back(d.c_str());  
        for (auto& t : types) cstrsTypes.push_back(t.c_str());
    }
    void rebuildCells(Field& field){
        cstrsCellules.clear();

        const auto& map = field.getField(FieldType::Player);

        for (char letter = 'A'; letter <= 'I'; ++letter){
            for (int num = 1; num <= 10; ++num){
                std::string key = std::format("{}{}", letter, num);

                auto it = map.find(key);

                if (it != map.end() && !it->second.placedShip) cstrsCellules.push_back(it->first.c_str());
            }
        }

        bool stillValid = false;

        for (auto& s : cstrsCellules){
            if (s == startCell){
                stillValid = true;
                break;
            }
        }

        if (!stillValid) startCell.clear();
    }
    void setupGui(GLFWwindow* window) {
        IMGUI_CHECKVERSION();
        ImGui::CreateContext();
        ImGuiIO& io = ImGui::GetIO(); (void)io;

        ImGui_ImplGlfw_InitForOpenGL(window, true);
        ImGui_ImplOpenGL3_Init("#version 330");

        ImGui::StyleColorsDark();
    }
    void destroyGui() {
        ImGui_ImplOpenGL3_Shutdown();
        ImGui_ImplGlfw_Shutdown();
        ImGui::DestroyContext();
    }
    void renderGui(bool& start,Field& field) {
        if (cstrsCellules.empty()) {
            for (char letter = 'A'; letter <= 'I'; ++letter) {
                for (int num = 1; num <= 10; ++num) {
                    std::string key = std::format("{}{}", letter, num);

                    auto it = field.getField(FieldType::Player).find(key);

                    if (it != field.getField(FieldType::Player).end() && !it->second.placedShip) {
                        cstrsCellules.push_back(it->first.c_str());
                    }
                }
            }
        }
        if (placedShips == MAX_SHIPS) canStartGame = true;
        
        const char* preview = startCell.empty() ? "Select..." : startCell.c_str();

        ImGui::Begin("Naval battle");

        ImGui::Dummy(ImVec2(0.0f, 10.0f));
        ImGui::Text("Place your ships");
        ImGui::Text("Placed ships %d", placedShips);

        if (ImGui::Combo("Select deck count", &idxDecks, cstrsDecks.data(), cstrsDecks.size())) {
            deckCount = std::stoi(cstrsDecks[idxDecks]);
        }
        

        if (ImGui::BeginCombo("Select start cellule", preview)){
            for (const auto& s : cstrsCellules){
                bool selected = (startCell == s);

                if (ImGui::Selectable(s, selected)) startCell = s;
            }

            ImGui::EndCombo();
        }
        if (ImGui::Combo("Select type", &idxTypes, cstrsTypes.data(), cstrsTypes.size())) {
            type = std::string(cstrsTypes[idxTypes]);
        }

        ImGui::BeginDisabled(!(placedShips < MAX_SHIPS));
        if (ImGui::Button("Place ship")) {
            
            field.getField(FieldType::Player)[startCell].placedShip = true;
            rebuildCells(field);

            placedShips++;
        }
        ImGui::EndDisabled();

        ImGui::BeginDisabled(!canStartGame && !start);
        if (ImGui::Button("Start game")) start = true;
        ImGui::EndDisabled();


        ImGui::End();
    }
};



