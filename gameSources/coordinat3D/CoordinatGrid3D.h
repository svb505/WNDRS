#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_CoordinatGrid3D.h"

class CoordinatGrid3D : public QMainWindow
{
    Q_OBJECT

public:
    CoordinatGrid3D(QWidget *parent = nullptr);
    ~CoordinatGrid3D();

private:
    Ui::CoordinatGrid3DClass ui;
};

