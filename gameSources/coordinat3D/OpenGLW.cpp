#include "OpenGLW.h"
#include <GL/gl.h>
#include <QPainter>
#include <QMouseEvent>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include <QRandomGenerator>
#include <QString>
#include <QDateTime>
#include "InputDialog.h"
#include "date.h"
#include "Settings.h"
#include <algorithm>
#include <GL/glut.h>

void OpenGLWidget::drawText3D(float x, float y, float z, const QString& text, float R, float G, float B)
{
    glColor3f(R,G,B);
    glRasterPos3f(x, y, z);

    for (QChar c : text)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c.toLatin1());
}
void OpenGLWidget::drawAxisNumbers()
{
    glDisable(GL_DEPTH_TEST);
    glColor3f(textColor[0], textColor[1], textColor[2]);

    int step = 2; 

    // ===== X ось на Z = 0, Y = 0 =====
    for (int x = -WORLD_X; x <= WORLD_X; x += step)
    {
        drawText3D(x, 0.0f, 0.0f, QString::number(x), textColor[0], textColor[1], textColor[2]);
    }

    // ===== Z ось на X = 0, Y = 0 =====
    for (int z = -WORLD_Z; z <= WORLD_Z; z += step)
    {
        drawText3D(0.0f, 0.0f, z, QString::number(z), textColor[0], textColor[1], textColor[2]);
    }

    // ===== Y ось на X = 0, Z = 0 =====
    for (int y = -WORLD_Y; y <= WORLD_Y; y += step)
    {
        drawText3D(0.0f, y, 0.0f, QString::number(y), textColor[0], textColor[1], textColor[2]);
    }

    glEnable(GL_DEPTH_TEST);
}
void OpenGLWidget::drawAxisText() {
    drawText3D(-WORLD_X,1.0f,0.0f,"-X",1.0f,0.0f,0.0f);
    drawText3D(WORLD_X, 1.0f, 0.0f, "X", 1.0f, 0.0f, 0.0f);
    drawText3D(0.0f, -WORLD_Y - 1.0f, 0.0f, "-Y", 0.0f, 1.0f, 0.0f);
    drawText3D(0.0f, WORLD_Y + 1.0f, 0.0f, "Y", 0.0f, 1.0f, 0.0f);
    drawText3D(0.0f, 1.0f, -WORLD_Z, "-Z", 0.0f, 0.0f, 1.0f);
    drawText3D(0.0f, 1.0f, WORLD_Z, "Z", 0.0f, 0.0f, 1.0f);

    update();
}
void OpenGLWidget::clampPosition(float& x, float& y, float& z)
{
    x = std::clamp(x, -WORLD_X, WORLD_X);
    y = std::clamp(y, -WORLD_Y, WORLD_Y);
    z = std::clamp(z, -WORLD_Z, WORLD_Z);
}
OpenGLWidget::OpenGLWidget(QWidget* parent, UI* ui) : QOpenGLWidget(parent)
{
    setFocusPolicy(Qt::StrongFocus);
    setFocus();
    this->ui = ui;
}
void OpenGLWidget::initializeGL()
{
    initializeOpenGLFunctions();

    glClearColor(background[0], background[1], background[2], 1.0f);

    glEnable(GL_DEPTH_TEST);    
    glDepthFunc(GL_LESS);
}
void OpenGLWidget::resizeGL(int w, int h)
{
    if (h == 0) h = 1;

    glViewport(0, 0, w, h);

    float fov = 60.0f;
    float aspect = float(w) / float(h);
    float zNear = 0.1f;
    float zFar = 100.0f;

    float f = 1.0f / tanf(fov * 0.5f * M_PI / 180.0f);

    float proj[16] = {
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (zFar + zNear) / (zNear - zFar), -1,
        0, 0, (2 * zFar * zNear) / (zNear - zFar), 0
    };

    glMatrixMode(GL_PROJECTION);
    glLoadMatrixf(proj);
    glMatrixMode(GL_MODELVIEW);
}
void OpenGLWidget::setConfig(const float Bg[], const float _textColor[], const int lvl, const float _camStep) {
    for (int i = 0; i < 3; i++) {
        background[i] = Bg[i];
        textColor[i] = _textColor[i];
    }
    if (lvl == 1) err = 1.0f;
    else if (lvl == 2) err = 0.6f;
    else err = 0.5f;
    
    camStep = _camStep;
    level = lvl;

    update();
}
void OpenGLWidget::drawGrid(float size, float step)
{
    glLineWidth(1.0f);
    glColor3f(1.0f, 1.0f, 1.0f);

    glBegin(GL_LINES);

    glLineWidth(1.0f);
    glBegin(GL_LINES);

    // ===== Плоскость XZ (Y = 0) =====
    for (int z = -WORLD_Z; z <= WORLD_Z; z += step){
        if (z == 0)glColor3f(0.0f, 1.0f, 0.0f); 
        else glColor3f(0.6f, 0.6f, 0.6f);

        glVertex3f(-WORLD_X, 0.0f, z);
        glVertex3f(WORLD_X, 0.0f, z);
    }
    for (int x = -WORLD_X; x <= WORLD_X; x += step){
        if (x == 0)glColor3f(1.0f, 0.0f, 0.0f); 
        else glColor3f(0.6f, 0.6f, 0.6f);

        glVertex3f(x, 0.0f, -WORLD_Z);
        glVertex3f(x, 0.0f, WORLD_Z);
    }
    // ===== Плоскость XY (Z = 0) =====
    for (int y = -WORLD_Y; y <= WORLD_Y; y += step){
        if (y == 0) glColor3f(1.0f, 0.0f, 0.0f); 
        else glColor3f(0.6f, 0.6f, 0.6f);

        glVertex3f(-WORLD_X, y, 0.0f);
        glVertex3f(WORLD_X, y, 0.0f);
    }
    for (int x = -WORLD_X; x <= WORLD_X; x += step){
        glColor3f(x == 0 ? 1.0f : 0.6f,x == 0 ? 0.0f : 0.6f,x == 0 ? 0.0f : 0.6f);

        glVertex3f(x, -WORLD_Y, 0.0f);
        glVertex3f(x, WORLD_Y, 0.0f);
    }
    // ===== Плоскость YZ (X = 0) =====
    for (int y = -WORLD_Y; y <= WORLD_Y; y += step) {
        glColor3f(y == 0 ? 0.0f : 0.6f,y == 0 ? 0.0f : 0.6f,y == 0 ? 1.0f : 0.6f);

        glVertex3f(0.0f, y, -WORLD_Z);
        glVertex3f(0.0f, y, WORLD_Z);
    }
    for (int z = -WORLD_Z; z <= WORLD_Z; z += step){
        glColor3f(z == 0 ? 0.0f : 0.6f,z == 0 ? 1.0f : 0.6f,z == 0 ? 0.0f : 0.6f);

        glVertex3f(0.0f, -WORLD_Y, z);
        glVertex3f(0.0f, WORLD_Y, z);
    }

    glEnd();
    glEnd();
    glEnd();
}
QPointF OpenGLWidget::worldToScreen(float x, float y) const
{
    float sx = (x + 10) / 20.0 * width();
    float sy = (10 - y) / 20.0 * height();
    return QPointF(sx, sy);
}
void OpenGLWidget::drawPoint() {

    glPointSize(12.0f);
    glColor3f(0.0f, 0.5f, 1.0f);
    glBegin(GL_POINTS);
    glVertex3f(xPoint, yPoint,zPoint);
    glEnd();
}
void OpenGLWidget::paintGL()
{
    glClearColor(background[0], background[1], background[2], 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glRotatef(camPitch, 1, 0, 0);
    glRotatef(camYaw, 0, 1, 0);
    glTranslatef(-camX, -camY, -camZ);

    glDisable(GL_DEPTH_TEST);
    drawGrid(10, 2);
    glEnable(GL_DEPTH_TEST);

    drawAxisNumbers();
    drawAxisText();

    if (start) {
        drawPoint();
    }
}
void OpenGLWidget::startGame() {
    start = true;
    if (level == 1) {
        xPoint = QRandomGenerator::global()->bounded(-10, 10);
        yPoint = QRandomGenerator::global()->bounded(-10, 10);
        zPoint = QRandomGenerator::global()->bounded(-10, 10);
    }
    else {
        xPoint = QRandomGenerator::global()->bounded(-10, 10);
        yPoint = QRandomGenerator::global()->bounded(-10, 10);
        zPoint = QRandomGenerator::global()->bounded(-10, 10);
        /*auto rng = QRandomGenerator::global();
        xPoint = static_cast<float>(rng->generateDouble() * 20.0 - 10.0);
        yPoint = static_cast<float>(rng->generateDouble() * 20.0 - 10.0);
        zPoint = static_cast<float>(rng->generateDouble() * 20.0 - 10.0);*/
    }

    InputDialog* dlg = new InputDialog(this);
    dlg->setAttribute(Qt::WA_DeleteOnClose);
    dlg->show();

    connect(dlg, &InputDialog::acceptedValues,
        this, [this](int x, int y, int z)
        {
            QDateTime now = getCurrentDate();
            QString formatted = getConvertedDate(now);

            bool xOk = abs(x - xPoint) < err;
            bool yOk = abs(y - yPoint) < err;
            bool zOk = abs(z - zPoint) < err;

            if (xOk && yOk && zOk) { QMessageBox::information(this, "XYZ Координаты", "Х, Y и Z угаданы"); score += level * 2; }
            else if (xOk && yOk && !zOk) { QMessageBox::information(this, "XYZ Координаты", "Х и Y угаданы, Z не угадан"); score += level; }
            else if (xOk && !yOk && zOk) { QMessageBox::information(this, "XYZ Координаты", "Х и Z угаданы, Y не угадан"); score += level; }
            else if (!xOk && yOk && zOk) { QMessageBox::information(this, "XYZ Координаты", "Y и Z угаданы, X не угадан"); score += level; }
            else if (xOk && !yOk && !zOk) { QMessageBox::information(this, "XYZ Координаты", "Только X угадан"); score += level; }
            else if (!xOk && yOk && !zOk) { QMessageBox::information(this, "XYZ Координаты", "Только Y угадан"); score += level; }
            else if (!xOk && !yOk && zOk) { QMessageBox::information(this, "XYZ Координаты", "Только Z угадан"); score += level; }
            else { QMessageBox::information(this, "XYZ Координаты", "Ни одна координата не угадана"); score -= level; }

            qDebug() << "X: " << xPoint << " Y " << yPoint << " Z " << zPoint;

            updateData(score, ui->getName(), formatted.toStdString());
            this->window()->setWindowTitle(QString("Угадай координату    Очки: %1").arg(score));
        });


    update();
}
void OpenGLWidget::keyPressEvent(QKeyEvent* event)
{
    if (!event->isAutoRepeat() && event->key() == Qt::Key_F9) {
        startGame();
        event->accept();
        return;
    }
    else if (event->key() == Qt::Key_W) camZ -= camStep;
    else if (event->key() == Qt::Key_S) camZ += camStep;
    else if (event->key() == Qt::Key_A) camX -= camStep;
    else if (event->key() == Qt::Key_D) camX += camStep;
    else if (event->key() == Qt::Key_Q) camY += camStep;
    else if (event->key() == Qt::Key_E) camY -= camStep;
    else if (event->key() == Qt::Key_Up) camPitch += camStep;
    else if (event->key() == Qt::Key_Down) camPitch -= camStep;
    else if (event->key() == Qt::Key_Left) camYaw -= camStep;
    else if (event->key() == Qt::Key_Right) camYaw += camStep;
    else if (event->key() == Qt::Key_C) { camPitch = 90; camZ = 0; camY = 20; camX = 0; }
    else if (event->key() == Qt::Key_V) { camPitch = -90; camZ = 0; camY = -20; camX = 0;}
    else if (event->key() == Qt::Key_B) { camX = -20; camZ = 0; camYaw = 90;}
    else if (event->key() == Qt::Key_N) { camX = 20; camZ = 0; camYaw = -90; }

    update();

    QOpenGLWidget::keyPressEvent(event);
}
void OpenGLWidget::mousePressEvent(QMouseEvent* event) {
    if (event->button() == Qt::RightButton)
    {
        QMenu menu(this);

        QAction* startAction = menu.addAction("Запуск");
        QAction* settingsAction = menu.addAction("Настройки");
        QAction* tournamendAction = menu.addAction("Турнирная таблица");
        QAction* uprAction = menu.addAction("Управление");
        QAction* exitAction = menu.addAction("Выход");
        QAction* selectedAction = menu.exec(event->globalPosition().toPoint());


        if (selectedAction == startAction) startGame();
        else if (selectedAction == settingsAction)
        {
            Settings s;
            s.openWindow(this);
        }
        else if (selectedAction == exitAction)
        {
            QMessageBox::information(this, "Выход", "Закрываем приложение...");

            QWidget* topLevel = this->window();
            if (topLevel) topLevel->close();
        }
        else if (selectedAction == tournamendAction) ui->showTournament();
        else if (selectedAction == uprAction) ui->showUpravlenie();
    }
    else QOpenGLWidget::mousePressEvent(event);
}