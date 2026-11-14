#pragma once
#include <string>
#include <map>

void changePlayerConfig(const std::string key, const bool value, std::string path = "droneNames.json");
void changePlayerConfig(const std::string key, const std::string value, std::string path = "droneNames.json");
std::string getStringFromJson(std::string key, std::string path = "droneNames.json");
bool getBoolFromJson(std::string key, std::string path = "config.json");