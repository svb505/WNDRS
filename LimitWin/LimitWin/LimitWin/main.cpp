#include <QApplication>
#include <QLabel>
#include <QVBoxLayout>
#include <QWidget>
#include <QFont>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    QString date = "unknown";
    if (argc > 1) {
        date = argv[1]; 
    }

    QWidget window;
    window.setStyleSheet("background-color: black;");
    window.showFullScreen();

    QVBoxLayout* layout = new QVBoxLayout(&window);
    layout->setAlignment(Qt::AlignCenter);

    QLabel* title = new QLabel("Limit reached!");
    title->setStyleSheet("color: white;");
    QFont font1("Arial", 55, QFont::Bold);
    title->setFont(font1);
    title->setAlignment(Qt::AlignCenter);

    QLabel* dateLabel = new QLabel("The limit will be exhausted " + date);
    dateLabel->setStyleSheet("color: white;");
    QFont font2("Arial", 35, QFont::Bold);
    dateLabel->setFont(font2);
    dateLabel->setAlignment(Qt::AlignCenter);

    layout->addWidget(title);
    layout->addWidget(dateLabel);

    window.setLayout(layout);

    return app.exec();
}