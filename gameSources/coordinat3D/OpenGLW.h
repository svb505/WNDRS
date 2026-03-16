#pragma once
#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include "UI.h"
#include "DataBase.h"

class OpenGLWidget : public QOpenGLWidget, protected QOpenGLFunctions
{
    Q_OBJECT
private:
    const float WORLD_X = 10.0f;
    const float WORLD_Y = 10.0f;
    const float WORLD_Z = 10.0f;
    const int step = 2;
    const int W = width() / 20;
    const int H = -height() / 20;
    int count = 5;
    float camYaw = 0.0f;
    float camPitch = 0.0f;
    float camX = 0.0f;
    float camY = 5.0f;
    float camZ = 10.0f;
    float camStep = 1.0f;
    float background[3] = { 0.1f, 0.1f, 0.15f };
    float textColor[3] = {1.0f, 1.0f, 1.0f};
    bool start = false;
    float xPoint = 0.0f;
    float yPoint = 0.0f;
    float zPoint = 0.0f;
    float err = 2.0f;
    int score = 0;
public:
    int level = 1;
    UI* ui;
    explicit OpenGLWidget(QWidget* parent = nullptr, UI* ui = nullptr);
    void drawGrid(float size, float step);
    void setConfig(const float Bg[], const float _textColor[], const int lvl,const float _camStep);
    void drawPoint();
    void startGame();
    void keyPressEvent(QKeyEvent* event);
    void clampPosition(float& x, float& y, float& z);
    void drawAxisNumbers();
    void drawText3D(float x, float y, float z, const QString& text, float R = 0.0f,float G = 0.0f, float B = 0.0f);
    void drawAxisText();
protected:
    void initializeGL() override;
    void resizeGL(int w, int h) override;
    void paintGL() override;
    void mousePressEvent(QMouseEvent* event) override;
    QPointF worldToScreen(float x, float y) const;
};
