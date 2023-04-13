#include <limits>
#include <set>
#include <map>
#include <queue>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
#include "GraphElements.h"
#include "Graph.h"
#include "DijkstraShortestPathAlg.h"
#include "YenTopKShortestPathsAlg.h"
#include <fstream>
#include <ctime>
#include <string>
#include <vector>
#include <stdio.h>
#include <cstdio>
#include <cassert>

#include <cstring>

#include <iostream>
//用到线程，下方的cstdlib库、windows.h头文件必须同时引入
#include <cstdlib>
#include <windows.h>

using namespace std;


void testDijkstraGraph(int org2, int dst2, std::ofstream& out1, std::ofstream& out)
{
	Graph* my_graph_pt = new Graph("C:/Users/111/Desktop/k-shortest-paths-cpp-version-master/data/test_7466_1");
	DijkstraShortestPathAlg shortest_path_alg(my_graph_pt);
	BasePath* result =
		shortest_path_alg.get_shortest_path(
			my_graph_pt->get_vertex(org2), my_graph_pt->get_vertex(dst2));
	result->PrintOut(out, out1);
}

vector<string> Tokenize(const string str, const string delimiters)
{
	// Skip delimiters at beginning.  vector<string>& tokens,
	vector<string> tokens;
	string::size_type lastPos = str.find_first_not_of(delimiters, 0);
	// Find first "non-delimiter".
	string::size_type pos = str.find_first_of(delimiters, lastPos);

	while (string::npos != pos || string::npos != lastPos)
	{
		// Found a token, add it to the vector.
		tokens.push_back(str.substr(lastPos, pos - lastPos));
		// Skip delimiters.  Note the "not_of"
		lastPos = str.find_first_not_of(delimiters, pos);
		// Find next "non-delimiter"
		pos = str.find_first_of(delimiters, lastPos);
	}
	return tokens;
}



void testYenAlg(int org2, int dst2, std::ofstream& out1, std::ofstream& out)
{
	Graph my_graph("C:/Users/111/Desktop/k-shortest-paths-cpp-version-master/data/test_7466_1");

	YenTopKShortestPathsAlg yenAlg(my_graph, my_graph.get_vertex(org2),
		my_graph.get_vertex(dst2));

	int i = 0;
	//while(yenAlg.has_next())
	clock_t startTime, endTime;
	startTime = clock();//计时开始
	while (i <= 3)
	{
		if (yenAlg.has_next())
		{
			yenAlg.next()->PrintOut(out, out1);
			out << "\n";
			endTime = clock();//计时结束
			cout << "The run time is:" << (double)(endTime - startTime) / CLOCKS_PER_SEC << "s" << endl;
		}
		++i;
	}

}

//  读取文件行数
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
// 读取文件某一行
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



int cotlines=101;
HANDLE hMutex;//互斥锁

