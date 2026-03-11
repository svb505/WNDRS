/********************************************************************************
** Form generated from reading UI file 'LimitWin.ui'
**
** Created by: Qt User Interface Compiler version 6.9.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_LIMITWIN_H
#define UI_LIMITWIN_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_LimitWinClass
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *LimitWinClass)
    {
        if (LimitWinClass->objectName().isEmpty())
            LimitWinClass->setObjectName("LimitWinClass");
        LimitWinClass->resize(600, 400);
        menuBar = new QMenuBar(LimitWinClass);
        menuBar->setObjectName("menuBar");
        LimitWinClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(LimitWinClass);
        mainToolBar->setObjectName("mainToolBar");
        LimitWinClass->addToolBar(mainToolBar);
        centralWidget = new QWidget(LimitWinClass);
        centralWidget->setObjectName("centralWidget");
        LimitWinClass->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(LimitWinClass);
        statusBar->setObjectName("statusBar");
        LimitWinClass->setStatusBar(statusBar);

        retranslateUi(LimitWinClass);

        QMetaObject::connectSlotsByName(LimitWinClass);
    } // setupUi

    void retranslateUi(QMainWindow *LimitWinClass)
    {
        LimitWinClass->setWindowTitle(QCoreApplication::translate("LimitWinClass", "LimitWin", nullptr));
    } // retranslateUi

};

namespace Ui {
    class LimitWinClass: public Ui_LimitWinClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_LIMITWIN_H
