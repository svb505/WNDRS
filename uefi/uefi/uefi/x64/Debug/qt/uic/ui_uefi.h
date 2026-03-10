/********************************************************************************
** Form generated from reading UI file 'uefi.ui'
**
** Created by: Qt User Interface Compiler version 6.9.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_UEFI_H
#define UI_UEFI_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_uefiClass
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *uefiClass)
    {
        if (uefiClass->objectName().isEmpty())
            uefiClass->setObjectName("uefiClass");
        uefiClass->resize(600, 400);
        menuBar = new QMenuBar(uefiClass);
        menuBar->setObjectName("menuBar");
        uefiClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(uefiClass);
        mainToolBar->setObjectName("mainToolBar");
        uefiClass->addToolBar(mainToolBar);
        centralWidget = new QWidget(uefiClass);
        centralWidget->setObjectName("centralWidget");
        uefiClass->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(uefiClass);
        statusBar->setObjectName("statusBar");
        uefiClass->setStatusBar(statusBar);

        retranslateUi(uefiClass);

        QMetaObject::connectSlotsByName(uefiClass);
    } // setupUi

    void retranslateUi(QMainWindow *uefiClass)
    {
        uefiClass->setWindowTitle(QCoreApplication::translate("uefiClass", "uefi", nullptr));
    } // retranslateUi

};

namespace Ui {
    class uefiClass: public Ui_uefiClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_UEFI_H
