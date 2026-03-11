#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_LimitWin.h"

class LimitWin : public QMainWindow
{
    Q_OBJECT

public:
    LimitWin(QWidget *parent = nullptr);
    ~LimitWin();

private:
    Ui::LimitWinClass ui;
};

