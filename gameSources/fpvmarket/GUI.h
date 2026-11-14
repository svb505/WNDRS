#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#define GLFW_INCLUDE_NONE
#include <GLFW/glfw3.h>
#include "variables.h"
#include "drone.h"
#include <algorithm>
#include "database.h"
#include "jsonParcer.h"
#include <algorithm>
#include <iostream>
#include "days.h"
#include "avgRating.h"
#include "localization.h"
#include "profiler.h"

class GUI {
private:
	static constexpr float kBestMarkup = 0.30f;

	char bufNameAch[256]{};
	char bufNameAs[256]{};

	std::vector<std::string> card = {};

	bool showPerformance = false;
	bool showPrices = false;
	bool showNames = false;
	bool showDev = false;
	bool showOther = false;

	float minValue = 0.0f;
	float maxValue = 2000.0f;

	int idxLang = 0;
	std::vector<const char*> langs = { "FR","EN","RU" };

	const ImVec4 colGreen = ImVec4(0.30f, 0.85f, 0.45f, 1.0f);
	const ImVec4 colRed = ImVec4(0.95f, 0.35f, 0.35f, 1.0f);
	const ImVec4 colYellow = ImVec4(1.00f, 0.80f, 0.30f, 1.0f);
	const ImVec4 colAccent = ImVec4(0.40f, 0.70f, 1.00f, 1.0f);
	const ImVec4 colDim = ImVec4(0.60f, 0.60f, 0.65f, 1.0f);

	static float getCost(const std::string& key,FPVDrone& drone) {
		const auto& prices = drone.getEquipPrice();
		auto it = prices.find(key);
		return it != prices.end() ? it->second : 0.0f;
	}
	static bool colorButton(const char* label, const ImVec4& base, const ImVec2& size) {
		ImGui::PushStyleColor(ImGuiCol_Button, base);
		ImGui::PushStyleColor(ImGuiCol_ButtonHovered, ImVec4(base.x + 0.12f, base.y + 0.12f, base.z + 0.12f, 1.0f));
		ImGui::PushStyleColor(ImGuiCol_ButtonActive, ImVec4(base.x * 0.7f, base.y * 0.7f, base.z * 0.7f, 1.0f));
		bool pressed = ImGui::Button(label, size);
		ImGui::PopStyleColor(3);
		return pressed;
	}
	void priceSlider(const char* title, const char* id, float& price, float cost, float minV, float maxV){
		const float best = std::clamp(cost * (1.0f + kBestMarkup), minV, maxV);
		const float markup = cost > 0.0f ? (price - cost) / cost * 100.0f : 0.0f;

		ImGui::TextColored(colDim, "%s", title);

		// Себестоимость / цена / наценка
		ImGui::Text("%s: %.0f  |  %s: %.0f  |  %s: %+.1f%%",
			returnStringFromLang("COST_PRICE").c_str(), cost,
			returnStringFromLang("SELL_PRICE").c_str(), price,
			returnStringFromLang("MARKUP").c_str(), markup);

		// Слайдер; в тексте на самом слайдере — лучшая цена
		const std::string fmt = std::format("%.0f   ({}: {:.0f})", lang[currLang]["BEST_PRICE"].get<std::string>().c_str(), best);
		ImGui::SliderFloat(id, &price, minV, maxV, fmt.c_str());

		// Маркер лучшей цены на шкале слайдера
		const ImVec2 rmin = ImGui::GetItemRectMin();
		const ImVec2 rmax = ImGui::GetItemRectMax();
		const float grab = ImGui::GetStyle().GrabMinSize;
		const float t = (maxV > minV) ? (best - minV) / (maxV - minV) : 0.0f;
		const float x = rmin.x + grab * 0.5f + t * ((rmax.x - rmin.x) - grab);

		ImDrawList* dl = ImGui::GetWindowDrawList();
		const ImU32 col = IM_COL32(80, 220, 120, 255);
		dl->AddLine(ImVec2(x, rmin.y), ImVec2(x, rmax.y), col, 2.0f);
		dl->AddTriangleFilled(ImVec2(x - 4, rmin.y - 5), ImVec2(x + 4, rmin.y - 5),
			ImVec2(x, rmin.y), col);

		ImGui::Spacing();
	}

