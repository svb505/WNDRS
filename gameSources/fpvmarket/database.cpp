#include "database.h"
#include "logger.h"

#include <sqlite3.h>
#include <filesystem>
#include <vector>
#include <string>
#include <iostream>
#include <format>
#include <exception>

sqlite3* db = nullptr;

int callbackPlayer(void* data, int argc, char** argv, char** colName) {
    auto* ctx = static_cast<PlayerContext*>(data);

    if (ctx == nullptr) {
        LOG_ERROR("callbackPlayer: PlayerContext is nullptr");
        return 1;
    }
    if (argc < 3) {
        LOG_ERROR(std::format("callbackPlayer: expected at least 3 columns, got {}",
            argc));
        return 1;
    }

    PlayerInfo p{};

    try {
        p.balance = argv[1] ? std::stof(argv[1]) : 0.0f;
        p.rating = argv[2] ? std::stof(argv[2]) : 0.0f;
        p.day = argv[3] ? std::stoi(argv[3]) : 0;
        p.level = argv[4] ? std::stoi(argv[4]) : 1;
        p.purchases = argv[5] ? std::stoi(argv[5]) : 0;
    }
    catch (const std::exception& e) {
        LOG_ERROR(std::format( "callbackPlayer: failed to parse player data: {}", e.what()));
        return 1;
    }

    ctx->players.push_back(p);


    return 0;
}

bool dbIsExists(const std::string name) {
    try {
        bool exists = std::filesystem::exists(name);

        std::cout << "[DB] File: " << name << ", exists=" << exists << '\n';

        return exists;
    }
    catch (const std::exception& e) {
        LOG_ERROR(std::format("dbIsExists: {}",e.what() ));
        return false;
    }
}

void createDb(const std::string name) {
    std::cout << "[DB] createDb started: " << name << '\n';

    sqlite3* localDb = nullptr;

    int rc = sqlite3_open(name.c_str(), &localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format( "createDb: sqlite3_open failed: {}",localDb ? sqlite3_errmsg(localDb) : "unknown error"));

        if (localDb) sqlite3_close(localDb);

        return;
    }

    const char* createQuery =
        "CREATE TABLE IF NOT EXISTS player("
        "id INTEGER PRIMARY KEY,"
        "balance REAL,"
        "rating REAL,"
        "day INTEGER,"
        "level INTEGER,"
        "purchases INTEGER)";

    const char* insertQuery =
        "INSERT OR IGNORE INTO player "
        "VALUES(0, 4000.0, 0.0, 0, 1, 0)";

    char* err = nullptr;

    rc = sqlite3_exec(localDb, createQuery, nullptr, nullptr, &err);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("createDb: CREATE TABLE failed: {}", err ? err : sqlite3_errmsg(localDb)));

        sqlite3_free(err);
        sqlite3_close(localDb);
        return;
    }

    sqlite3_free(err);
    err = nullptr;

    std::cout << "[DB] Table created or already exists\n";

    rc = sqlite3_exec(localDb, insertQuery, nullptr, nullptr, &err);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("createDb: INSERT failed: {}",err ? err : sqlite3_errmsg(localDb)));

        sqlite3_free(err);
        sqlite3_close(localDb);
        return;
    }

    sqlite3_free(err);

    std::cout << "[DB] Initial player inserted or already exists\n";

    sqlite3_close(localDb);

    std::cout << "[DB] createDb finished\n";
}

void saveLevelAndPurchasesToDb(int level, int purchases) {
    std::cout << "Lvl: " << level << " | Purchases: " << purchases << std::endl;

    sqlite3* localDb = nullptr;

    int rc = sqlite3_open("playerInfo.db", &localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveLevelAndPurchasesToDb: open failed: {}", localDb ? sqlite3_errmsg(localDb) : "unknown error"));

        if (localDb) sqlite3_close(localDb);

        return;
    }

    char* sql = nullptr;

    sql = sqlite3_mprintf("UPDATE player SET ""level = %d, purchases = purchases + %d ""WHERE id = 0;", level, purchases);

    if (sql == nullptr) {
        LOG_ERROR("saveLevelAndPurchasesToDb: sqlite3_mprintf failed");
        sqlite3_close(localDb);
        return;
    }

    std::cout << "[DB] SQL: " << sql << '\n';

    char* err = nullptr;

    rc = sqlite3_exec(localDb, sql, nullptr, nullptr, &err);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveLevelAndPurchasesToDb: UPDATE failed: {}", err ? err : sqlite3_errmsg(localDb)));
    }
    else {
        std::cout << "[DB] UPDATE successful. Rows changed: " << sqlite3_changes(localDb) << '\n';

        if (sqlite3_changes(localDb) == 0) {
            LOG_ERROR("saveLevelAndPurchasesToDb: no player row updated (id=0)"
            );
        }
    }

    sqlite3_free(err);
    sqlite3_free(sql);

    rc = sqlite3_close(localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveLevelAndPurchasesToDb: close failed: {}", sqlite3_errstr(rc)));
    }
}

