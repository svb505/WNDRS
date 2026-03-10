#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_uefi.h"

class uefi : public QMainWindow
{
    Q_OBJECT

public:
    uefi(QWidget *parent = nullptr);
    ~uefi();

private:
    Ui::uefiClass ui;
};

