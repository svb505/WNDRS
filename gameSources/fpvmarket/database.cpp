#include "database.h"
#include <sqlite3.h>
#include <filesystem>
#include <vector>
#include <string>

sqlite3* db;

int callbackPlayer(void* data, int argc, char** argv, char** colName) {
	PlayerContext* ctx = static_cast<PlayerContext*>(data);
	PlayerInfo p;

	p.balance = std::stoi(argv[1]);

	ctx->players.push_back(p);
}
bool dbIsExists(const std::string name) {
	return std::filesystem::exists(name);
}
void createDb(const std::string name) {
	std::string createQuery;
	std::string insertQuery;
	char* err;

	if (sqlite3_open(name.c_str(), &db) != SQLITE_OK) return;

	createQuery = "CREATE TABLE if NOT EXISTS player(id INTEGER PRIMARY KEY,"
		"balance REAL)";
	insertQuery = "INSERT INTO player VALUES(0, 4000.0)";

	if (sqlite3_exec(db, createQuery.c_str(), nullptr, nullptr, &err) != SQLITE_OK) {
		sqlite3_free(err);
		return;
	}
	if (sqlite3_exec(db, insertQuery.c_str(), 0, 0, &err) != SQLITE_OK) {
		sqlite3_free(err);
		return;
	}
	sqlite3_close(db);
}
void saveDataForPlayer(float balance, std::string scoreOperation) {
	if (sqlite3_open("playerInfo.db", &db) != SQLITE_OK) return;
	char* sql = nullptr;

	if (scoreOperation == "+") {
		sql = sqlite3_mprintf(
			"UPDATE player SET balance = balance + %f WHERE id = 0;", balance);
	}
	else {
		sql = sqlite3_mprintf(
			"UPDATE player SET balance = balance - %f WHERE id = 0;",balance);
	}

	char* err = nullptr;

	sqlite3_exec(db, sql, nullptr, nullptr, &err);
	sqlite3_free(sql);
}
PlayerContext getDataForPlayer() {
	PlayerContext ctx;

	if (sqlite3_open("playerInfo.db", &db) != SQLITE_OK) return ctx; 
	else {
		char* err;

		sqlite3_exec(db, "SELECT * FROM player", callbackPlayer, &ctx, &err);
		sqlite3_close(db);

		return ctx;
	}

}
