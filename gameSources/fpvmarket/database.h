#pragma once
#include <sqlite3.h>
#include <vector>
#include <string>

struct PlayerInfo {
	float balance;
};
struct PlayerContext {
	std::vector<PlayerInfo> players;
};
extern sqlite3* db;

int callbackPlayer(void* data, int argc, char** argv, char** colName);
void createDb(const std::string name = "playerInfo.db");
bool dbIsExists(const std::string name = "playerInfo.db");
void saveDataForPlayer(float balance, std::string scoreOperation);
PlayerContext getDataForPlayer();