	void sectionTitle(const char* title) {
		ImGui::Spacing();
		ImGui::TextColored(colAccent, "%s", title);
		ImGui::Separator();
		ImGui::Spacing();
	}
	void componentText(const char* text, int current, int required) {
		bool done = current >= required;

		if (done) ImGui::PushStyleColor(ImGuiCol_Text, colGreen);

		ImGui::Text("%s %d / %d", text, current, required);

		if (done) ImGui::PopStyleColor();

		float frac = required > 0 ? static_cast<float>(current) / required : 1.0f;

		frac = std::clamp(frac, 0.0f, 1.0f);

		ImGui::PushStyleColor(ImGuiCol_PlotHistogram,done ? colGreen : colAccent);

		ImGui::ProgressBar(frac, ImVec2(-FLT_MIN, 6.0f), "");
		ImGui::PopStyleColor();
		ImGui::Spacing();
	}

	static void pushStyle() {
		ImGui::PushStyleVar(ImGuiStyleVar_WindowRounding, 10.0f);
		ImGui::PushStyleVar(ImGuiStyleVar_FrameRounding, 6.0f);
		ImGui::PushStyleVar(ImGuiStyleVar_GrabRounding, 6.0f);
		ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(14.0f, 12.0f));
		ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(8.0f, 5.0f));
		ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, ImVec2(8.0f, 7.0f));
	}
	static void popStyle() { ImGui::PopStyleVar(6); }

	bool windowToggle(const char* label, bool& state) {
		const ImVec4 base = state ? ImVec4(0.20f, 0.55f, 0.35f, 1.0f) : ImVec4(0.25f, 0.28f, 0.35f, 1.0f);
		bool pressed = colorButton(label, base, ImVec2(-FLT_MIN, 0.0f));
		if (pressed) state = !state;
		return pressed;
	}

	CompType type;
	bool buyingWin = false;

