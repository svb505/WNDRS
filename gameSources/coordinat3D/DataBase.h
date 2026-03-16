#pragma once
#include <string>

void createDb();
void addData(std::string name, int score, std::string date);
void readData();
void updateData(int score, const std::string& name, const std::string& date);
