#include "localization.h"
#include <fstream>
#include <nlohmann//json.hpp>
#include "variables.h"
#include "logger.h"
#include <format>

void getLangJson() {
	std::ifstream file("lang.json");

	file >> lang;
}
std::string returnStringFromLang(std::string key) {
    if (!lang.contains(currLang)) {
        LOG_ERROR(std::format("[LANG ERROR] Language not found: {}",currLang));
        return key;
    }

    if (!lang[currLang].contains(key)) {
        LOG_ERROR(std::format("[LANG ERROR] Key not found: {}",key));
        return key;
    }
    return lang[currLang][key].get<std::string>();
}