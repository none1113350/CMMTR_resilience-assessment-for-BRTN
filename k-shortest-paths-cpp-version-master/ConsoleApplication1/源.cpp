//���ͳ���ı�����������ζ�ȡ�ļ�ĳһ�����ݣ�

#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int CountLines(char* filename)
{
    ifstream ReadFile;
    int n = 0;
    string tmp;
    ReadFile.open(filename, ios::in);//ios::in ��ʾ��ֻ���ķ�ʽ��ȡ�ļ�
    if (ReadFile.fail())//�ļ���ʧ��:����0
    {
        return 0;
    }
    else//�ļ�����
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
        return "Error 1: �������󣬲���Ϊ0������";
    }
    if (file.fail())
    {
        return "Error 2: �ļ������ڡ�";
    }
    if (line > lines)
    {
        return "Error 3: ���������ļ����ȡ�";
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
    cout << "���ļ�����Ϊ��" << CountLines(filename) << endl;
    cout << "\n������Ҫ��ȡ������:" << endl;
    while (cin >> line)
    {
        cout << "��" << line << "�е������� ��" << endl;
        cout << ReadLine(filename, line);
        cout << "\n\n������Ҫ��ȡ������:" << endl;
    }
}
/**********************************
��������������£�
���ļ�����Ϊ��26
������Ҫ��ȡ������:
-3
��-3�е������� ��
Error 1: �������󣬲���Ϊ0������
������Ҫ��ȡ������:
4
��4�е������� ��
 4      d
������Ҫ��ȡ������:
8
��8�е������� ��
 8      h
������Ҫ��ȡ������:
26
��26�е������� ��
26      z
������Ҫ��ȡ������:
33
��33�е������� ��
Error 3: ���������ļ����ȡ�
������Ҫ��ȡ������:
66
��66�е������� ��
Error 3: ���������ļ����ȡ�
������Ҫ��ȡ������:
^Z
Process returned 0 (0x0)   execution time : 24.632 s
Press any key to continue.
**********************************/