public:
	GUI() {
		for (int i = 0; i < langs.size(); i++) {
			if (std::strcmp(langs[i], currLang.c_str()) == 0) {
				idxLang = i;
				break;
			}
		}
	}
	void destroyGui() {
		ImGui_ImplOpenGL3_Shutdown();
		ImGui_ImplGlfw_Shutdown();
		ImGui::DestroyContext();
	}
	void setupGui(GLFWwindow* window) {
		IMGUI_CHECKVERSION();
		ImGui::CreateContext();

		ImGuiIO& io = ImGui::GetIO();

		ImFont* font = io.Fonts->AddFontFromFileTTF(
			"res/ARIAL.ttf",
			18.0f,
			nullptr,
			io.Fonts->GetGlyphRangesCyrillic()
		);

		if (!font) {
			std::cout << "ERROR: Failed to load res/ARIAL.ttf\n";
			io.Fonts->AddFontDefault();
		}

		ImGui::StyleColorsDark();

		ImGui_ImplGlfw_InitForOpenGL(window, true);
		ImGui_ImplOpenGL3_Init("#version 330");
	}

	void renderOtherWindow(Building& build) {
		if (!showOther) return;

		pushStyle();
		ImGui::SetNextWindowPos(ImVec2(250.0f, 10.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(540.0f, 140.0f), ImGuiCond_FirstUseEver);

		if (ImGui::Begin(returnStringFromLang("OTHER").c_str(), &showOther)) {
			ImGui::PushItemWidth(-FLT_MIN);

			if (!build.isSecuritySystem()) {
				ImGui::TextColored(colDim, std::format("{} {}$", returnStringFromLang("BUY_SEC_SYS").c_str(),
					build.getSecuritySystemPrice()).c_str());

				if (colorButton(returnStringFromLang("BUY_ALL").c_str(),
					ImVec4(0.20f, 0.50f, 0.80f, 1.0f), ImVec2(-FLT_MIN, 0.0f))) {

					if (myBalance >= build.getSecuritySystemPrice()) {
						myBalance -= build.getSecuritySystemPrice();

						saveDataForPlayer(build.getSecuritySystemPrice(), averageRating(),
							"-");

						build.setSecuritySystem(true);
					}
				}
			}
			else {
				ImGui::TextColored(colDim, returnStringFromLang("SEC_SYS_BUYED").c_str());
			}

			ImGui::PopItemWidth();
		}

		ImGui::End();
		popStyle();
	}
	void renderBalanceRatingWindow() {
		pushStyle();

		ImGui::SetNextWindowPos(ImVec2(800.0f, 5.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(150.0f, 160.0f), ImGuiCond_FirstUseEver);
		if (ImGui::Begin("INFO",nullptr, ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoCollapse)) {
			ImVec4 color;
			float rating = 0.0f;
			std::string dayString = returnStringFromLang("DAY");
			std::string sallesForDayString = returnStringFromLang("SALES_FOR_DAY");

			if (!ratings.empty()) {
				for (float r : ratings) rating += r;

				rating /= static_cast<float>(ratings.size());
			}

			if (rating > 4.0) color = colGreen;
			else if (rating > 3.0f && rating < 4.0f) color = colYellow;
			else color = colRed;

			ImGui::Spacing();
			

			ImGui::Text(std::format("{}: {} - {}:{:.0f}", dayString, day, heure, seconds).c_str());
			ImGui::Dummy({ 0.0f, 10.0f });

			ImGui::Text(std::format("{}: {}", sallesForDayString, sallesForDay).c_str());
			ImGui::Dummy({ 0.0f, 10.0f });

			ImGui::Text(returnStringFromLang("CHECK").c_str());
			ImGui::SameLine();

			ImGui::TextColored(colYellow, "%.1f $", myBalance);
			ImGui::Spacing();

			ImGui::Text(returnStringFromLang("RATING").c_str());
			ImGui::SameLine();
			ImGui::TextColored(color, "%.1f", rating);

			ImGui::Dummy({ 0.0f, 10.0f });
			ImGui::Text(std::format("{}: {}", returnStringFromLang("LEVEL"), level).c_str());
			ImGui::Dummy({ 0.0f, 10.0f });
			ImGui::Text(std::format("{}: {}", returnStringFromLang("PURCHASES"),purchasesForAllTime).c_str());
		}

		ImGui::End();
		popStyle();
	}
	void renderMainWindow(FPS& fps, FPVDrone& drone, BuildingSettings& build) {
		auto comp = drone.getComp();

		pushStyle();

		ImGui::SetNextWindowPos(ImVec2(10.0f, 10.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(350.0f, 720.0f), ImGuiCond_FirstUseEver);
		ImGui::Begin(returnStringFromLang("MAIN_WIN").c_str());

		ImGui::Checkbox(returnStringFromLang("OPEN_STORE").c_str(), &isOpen);

		sectionTitle(returnStringFromLang("WINDOWS").c_str());
		const float spacing = ImGui::GetStyle().ItemSpacing.x;
		const float third = (ImGui::GetContentRegionAvail().x - spacing * 2.0f) / 3.0f;

		{
			auto toggleSmall = [&](const char* label, bool& state, bool sameLine) {
				if (sameLine) ImGui::SameLine();
				const ImVec4 base = state ? ImVec4(0.20f, 0.55f, 0.35f, 1.0f) : ImVec4(0.25f, 0.28f, 0.35f, 1.0f);
				if (colorButton(label, base, ImVec2(third, 0.0f))) state = !state;
			};
			toggleSmall(returnStringFromLang("PERF").c_str(), showPerformance, false);
			toggleSmall(returnStringFromLang("PRICE").c_str(), showPrices, true);
			toggleSmall(returnStringFromLang("NAMES").c_str(), showNames, true);
			toggleSmall(returnStringFromLang("OTHER").c_str(), showOther, false);

			if (getBoolFromJson("DEVMODE"))
				toggleSmall("DEV WINDOW", showDev, false);
		}

		ImGui::BeginDisabled(!drone.getPlacedEquip().empty() || canTakeObj);

		if (ImGui::Combo(returnStringFromLang("SLCT_LANG").c_str(), &idxLang, langs.data(), langs.size())) {
			currLang = langs[idxLang];
			changePlayerConfig("CURR_LANG", currLang, "config.json");
			drone.reInitListes();
		}

		ImGui::EndDisabled();

		if (ImGui::CollapsingHeader(returnStringFromLang("WIN_COMM").c_str())) {
			if (ImGui::Button("TYPE1")) {
				buyingWin = true;
				type = CompType::TYPE1;
			}

			ImGui::BeginDisabled(level < 2);
			if (ImGui::Button("TYPE2")) {
				buyingWin = true;
				type = CompType::TYPE2;
			}
			ImGui::EndDisabled();

			ImGui::BeginDisabled(level < 3);
			if (ImGui::Button("TYPE3")) {
				buyingWin = true;
				type = CompType::TYPE3;
			}
			ImGui::EndDisabled();

		}

		sectionTitle(returnStringFromLang("ASSEMBLE").c_str());

		componentText(returnStringFromLang("FRAME").c_str(),
			comp.frame,1);
		componentText(returnStringFromLang("CAM").c_str(), comp.camera, 1);
		componentText(returnStringFromLang("BAT").c_str(), comp.battery, 1);
		componentText(returnStringFromLang("MOTOR").c_str(), comp.motor, 4);
		componentText(returnStringFromLang("PROPELLER").c_str(), comp.propeller, 4);
		componentText(returnStringFromLang("FC").c_str(),comp.fc, 1);

		ImGui::Dummy({ 0.0f, 10.0f });
		ImGui::Text("©Developped by SVB & Red.Fpv");

		ImGui::End();

		popStyle();
	}
	void renderBuyingWindow(FPVDrone& drone, BuildingSettings& build, const float& spacing) {
		if (!buyingWin) return;
		
		pushStyle();
		
		ImGui::SetNextWindowPos(ImVec2(100.0f, 10.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(350.0f, 650.0f), ImGuiCond_FirstUseEver);

		if (ImGui::Begin(returnStringFromLang("WIN_COMM").c_str(), &buyingWin)) {
			auto equip = drone.getEquipPrice();

			ImGui::Text(returnStringFromLang("PROD_IN_CARD").c_str());
			ImGui::SameLine();
			ImGui::TextColored(card.empty() ? colDim : colGreen, "%d", (int)card.size());

			ImGui::Spacing();
			ImGui::Separator();
			ImGui::Spacing();

			ImGui::Spacing();
			ImGui::Separator();
			ImGui::Spacing();

			const float btnWidth = (ImGui::GetContentRegionAvail().x - spacing) * 0.5f;

			for (const auto& [key, value] : equip) {
				const auto& typeComponents = drone.getEquipTypes()[type];

				if (std::ranges::find(typeComponents, key) == typeComponents.end()) continue;

				ImGui::PushID(key.c_str());

				ImGui::ImageButton(key.c_str(), (ImTextureID)(intptr_t)drone.returnCompPreview(key),
					ImVec2(60, 60));

				if (std::ranges::find(card, key) != card.end()) ImGui::TextColored(colGreen, "%s - %.1f$", key.c_str(), value);
				else ImGui::Text("%s - %.1f$", key.c_str(), value);

				if (colorButton(
					std::format("{}##{}", returnStringFromLang("ADD_TO_CARD"), key).c_str(),
					ImVec4(0.10f, 0.60f, 0.25f, 1.0f), ImVec2(btnWidth, 0.0f))) {
					card.push_back(key);
				}

				ImGui::SameLine();

				if (colorButton(std::format("{}##{}", returnStringFromLang("DELETE_FROM_CARD"),
					key).c_str(), ImVec4(0.75f, 0.15f, 0.15f, 1.0f), ImVec2(btnWidth, 0.0f))) {
					card.erase(std::remove(card.begin(), card.end(), key), card.end());
				}

				ImGui::PopID();
				ImGui::Spacing();
			}

			if (colorButton(returnStringFromLang("BUY_ALL").c_str(), ImVec4(0.15f, 0.45f, 0.85f, 1.0f), ImVec2(-FLT_MIN, 32.0f))) {
				float totalPrice = 0.0f;

				for (auto& element : card) totalPrice += equip[element];

				if (myBalance >= totalPrice) {

					saveDataForPlayer(totalPrice, averageRating(), "-");

					for (auto& p : getDataForPlayer().players) myBalance = p.balance;

					drone.sendPackage(card, build);
					card.clear();
				}
				else ImGui::TextColored(colRed, returnStringFromLang("NOT_ENOUGH_MONEY").c_str());
			}
			ImGui::Spacing();
		}
		ImGui::End();
		popStyle();
	}
	void renderPerformanceWindow(FPS& fps) {
		if (!showPerformance) return;

		pushStyle();
		ImGui::SetNextWindowPos(ImVec2(380.0f, 10.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(260.0f, 140.0f), ImGuiCond_FirstUseEver);

		if (ImGui::Begin(returnStringFromLang("PERF").c_str(), &showPerformance)) {
			ImVec4 fpsColor = fps.fps >= 60.0f ? colGreen : (fps.fps >= 30.0f ? colYellow : colRed);

			ImGui::Text(std::format("{}: % .0f", returnStringFromLang("MIN_FPS")).c_str(), fps.minFps);
			ImGui::Text(std::format("{}: % .0f", returnStringFromLang("MAX_FPS")).c_str(), fps.maxFps);
			ImGui::PushStyleColor(ImGuiCol_Text, fpsColor);
			ImGui::Text(std::format("{}: % .0f", returnStringFromLang("CURR_FPS")).c_str(), fps.fps);
			ImGui::PopStyleColor();
		}
		ImGui::End();
		popStyle();
	}
	void renderDevWindow() {
		if (!showDev) return;

		pushStyle();
		ImGui::SetNextWindowPos(ImVec2(380.0f, 10.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(260.0f, 140.0f), ImGuiCond_FirstUseEver);

		if (ImGui::Begin("DEV Window", nullptr)) {
			for (const auto& line : Profiler::getMemoryUsage()) ImGui::Text("%s", line.c_str());
		}

		ImGui::End();
		popStyle();
	}
	void renderPricesWindow(FPVDrone& drone) {
		if (!showPrices) return;

		pushStyle();
		ImGui::SetNextWindowPos(ImVec2(380.0f, 170.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(340.0f, 460.0f), ImGuiCond_FirstUseEver);

		if (ImGui::Begin(returnStringFromLang("PRICE").c_str())) {
			sectionTitle(returnStringFromLang("PRICE_OF_DRONE").c_str());

			ImGui::Text("%s", std::format("{} {} {:.0f}", getStringFromJson("DRONE_Achetee"),
				returnStringFromLang("PRICE"), priceForT1).c_str());

			ImGui::Text("%s", std::format("{} {} {:.0f}", getStringFromJson("DRONE_Assemblee"),
				returnStringFromLang("PRICE"), priceForT2).c_str());

			sectionTitle(returnStringFromLang("SETTING_OF_PRICE").c_str());

			ImGui::PushItemWidth(-FLT_MIN);

			priceSlider(returnStringFromLang("ENTER_PRICE_FOR_DRN_BUY").c_str(),
				"##p1", priceForT1, getCost(drone.getBaseEquip()[7], drone), minValue, maxValue);

			ImGui::TextColored(colDim, "%s", returnStringFromLang("ENTER_PRICE_FOR_DRN_ASSEMBLE").c_str());
			ImGui::InputFloat("2##", &priceForT2);

			priceSlider(returnStringFromLang("ENTER_PRICE_FOR_GOGGLES").c_str(),
				"##p3", priceForGoggles1, getCost(drone.getBaseEquip()[6], drone), minValue, maxValue);

			priceSlider(returnStringFromLang("ENTER_PRICE_FOR_GOGGLES2").c_str(),
				"##p4", priceForGoggles2, getCost(drone.getBaseEquip()[15], drone), minValue, maxValue);

			priceSlider(returnStringFromLang("ENTER_PRICE_FOR_CONTROLLER").c_str(),
				"##p5", priceForController1, getCost(drone.getBaseEquip()[5], drone), minValue, maxValue);

			priceSlider(returnStringFromLang("ENTER_PRICE_FOR_CONTROLLER2").c_str(),
				"##p6", priceForController2, getCost(drone.getBaseEquip()[14], drone), minValue, maxValue);

			priceForT2 = std::clamp(priceForT2, minValue, maxValue);

			ImGui::PopItemWidth();
		}
		ImGui::End();
		popStyle();
	}
	void renderNamesWindow() {
		if (!showNames) return;

		pushStyle();
		ImGui::SetNextWindowPos(ImVec2(740.0f, 10.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(320.0f, 250.0f), ImGuiCond_FirstUseEver);

		if (ImGui::Begin(returnStringFromLang("DRONE_NAMES").c_str(), &showNames)) {
			ImGui::PushItemWidth(-FLT_MIN);

			ImGui::TextColored(colDim, returnStringFromLang("ENTER_NAME_FOR_DRN_ASSEMBLE").c_str());
			ImGui::InputText("7##", bufNameAs, sizeof(bufNameAs));
			if (colorButton("Appliquer##", ImVec4(0.20f, 0.50f, 0.80f, 1.0f), ImVec2(-FLT_MIN, 0.0f)))
				changePlayerConfig("DRONE_Assemblee", bufNameAs);

			ImGui::Spacing();

			ImGui::TextColored(colDim, returnStringFromLang("ENTER_NAME_FOR_DRN_BUY").c_str());
			ImGui::InputText("8##", bufNameAch, sizeof(bufNameAch));
			if (colorButton("Appliquer", ImVec4(0.20f, 0.50f, 0.80f, 1.0f), ImVec2(-FLT_MIN, 0.0f)))
				changePlayerConfig("DRONE_Achetee", bufNameAch);

			ImGui::PopItemWidth();
		}
		ImGui::End();
		popStyle();
	}
	void renderAll(FPS& fps, FPVDrone& drone, BuildingSettings& buildSettings,
		Building& build) {
		renderMainWindow(fps, drone, buildSettings);
		renderPerformanceWindow(fps);
		renderPricesWindow(drone);
		renderNamesWindow();
		renderBalanceRatingWindow();
		renderOtherWindow(build);
		renderDevWindow();

		const float spacing = ImGui::GetStyle().ItemSpacing.x;

		renderBuyingWindow(drone, buildSettings, spacing);
	}
};