#include <array>
#include <memory>
#include <QWidget>
#include <QPushButton>
#include <QFormLayout>
#include <QColorDialog>
#include "OpenGLW.h"
#include "Settings.h"
#include <QComboBox>
#include <QDoubleSpinBox>

void Settings::openWindow(OpenGLWidget* ogl) {
    auto colorBg = std::make_shared<std::array<float, 3>>(std::array<float, 3>{0.1f, 0.1f, 0.15f});
    auto textColor = std::make_shared<std::array<float, 3>>(std::array<float, 3>{1.0f, 1.0f, 1.0f});

    QWidget* win = new QWidget();
    win->setWindowTitle("Настройки");
    win->show();

    QFormLayout* layout = new QFormLayout(win);

    QPushButton* btnColor3 = new QPushButton("Цвет заднего фона");
    layout->addRow(btnColor3);

    QColorDialog* dialog3 = new QColorDialog(win);
    dialog3->hide();

    QObject::connect(btnColor3, &QPushButton::clicked,
        [dialog3]() {
            dialog3->show();
        });

    QObject::connect(dialog3, &QColorDialog::currentColorChanged,
        [colorBg](const QColor& c) {
            (*colorBg)[0] = c.redF();
            (*colorBg)[1] = c.greenF();
            (*colorBg)[2] = c.blueF();
        });

    QPushButton* btnColor4 = new QPushButton("Цвет текста");
    layout->addRow(btnColor4);

    QColorDialog* dialog4 = new QColorDialog(win);
    dialog4->hide();

    QObject::connect(btnColor4, &QPushButton::clicked,
        [dialog4]() {
            dialog4->show();
        });

    QObject::connect(dialog4, &QColorDialog::currentColorChanged,
        [textColor](const QColor& c) {
            (*textColor)[0] = c.redF();
            (*textColor)[1] = c.greenF();
            (*textColor)[2] = c.blueF();
        });

    QComboBox* lvl = new QComboBox();
    lvl->addItem("1 Уровень");
    lvl->addItem("2 Уровень");
    lvl->addItem("3 Уровень");
    lvl->setCurrentIndex(ogl->level - 1);
    layout->addRow(lvl);

    QLabel* lbl = new QLabel("Скорость камеры");
    layout->addRow(lbl);

    QDoubleSpinBox* camSpeed = new QDoubleSpinBox();
    camSpeed->setRange(1.0f, 10.0f);
    camSpeed->setSingleStep(0.5f);
    layout->addRow(camSpeed);

    QPushButton* applyBtn = new QPushButton("Применить");
    layout->addRow(applyBtn);

    QObject::connect(applyBtn, &QPushButton::clicked,
        [ogl, colorBg, textColor, lvl, camSpeed]() {
            ogl->setConfig(colorBg->data(), textColor->data(), lvl->currentIndex() + 1, camSpeed->value());
        });

}