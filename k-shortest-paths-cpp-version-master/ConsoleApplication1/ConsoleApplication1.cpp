#include <iostream>
//用到线程，下方的cstdlib库、windows.h头文件必须同时引入
#include <cstdlib>
#include <windows.h>

#include <iostream>
#include <thread>
#include <numeric>
#include <algorithm>
#include <vector>
#include <functional>
#include <utility>
#include <windows.h>

using namespace std;

int tickets = 100;//tickets由于被多线程操作，注定是一个全局变量
HANDLE hMutex;//互斥锁

DWORD WINAPI Thread_Function(LPVOID lpParameter)//线程执行的函数
{
	char* thread_name = (char*)lpParameter;
	cout << "创建线程" << endl;
	//将传过来参数转化为字符串
	//这里LPVOID相当于其它编程语言的Object类型，(char *)就是string
	while (true)//线程的执行必须与while相配，Thread_Function的代码跑完了，线程也就死亡了
	{
		WaitForSingleObject(hMutex, INFINITE);//临界区开始
		//仅能有一个线程↓↓↓↓↓↓↓↓↓↓↓↓
		if (tickets > 0)
		{
			tickets--;//不得同时处理ticket，否则会乱套的，
			Sleep(100);
			cout << thread_name << "刷到了票，票还剩余: " << tickets << endl;
		}
		else {
			break;
		}
		//仅能有一个线程↑↑↑↑↑↑↑↑↑↑↑↑
		ReleaseMutex(hMutex);//临界区结束
	}
	cout << thread_name << "被销毁" << endl;
	return 0;
}

int main()//主函数，程序的入口
{
	
	getchar();//等我按个键，程序再开始跑下面的代码啊，别急~
	hMutex = CreateMutex(NULL, FALSE, NULL);//初始化互斥锁
	//创建3个线程
	//这里关键是两个参数：
	//第3个参数，指明线程执行的函数
	//第4个参数，是给线程执行的函数中LPVOID lpParameter所传递的值
	char str1[255] = "线程1";
	char str2[255] = "线程2";
	char str3[255] = "线程3";
	HANDLE hThread_1 = CreateThread(NULL, 0, Thread_Function,str1, 0, NULL);
	HANDLE hThread_2 = CreateThread(NULL, 0, Thread_Function, str2, 0, NULL);
	HANDLE hThread_3 = CreateThread(NULL, 0, Thread_Function,str3, 0, NULL);
	//等线程1、2、3结束才能结束下方的代码
	WaitForSingleObject(hThread_1, INFINITE) ||
		WaitForSingleObject(hThread_2, INFINITE) ||
		WaitForSingleObject(hThread_3, INFINITE);
	cout << "票没了，大家都散了！" << endl;
	CloseHandle(hMutex);//销毁互斥锁
	CloseHandle(hThread_1);//销毁线程1
	CloseHandle(hThread_2);//销毁线程2
	CloseHandle(hThread_3);//销毁线程3
	getchar();//也可以写成system("pause");防止这个控制台程序一闪而过
	return 0;
}