DWORD WINAPI Thread_Function(LPVOID lpParameter)//线程执行的函数odlist_new_1  new150
{
	char* thread_name = (char*)lpParameter;
	char filename[] = "C:/Users/111/Desktop/k-shortest-paths-cpp-version-master/data/od/odlist_new_new000.txt";
	cout << "创建线程" << endl;


	const char *file1 = "route_r_new.txt";
	char* route = new char[strlen(file1) + strlen(thread_name) + 1];
	strcpy(route, thread_name);
	strcat(route, file1);
	
	const char* file2 = "cost_r_new.txt";
	char* cost1 = new char[strlen(file2) + strlen(thread_name) + 1];
	strcpy(cost1, thread_name);
	strcat(cost1, file2);

	ofstream out(route);
	ofstream out1(cost1);



	vector<string>tokens;
	//将传过来参数转化为字符串
	//这里LPVOID相当于其它编程语言的Object类型，(char *)就是string
	while (true)//线程的执行必须与while相配，Thread_Function的代码跑完了，线程也就死亡了
	{
		WaitForSingleObject(hMutex, INFINITE);//临界区开始
		//仅能有一个线程↓↓↓↓↓↓↓↓↓↓↓↓
		if (cotlines > 0)
		{
			string textline = ReadLine(filename, cotlines);
			tokens=Tokenize(textline, " ");
			cout << thread_name <<":哈哈哈，抢到了...： " << tokens[0] << " " << tokens[1] << endl;
			const char* org1 = tokens[0].c_str();
			const char* dst1 = tokens[1].c_str();
			int org2 = atoi(org1);
			int dst2 = atoi(dst1);
			testYenAlg(org2, dst2, out1, out);
			//Sleep(1000);
			cotlines--;//不得同时处理ticket，否则会乱套的，
			Sleep(10);
			cout << thread_name << "刷到了，当前OD为: " << org2<<" "<<dst2 << endl;
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


int main(...)
{
	cout << "Welcome to the real world!" << endl;

	//testDijkstraGraph();
	// testYenAlg();
	
	// string file = "C:/Users/111/Desktop/k-shortest-paths-cpp-version-master/data/odlist_new.txt";odlist_new_1
	char filename[] = "C:/Users/111/Desktop/k-shortest-paths-cpp-version-master/data/od/odlist_new_new000.txt";
	
	cotlines = CountLines(filename);
	// string textline=ReadLine(filename, 1115);
	// cout << textline<< endl;
	cout <<"总行数： " << cotlines<< endl;

	hMutex = CreateMutex(NULL, FALSE, NULL);//初始化互斥锁
	//创建8个线程
	//这里关键是两个参数：
	//第3个参数，指明线程执行的函数
	//第4个参数，是给线程执行的函数中LPVOID lpParameter所传递的值
	char str1[255] = "线程1";
	char str2[255] = "线程2";
	char str3[255] = "线程3";
	char str4[255] = "线程4";
	char str5[255] = "线程5";
	char str6[255] = "线程6";
	char str7[255] = "线程7";
	char str8[255] = "线程8";
	char str9[255] = "线程9";
	char str10[255] = "线程10";

	char str11[255] = "线程11";
	char str12[255] = "线程12";
	char str13[255] = "线程13";
	char str14[255] = "线程14";
	char str15[255] = "线程15";
	char str16[255] = "线程16";
	char str17[255] = "线程17";
	char str18[255] = "线程18";
	char str19[255] = "线程19";
	char str20[255] = "线程20";

	char str21[255] = "线程21";
	char str22[255] = "线程22";
	char str23[255] = "线程23";
	char str24[255] = "线程24";
	char str25[255] = "线程25";
	char str26[255] = "线程26";
	char str27[255] = "线程27";
	char str28[255] = "线程28";
	char str29[255] = "线程29";
	char str30[255] = "线程30";


	HANDLE hThread_1 = CreateThread(NULL, 0, Thread_Function, str1, 0, NULL);
	HANDLE hThread_2 = CreateThread(NULL, 0, Thread_Function, str2, 0, NULL);
	HANDLE hThread_3 = CreateThread(NULL, 0, Thread_Function, str3, 0, NULL);
	HANDLE hThread_4 = CreateThread(NULL, 0, Thread_Function, str4, 0, NULL);
	HANDLE hThread_5 = CreateThread(NULL, 0, Thread_Function, str5, 0, NULL);
	HANDLE hThread_6 = CreateThread(NULL, 0, Thread_Function, str6, 0, NULL);
	HANDLE hThread_7 = CreateThread(NULL, 0, Thread_Function, str7, 0, NULL);
	HANDLE hThread_8 = CreateThread(NULL, 0, Thread_Function, str8, 0, NULL);
	HANDLE hThread_9 = CreateThread(NULL, 0, Thread_Function, str9, 0, NULL);
	HANDLE hThread_10 = CreateThread(NULL, 0, Thread_Function, str10, 0, NULL);

	HANDLE hThread_11 = CreateThread(NULL, 0, Thread_Function, str11, 0, NULL);
	HANDLE hThread_12 = CreateThread(NULL, 0, Thread_Function, str12, 0, NULL);
	HANDLE hThread_13 = CreateThread(NULL, 0, Thread_Function, str13, 0, NULL);
	HANDLE hThread_14 = CreateThread(NULL, 0, Thread_Function, str14, 0, NULL);
	HANDLE hThread_15 = CreateThread(NULL, 0, Thread_Function, str15, 0, NULL);
	HANDLE hThread_16 = CreateThread(NULL, 0, Thread_Function, str16, 0, NULL);
	HANDLE hThread_17 = CreateThread(NULL, 0, Thread_Function, str17, 0, NULL);
	HANDLE hThread_18 = CreateThread(NULL, 0, Thread_Function, str18, 0, NULL);
	HANDLE hThread_19 = CreateThread(NULL, 0, Thread_Function, str19, 0, NULL);
	HANDLE hThread_20 = CreateThread(NULL, 0, Thread_Function, str20, 0, NULL);

	HANDLE hThread_21 = CreateThread(NULL, 0, Thread_Function, str21, 0, NULL);
	HANDLE hThread_22 = CreateThread(NULL, 0, Thread_Function, str22, 0, NULL);
	HANDLE hThread_23 = CreateThread(NULL, 0, Thread_Function, str23, 0, NULL);
	HANDLE hThread_24 = CreateThread(NULL, 0, Thread_Function, str24, 0, NULL);
	HANDLE hThread_25 = CreateThread(NULL, 0, Thread_Function, str25, 0, NULL);
	HANDLE hThread_26 = CreateThread(NULL, 0, Thread_Function, str26, 0, NULL);
	HANDLE hThread_27 = CreateThread(NULL, 0, Thread_Function, str27, 0, NULL);
	HANDLE hThread_28 = CreateThread(NULL, 0, Thread_Function, str28, 0, NULL);
	HANDLE hThread_29 = CreateThread(NULL, 0, Thread_Function, str29, 0, NULL);
	HANDLE hThread_30 = CreateThread(NULL, 0, Thread_Function, str30, 0, NULL);


	//等线程1、2、3结束才能结束下方的代码
	DWORD dwRet = WaitForSingleObject(hThread_1, INFINITE);
	DWORD dwRet1 = WaitForSingleObject(hThread_2, INFINITE);
	DWORD dwRet2 = WaitForSingleObject(hThread_3, INFINITE);
	DWORD dwRet3 = WaitForSingleObject(hThread_4, INFINITE);
	DWORD dwRet4 = WaitForSingleObject(hThread_5, INFINITE);
	DWORD dwRet5 = WaitForSingleObject(hThread_6, INFINITE);
	DWORD dwRet6 = WaitForSingleObject(hThread_7, INFINITE);
	DWORD dwRet7 = WaitForSingleObject(hThread_8, INFINITE);
	DWORD dwRet8 = WaitForSingleObject(hThread_8, INFINITE);
	DWORD dwRet9 = WaitForSingleObject(hThread_9, INFINITE);
	DWORD dwRet10 = WaitForSingleObject(hThread_10, INFINITE);

	DWORD dwRet11 = WaitForSingleObject(hThread_11, INFINITE);
	DWORD dwRet12 = WaitForSingleObject(hThread_12, INFINITE);
	DWORD dwRet13 = WaitForSingleObject(hThread_13, INFINITE);
	DWORD dwRet14 = WaitForSingleObject(hThread_14, INFINITE);
	DWORD dwRet15 = WaitForSingleObject(hThread_15, INFINITE);
	DWORD dwRet16 = WaitForSingleObject(hThread_16, INFINITE);
	DWORD dwRet17 = WaitForSingleObject(hThread_17, INFINITE);
	DWORD dwRet18 = WaitForSingleObject(hThread_18, INFINITE);
	DWORD dwRet19 = WaitForSingleObject(hThread_19, INFINITE);
	DWORD dwRet20 = WaitForSingleObject(hThread_20, INFINITE);

	DWORD dwRet21 = WaitForSingleObject(hThread_21, INFINITE);
	DWORD dwRet22 = WaitForSingleObject(hThread_22, INFINITE);
	DWORD dwRet23 = WaitForSingleObject(hThread_23, INFINITE);
	DWORD dwRet24 = WaitForSingleObject(hThread_24, INFINITE);
	DWORD dwRet25 = WaitForSingleObject(hThread_25, INFINITE);
	DWORD dwRet26 = WaitForSingleObject(hThread_26, INFINITE);
	DWORD dwRet27 = WaitForSingleObject(hThread_27, INFINITE);
	DWORD dwRet28 = WaitForSingleObject(hThread_28, INFINITE);
	DWORD dwRet29 = WaitForSingleObject(hThread_29, INFINITE);
	DWORD dwRet30 = WaitForSingleObject(hThread_30, INFINITE);


	if (dwRet == dwRet1 && dwRet1 == dwRet2 && dwRet2 == dwRet3 && dwRet3 == dwRet4 && dwRet4 == dwRet5 
		&& dwRet5 == dwRet6 && dwRet6 == dwRet7 && dwRet7 == dwRet8 && dwRet8 == dwRet9 && dwRet9 == dwRet10
		&&dwRet11 == dwRet12 && dwRet12 == dwRet13 && dwRet13 == dwRet14 && dwRet14 == dwRet15 && dwRet15 == dwRet16 
		&& dwRet16 == dwRet17 && dwRet17 == dwRet18 && dwRet18 == dwRet19 && dwRet19 == dwRet20 && dwRet20 == dwRet21 &&
		dwRet21 == dwRet22 && dwRet22 == dwRet23 && dwRet23 == dwRet24 && dwRet24 == dwRet25
		&& dwRet25 == dwRet26 && dwRet26 == dwRet27 && dwRet27 == dwRet28 && dwRet28 == dwRet29 && dwRet29 == dwRet30 &&
		dwRet1 == WAIT_OBJECT_0)
	{
		cout << "票没了，大家都散了！" << endl;
		CloseHandle(hMutex);//销毁互斥锁
		CloseHandle(hThread_1);//销毁线程1
		CloseHandle(hThread_2);//销毁线程2
		CloseHandle(hThread_3);//销毁线程3
		CloseHandle(hThread_4);//销毁线程4
		CloseHandle(hThread_5);//销毁线程5
		CloseHandle(hThread_6);//销毁线程6
		CloseHandle(hThread_7);//销毁线程7
		CloseHandle(hThread_8);//销毁线程8
		CloseHandle(hThread_9);//销毁线程8
		CloseHandle(hThread_10);//销毁线程8

		CloseHandle(hThread_11);//销毁线程1
		CloseHandle(hThread_12);//销毁线程2
		CloseHandle(hThread_13);//销毁线程3
		CloseHandle(hThread_14);//销毁线程4
		CloseHandle(hThread_15);//销毁线程5
		CloseHandle(hThread_16);//销毁线程6
		CloseHandle(hThread_17);//销毁线程7
		CloseHandle(hThread_18);//销毁线程8
		CloseHandle(hThread_19);//销毁线程8
		CloseHandle(hThread_20);//销毁线程8

		CloseHandle(hThread_21);//销毁线程1
		CloseHandle(hThread_22);//销毁线程2
		CloseHandle(hThread_23);//销毁线程3
		CloseHandle(hThread_24);//销毁线程4
		CloseHandle(hThread_25);//销毁线程5
		CloseHandle(hThread_26);//销毁线程6
		CloseHandle(hThread_27);//销毁线程7
		CloseHandle(hThread_28);//销毁线程8
		CloseHandle(hThread_29);//销毁线程8
		CloseHandle(hThread_30);//销毁线程8
	}
	return 0;
}

