#include "DataBase.h"
#include <QSqlDatabase>
#include <QSqlError>
#include <QDebug>
#include <QSqlQuery>

void createDb() {
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("game.db");
    if (!db.open()) {
        qDebug() << "OPEN ERROR:" << db.lastError().text();
        return;
    }

    QSqlQuery query;
    if (!query.exec(R"(
        CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    score INTEGER,
    date TEXT
        );

    )")) {
        qDebug() << "CREATE TABLE ERROR:" << query.lastError().text();
    }
}
void addData(std::string name, int score, std::string date) {
    QSqlQuery query;
    query.prepare(R"(
        INSERT OR IGNORE INTO players (name, score, date)
        VALUES (?, ?, ?)
    )");
    query.addBindValue(QString::fromStdString(name));
    query.addBindValue(score);
    query.addBindValue(QString::fromStdString(date));

    if (!query.exec()) {
        qDebug() << query.lastError().text();
    }
}
void readData() {
    QSqlQuery query;
    query.exec("SELECT id, name, score, date FROM players");

    while (query.next()) {
        int id = query.value(0).toInt();
        QString name = query.value("name").toString();
        int score = query.value("score").toInt();
        QString date = query.value("date").toString();
    }
}
void updateData(int score, const std::string& name, const std::string& date) {
    QSqlQuery query;
    query.prepare(R"(UPDATE players SET score = score + ?, date = ? WHERE name = ?)");

    query.addBindValue(score);
    query.addBindValue(QString::fromStdString(date));
    query.addBindValue(QString::fromStdString(name));

    if (!query.exec()) {
        qDebug() << "UPDATE ERROR:" << query.lastError().text();
    }
}



