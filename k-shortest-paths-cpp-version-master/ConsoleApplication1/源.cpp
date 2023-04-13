//如何统计文本的行数及如何读取文件某一行内容：

#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int CountLines(char* filename)
{
    ifstream ReadFile;
    int n = 0;
    string tmp;
    ReadFile.open(filename, ios::in);//ios::in 表示以只读的方式读取文件
    if (ReadFile.fail())//文件打开失败:返回0
    {
        return 0;
    }
    else//文件存在
    {
        while (getline(ReadFile, tmp, '\n'))
        {
            n++;
        }
        ReadFile.close();
        return n;
    }
}

string ReadLine(char* filename, int line)
{
    int lines, i = 0;
    string temp;
    fstream file;
    file.open(filename, ios::in);
    lines = CountLines(filename);

    if (line <= 0)
    {
        return "Error 1: 行数错误，不能为0或负数。";
    }
    if (file.fail())
    {
        return "Error 2: 文件不存在。";
    }
    if (line > lines)
    {
        return "Error 3: 行数超出文件长度。";
    }
    while (getline(file, temp) && i < line - 1)
    {
        i++;
    }
    file.close();
    return temp;
}
int main()
{
    int line;
    char filename[] = "inFile.txt";
    cout << "该文件行数为：" << CountLines(filename) << endl;
    cout << "\n请输入要读取的行数:" << endl;
    while (cin >> line)
    {
        cout << "第" << line << "行的内容是 ：" << endl;
        cout << ReadLine(filename, line);
        cout << "\n\n请输入要读取的行数:" << endl;
    }
}
/**********************************
程序运行情况如下：
该文件行数为：26
请输入要读取的行数:
-3
第-3行的内容是 ：
Error 1: 行数错误，不能为0或负数。
请输入要读取的行数:
4
第4行的内容是 ：
 4      d
请输入要读取的行数:
8
第8行的内容是 ：
 8      h
请输入要读取的行数:
26
第26行的内容是 ：
26      z
请输入要读取的行数:
33
第33行的内容是 ：
Error 3: 行数超出文件长度。
请输入要读取的行数:
66
第66行的内容是 ：
Error 3: 行数超出文件长度。
请输入要读取的行数:
^Z
Process returned 0 (0x0)   execution time : 24.632 s
Press any key to continue.
**********************************/