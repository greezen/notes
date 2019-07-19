#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    QSize size;
    size.setWidth(600);
    size.setHeight(500);
    w.resize(size);
    w.show();

    return a.exec();
}
