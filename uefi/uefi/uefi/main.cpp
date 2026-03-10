#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QKeyEvent>
#include <QStringList>
#include <QProcess>
#include <QSysInfo>
#include <QStorageInfo>
#include <QScreen>
#include <windows.h>
#include <tlhelp32.h>
#include <QThread>

class BiosWindow : public QWidget{
public:
    BiosWindow(){
        menuItems << "Boot Order"
            << "CPU Info"
            << "Memory Info"
            << "Power Settings"
            << "Return"
            << "Exit";

        selectedIndex = 0;
        infoMode = false;

        setStyleSheet("background-color:black;");
        setWindowTitle("UEFI Setup Utility");

        layout = new QVBoxLayout(this);

        title = new QLabel("UEFI Setup Utility");
        title->setStyleSheet("color:lightblue; font: bold 28px 'Courier';");
        layout->addWidget(title);

        drawMenu();

        showFullScreen();
    }

protected:
    void keyPressEvent(QKeyEvent* event) override{
        if (!infoMode){
            if (event->key() == Qt::Key_Up){
                selectedIndex--;
                if (selectedIndex < 0) selectedIndex = menuItems.size() - 1;
                drawMenu();
            }
            if (event->key() == Qt::Key_Down){
                selectedIndex++;
                if (selectedIndex >= menuItems.size()) selectedIndex = 0;
                drawMenu();
            }
            if (event->key() == Qt::Key_Return) selectOption();
        }
        else{
            if (event->key() == Qt::Key_Escape){infoMode = false; drawMenu();}
        }
    }
private:
    QVBoxLayout* layout;
    QLabel* title;
    QVector<QLabel*> labels;
    QStringList menuItems;
    int selectedIndex;
    bool infoMode;

    void clearMenu(){
        for (auto l : labels){
            layout->removeWidget(l);
            delete l;
        }
        labels.clear();
    }
    void drawMenu(){
        clearMenu();

        for (int i = 0; i < menuItems.size(); i++){
            QLabel* label = new QLabel;

            QString prefix = (i == selectedIndex) ? "> " : "  ";
            label->setText(prefix + menuItems[i]);

            if (i == selectedIndex) label->setStyleSheet("color:yellow; font: 22px 'Courier';");
            else label->setStyleSheet("color:white; font: 22px 'Courier';");

            layout->addWidget(label);
            labels.push_back(label);
        }
    }

    void showInfo(QString option){
        clearMenu();
        infoMode = true;

        QLabel* header = new QLabel(option);
        header->setStyleSheet("color:lightgreen; font: 26px 'Courier';");
        layout->addWidget(header);

        QString info;

        if (option == "Boot Order") info = "1. USB Drive\n2. Hard Disk\n3. Network Boot\n4. CD/DVD";
        if (option == "CPU Info"){
            info =
                "Processor: " + QSysInfo::currentCpuArchitecture() + "\n" +
                "Threads: " + QString::number(QThread::idealThreadCount());
        }
        if (option == "Memory Info"){
            MEMORYSTATUSEX mem;
            mem.dwLength = sizeof(mem);
            GlobalMemoryStatusEx(&mem);

            double total = mem.ullTotalPhys / (1024.0 * 1024 * 1024);
            double used = (mem.ullTotalPhys - mem.ullAvailPhys) / (1024.0 * 1024 * 1024);

            info =
                "Total RAM: " + QString::number(total, 'f', 2) + " GB\n" +
                "Used: " + QString::number(used, 'f', 2) + " GB";
        }
        if (option == "Power Settings"){
            info =
                "Power Saving Mode: OFF\n"
                "Sleep Timer: 30 min\n"
                "Wake-on-LAN: ENABLED";
        }

        QLabel* infoLabel = new QLabel(info);
        infoLabel->setStyleSheet("color:white; font:20px 'Courier';");
        layout->addWidget(infoLabel);

        QLabel* esc = new QLabel("[Press ESC to go back]");
        esc->setStyleSheet("color:gray; font:18px 'Courier';");
        layout->addWidget(esc);

        labels.push_back(header);
        labels.push_back(infoLabel);
        labels.push_back(esc);
    }

    void killProcess(QString name){
        HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        PROCESSENTRY32 pe;
        pe.dwSize = sizeof(PROCESSENTRY32);

        if (Process32First(snap, &pe)){
            do{
                if (QString::fromWCharArray(pe.szExeFile) == name){
                    HANDLE h = OpenProcess(PROCESS_TERMINATE, FALSE, pe.th32ProcessID);
                    TerminateProcess(h, 0);
                    CloseHandle(h);
                }
            } while (Process32Next(snap, &pe));
        }

        CloseHandle(snap);
    }

    void selectOption(){
        QString option = menuItems[selectedIndex];

        if (option == "Exit") close();
        else if (option == "Return"){ close(); QProcess::startDetached("WinDoors52.exe"); }
        else showInfo(option);
    }
};

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    BiosWindow w;
    w.show();

    return app.exec();
}