void saveDataForPlayer(float balance, float rating, std::string scoreOperation) {
    std::cout << "[DB] saveDataForPlayer: balance=" << balance << ", rating=" << rating << ", operation=" << scoreOperation << '\n';

    sqlite3* localDb = nullptr;

    int rc = sqlite3_open("playerInfo.db", &localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format( "saveDataForPlayer: open failed: {}",localDb ? sqlite3_errmsg(localDb) : "unknown error"));

        if (localDb) sqlite3_close(localDb);

        return;
    }

    char* sql = nullptr;

    if (scoreOperation == "+") {
        sql = sqlite3_mprintf("UPDATE player SET ""balance = balance + %f, rating = %f ""WHERE id = 0;",balance, rating);
    }
    else {
        sql = sqlite3_mprintf("UPDATE player SET ""balance = balance - %f, rating = %f ""WHERE id = 0;",balance, rating);
    }

    if (sql == nullptr) {
        LOG_ERROR("saveDataForPlayer: sqlite3_mprintf failed");
        sqlite3_close(localDb);
        return;
    }

    std::cout << "[DB] SQL: " << sql << '\n';

    char* err = nullptr;

    rc = sqlite3_exec(localDb, sql, nullptr, nullptr, &err);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveDataForPlayer: UPDATE failed: {}", err ? err : sqlite3_errmsg(localDb)));
    }
    else {
        std::cout << "[DB] UPDATE successful. Rows changed: " << sqlite3_changes(localDb) << '\n';

        if (sqlite3_changes(localDb) == 0) {
            LOG_ERROR( "saveDataForPlayer: no player row updated (id=0)"
            );
        }
    }

    sqlite3_free(err);
    sqlite3_free(sql);

    rc = sqlite3_close(localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveDataForPlayer: close failed: {}",sqlite3_errstr(rc)));
    }
}
void saveDayToDb(int day) {
    sqlite3* localDb = nullptr;

    int rc = sqlite3_open("playerInfo.db", &localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveDataForPlayer: open failed: {}", localDb ? sqlite3_errmsg(localDb) : "unknown error"));

        if (localDb) sqlite3_close(localDb);

        return;
    }

    char* sql = nullptr;

    sql = sqlite3_mprintf("UPDATE player SET day = %d WHERE id = 0;", day);


    if (sql == nullptr) {
        LOG_ERROR("saveDataForPlayer: sqlite3_mprintf failed");
        sqlite3_close(localDb);
        return;
    }

    std::cout << "[DB] SQL: " << sql << '\n';

    char* err = nullptr;

    rc = sqlite3_exec(localDb, sql, nullptr, nullptr, &err);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveDataForPlayer: UPDATE failed: {}", err ? err : sqlite3_errmsg(localDb)));
    }
    else {
        std::cout << "[DB] UPDATE successful. Rows changed: " << sqlite3_changes(localDb) << '\n';

        if (sqlite3_changes(localDb) == 0) {
            LOG_ERROR("saveDataForPlayer: no player row updated (id=0)"
            );
        }
    }

    sqlite3_free(err);
    sqlite3_free(sql);

    rc = sqlite3_close(localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("saveDataForPlayer: close failed: {}", sqlite3_errstr(rc)));
    }
}

PlayerContext getDataForPlayer() {
    PlayerContext ctx{};

    std::cout << "[DB] getDataForPlayer started\n";

    sqlite3* localDb = nullptr;

    int rc = sqlite3_open("playerInfo.db", &localDb);

    if (rc != SQLITE_OK) {
        LOG_ERROR(std::format("getDataForPlayer: open failed: {}",localDb ? sqlite3_errmsg(localDb) : "unknown error"));

        if (localDb)sqlite3_close(localDb);

        return ctx;
    }

    char* err = nullptr;

    rc = sqlite3_exec(localDb,"SELECT * FROM player",callbackPlayer,&ctx, &err);

    if (rc != SQLITE_OK)  LOG_ERROR(std::format( "getDataForPlayer: SELECT failed: {}",err ? err : sqlite3_errmsg(localDb)));

    sqlite3_free(err);

    rc = sqlite3_close(localDb);

    if (rc != SQLITE_OK)  LOG_ERROR(std::format( "getDataForPlayer: close failed: {}", sqlite3_errstr(rc)));

    return ctx;
}