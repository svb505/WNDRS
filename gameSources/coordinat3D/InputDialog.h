#pragma once
#include <QDialog>
#include <QPoint>

class QDoubleSpinBox;
class QPushButton;

class InputDialog : public QDialog
{
    Q_OBJECT
public:
    explicit InputDialog(QWidget* parent = nullptr);

    int firstValue() const;
    int secondValue() const;
    int thirtValue() const;
private:
    QDoubleSpinBox* spin1;
    QDoubleSpinBox* spin2;
    QDoubleSpinBox* spin3;
signals:
    void acceptedValues(int x, int y, int z);
};
