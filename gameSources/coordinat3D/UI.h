#pragma once
#include <QWidget>
#include <QFormLayout>
#include <QPushButton>
#include <QLineEdit>
#include <QLabel>
#include <QMainWindow>
#include <QDialog>
#include <QSqlTableModel>
#include <QTableView>
#include <vector>

#include "date.h"
#include "DataBase.h"
class UI {
private:
    std::string userName;
    std::string upr = "W - Камера вперед\nA - Камера влево\nS - Камера назад\nD - Камера вправо\n"
        "Q - Камера вверх\nE - Камера вниз"
        "\n--------------------------------------------------\n"
        "\nC - Вид сверху\nV - Вид снизу\nB - Вид слева\nN - Вид справа\n"
        "\n--------------------------------------------------\n"
        "← - Поворот камеры влево\n→ - Поворот камеры вправо\n↑ - Наклон камеры вверх\n↓ - Наклон камеры вниз";
public:
    void askName(QMainWindow* parent) {
        QDialog* dlg = new QDialog(parent);
        dlg->setWindowTitle("Enter name");

        QFormLayout* l = new QFormLayout(dlg);

        QLabel* lbl = new QLabel("Enter your name");
        QLineEdit* name = new QLineEdit();
        QPushButton* btn = new QPushButton("Apply");

        l->addRow(lbl);
        l->addRow(name);
        l->addRow(btn);

        QObject::connect(btn, &QPushButton::clicked, [=]() {
            QDateTime time = getCurrentDate();
            QString f = getConvertedDate(time);
            userName = name->text().toStdString();
            addData(userName, 0, f.toStdString());

            dlg->accept();
            });

        dlg->exec();
    }
    void showTournament() {
        QWidget* win = new QWidget();
        win->resize(500, 400);
        QVBoxLayout* l = new QVBoxLayout(win);
        l->setParent(win);

        QTableView* tableView = new QTableView(win);

        QSqlTableModel* model = new QSqlTableModel(win);
        model->setTable("players");
        model->setSort(2, Qt::DescendingOrder);
        model->select();

        tableView->setModel(model);
        tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
        tableView->setEditTriggers(QAbstractItemView::NoEditTriggers);
        tableView->hideColumn(0);

        l->addWidget(tableView);

        win->show();

    }
    void showUpravlenie() {
        QFont font("Arial", 13, QFont::Bold); 

        QWidget* win = new QWidget();
        win->resize(500, 400);
        QFormLayout* l = new QFormLayout(win);
        l->setParent(win);

        QLabel* lbl = new QLabel();
        lbl->setText(QString::fromStdString(upr));
        lbl->setFont(font);
        l->addRow(lbl);

        win->show();
    }
    std::string getName() { return userName; }
};

