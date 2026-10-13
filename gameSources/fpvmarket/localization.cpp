#include "localization.h"
#include <fstream>
#include <nlohmann//json.hpp>
#include "variables.h"

void getLangJson() {
	std::ifstream file("lang.json");

	file >> lang;
}