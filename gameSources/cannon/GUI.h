#pragma once
#include <vector>
#include <string>
#include "imgui.h"

extern int level;

class GUI {
private:
	std::vector<std::string> levels = { "1", "2" };
	std::vector<const char*> cstrs;
	int currentIndex = 0;
public:
	GUI() {
		for (auto& s : levels)
			cstrs.push_back(s.c_str());
	}
	void drawGui(int score,float reloadTime,float fps) {
		ImGui::Begin("Settings & Info");

		ImGui::Text("Score: %d", score);
		ImGui::Text("Reload: %.1f", reloadTime);
		ImGui::Text("FPS: %.0f", fps);

		if (ImGui::Combo("Select level", &currentIndex, cstrs.data(), cstrs.size())) level = std::stoi(levels[currentIndex]);

		ImGui::End();
	}
};