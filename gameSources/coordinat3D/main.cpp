#include <QApplication>
#include <QMainWindow>
#include <QSurfaceFormat>
#include "OpenGLW.h"
#include "UI.h"
#include "DataBase.h"
#include <GL/glut.h>

int main(int argc, char* argv[])
{
    glutInit(&argc, argv);
    QApplication a(argc, argv);

    UI ui;

    QSurfaceFormat format;
    format.setVersion(2, 1);
    format.setProfile(QSurfaceFormat::CompatibilityProfile);
    QSurfaceFormat::setDefaultFormat(format);

    QMainWindow window;
    window.resize(600, 600);
    window.setWindowTitle("Угадай координату    Очки: 0");
    window.setWindowIcon(QIcon(":/coordinate.png"));

    OpenGLWidget* glWidget = new OpenGLWidget(nullptr, &ui);
    window.setCentralWidget(glWidget);

    createDb();
    ui.askName(&window);

    window.show();
    return a.exec();
}
