#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTextEdit>
#include <QMenuBar>
#include <QMenu>
#include <QAction>

class MainWindow : public QMainWindow
{
    Q_OBJECT
private:
    QTextEdit *txt;

    QMenu *file;
    QAction *file_open;
    QAction *file_save;
    QAction *file_exit;

    QMenu *edit;
    QAction *edit_selectall;
    QAction *edit_copy;
    QAction *edit_past;
    QAction *edit_cut;

    QMenu *build;
    QMenu *help;
    QAction *help_ahout;

private slots:
    void on_open();
    void on_save();
    void on_exit();
    void on_about();
    void on_selectall();
    void on_copy();
    void on_paste();
    void on_cut();

public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();
};

#endif // MAINWINDOW_H
