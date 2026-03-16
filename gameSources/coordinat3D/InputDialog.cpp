#include "InputDialog.h"
#include <QSpinBox>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QDoubleSpinBox>
#include <QLabel>
#include <QPushButton>
#include <QGridLayout>
#include <QVBoxLayout>
#include <QHBoxLayout>

InputDialog::InputDialog(QWidget* parent): QDialog(parent)
{
    setWindowTitle("Введите значения");

    spin1 = new QDoubleSpinBox(this);
    spin2 = new QDoubleSpinBox(this);
    spin3 = new QDoubleSpinBox(this);

    spin1->setRange(-10.0, 10.0);
    spin2->setRange(-10.0, 10.0);
    spin3->setRange(-10.0, 10.0);

    spin1->setDecimals(1);
    spin2->setDecimals(1);
    spin1->setSingleStep(0.5);
    spin2->setSingleStep(0.5);
    spin3->setSingleStep(0.5);
    spin3->setSingleStep(0.5);

    QLabel* label1 = new QLabel("X:", this);
    QLabel* label2 = new QLabel("Y:", this);
    QLabel* label3 = new QLabel("Z:", this);

    QPushButton* okBtn = new QPushButton("OK", this);
    QPushButton* cancelBtn = new QPushButton("Отмена", this);

    QObject::connect(okBtn, &QPushButton::clicked, this, &QDialog::accept);
    QObject::connect(cancelBtn, &QPushButton::clicked, this, &QDialog::reject);

    QGridLayout* grid = new QGridLayout;
    grid->addWidget(label1, 0, 0);
    grid->addWidget(spin1, 0, 1);
    grid->addWidget(label2, 1, 0);
    grid->addWidget(spin2, 1, 1);
    grid->addWidget(label3, 2, 0);
    grid->addWidget(spin3, 2, 1);

    QHBoxLayout* buttons = new QHBoxLayout;
    buttons->addStretch();
    buttons->addWidget(okBtn);
    buttons->addWidget(cancelBtn);

    QVBoxLayout* mainLayout = new QVBoxLayout(this);
    mainLayout->addLayout(grid);
    mainLayout->addLayout(buttons);

    connect(okBtn, &QPushButton::clicked, this, [this]() {
        emit acceptedValues(spin1->value(),spin2->value(),spin3->value());
        close();
    });

}

int InputDialog::firstValue() const { return spin1->value(); }
int InputDialog::secondValue() const { return spin2->value(); }
int InputDialog::thirtValue() const { return spin3->value(); }
