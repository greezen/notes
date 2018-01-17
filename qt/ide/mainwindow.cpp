#include "mainwindow.h"
#include <QMessageBox>
#include <QFileDialog>
#include <QString>

//打开文件
void MainWindow::on_open()
{
    QString filename = QFileDialog::getOpenFileName();
    if(filename.isEmpty()){
        return;
    }

    FILE *p = fopen(filename.toStdString().data(), "rb");
    if(p == NULL){
        QMessageBox::information(this, "错误", "打开文件失败");
        return;
    }

    QString content;

    while (!feof(p)) {
        char buf[1024] = { 0 };
        fgets(buf, sizeof(buf), p);
        content += buf;
    }
    fclose(p);
    txt->setText(content);
}

//保存文件
void MainWindow::on_save()
{
    QString filename = QFileDialog::getSaveFileName();
    if(filename.isEmpty()){
        return;
    }

    FILE *p = fopen(filename.toStdString().data(), "wb");
    if(p == NULL){
        QMessageBox::information(this, "错误", "打开文件失败");
        return;
    }
    fputs(txt->toPlainText().toStdString().data(), p);
    fclose(p);
}

//退出程序
void MainWindow::on_exit()
{
    exit(0);
}

//关于
void MainWindow::on_about()
{
    QMessageBox::information(this, "关于", "QT版IDE");
}

//全选
void MainWindow::on_selectall()
{
    txt->selectAll();
}

//复制
void MainWindow::on_copy()
{
    txt->copy();
}

//粘贴
void MainWindow::on_paste()
{
    txt->paste();
}

//剪切
void MainWindow::on_cut()
{
    txt->cut();
}

//编译
void MainWindow::on_compile()
{

}

//运行
void MainWindow::on_run()
{

}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    //设置中心控件为文本编辑器
    txt = new QTextEdit;
    QColor bgc;
    bgc.setRgb(255,166,123);
    txt->setTextBackgroundColor(bgc);
    txt->setStyleSheet("QTextEdit{background-color:#ccc}");
    this->setCentralWidget(txt);

    //文件菜单
    file = this->menuBar()->addMenu("文件");

    file_open = new QAction("打开", this);
    file_open->setShortcut(tr("Ctrl+O"));//快捷键
    file->addAction(file_open);
    connect(file_open, SIGNAL(triggered(bool)), this, SLOT(on_open()));//绑定事件

    file->addSeparator();//分隔线
    file_save = new QAction("保存", this);
    file_save->setShortcut(tr("Ctrl+S"));
    file->addAction(file_save);
    connect(file_save, SIGNAL(triggered(bool)), this, SLOT(on_save()));

    file->addSeparator();
    file_exit = new QAction("退出", this);
    file->addAction(file_exit);
    connect(file_exit, SIGNAL(triggered(bool)), this, SLOT(on_exit()));

    //编辑菜单
    edit = this->menuBar()->addMenu("编辑");

    edit_selectall = new QAction("全选", this);
    edit_selectall->setShortcut(tr("Ctrl+A"));
    edit->addAction(edit_selectall);
    connect(edit_selectall, SIGNAL(triggered(bool)), this, SLOT(on_selectall()));

    edit->addSeparator();
    edit_copy = new QAction("复制", this);
    edit_copy->setShortcut(tr("Ctrl+C"));
    edit->addAction(edit_copy);
    connect(edit_copy, SIGNAL(triggered(bool)), this, SLOT(on_copy()));

    edit->addSeparator();
    edit_past = new QAction("粘贴", this);
    edit_past->setShortcut(tr("Ctrl+V"));
    edit->addAction(edit_past);
    connect(edit_past, SIGNAL(triggered(bool)), this, SLOT(on_paste()));

    edit->addSeparator();
    edit_cut = new QAction("剪切", this);
    edit_cut->setShortcut(tr("Ctrl+X"));
    edit->addAction(edit_cut);
    connect(edit_cut, SIGNAL(triggered(bool)), this, SLOT(on_cut()));


    //构建菜单
    build = this->menuBar()->addMenu("构建");
    build_compile = new QAction("编译", this);
    build->addAction(build_compile);

    build->addSeparator();
    build_run = new QAction("运行", this);
    build->addAction(build_run);


    //帮助菜单
    help = this->menuBar()->addMenu("帮助");

    help_ahout = new QAction("关于", this);
    help->addAction(help_ahout);
    connect(help_ahout, SIGNAL(triggered(bool)), this, SLOT(on_about()));


}

MainWindow::~MainWindow()
{
    delete txt;
}
