#define _CRT_SECURE_NO_WARNINGS

#include "C:\Program Files (x86)\Microsoft Visual Studio\json.hpp"

using namespace nlohmann;


#include <iostream>
#include <stdio.h>
#include <string>
#include <ctime> 

using namespace std;




int main(int argc, char *argv[])// на вход: начальное смещение по х, начальное смещение по у, по х в цикле, по у в цикле, по х конечное, по у конечное
{
	srand(time(NULL));
	setlocale(LC_ALL, "ru_RU.UTF-8");
	int insert0 = 0;
	int insert1 = 0;
	int insert2 = 0;
	int insert3 = 0;
	int insert4 = 0;
	int insert5 = 0;
	int insert6 = 0;

	while (insert2 == 0 && insert3 == 0 || insert0 + insert4 == 0 && insert1+insert5 == 0)
	{
		insert0 = -100 + rand() % 200;
		insert1 = -100 + rand() % 200;
		insert0 = -10 + rand() % 20;
		insert0 = -10 + rand() % 20;
		insert2 = -100 + rand() % 200;
		insert3 = -100 + rand() % 200;

	}

	char *sp[20];

	int insert_in[7];

	int arrn[7];
	for (int i = 0; i < 7; i++)
		insert_in[i] = -1;


	for (int i = 1; i < argc; i++)
	{
		sp[i] = strtok(argv[i], "=");
		insert_in[i] = atoi(sp[i]);
		sp[i] = strtok(NULL, "=");
		arrn[i] = atoi(sp[i]);

	}




	int right_order[7];

	for (int i = 1; i < 7; i++)
		right_order[i] = -1;

	for (int i = 1; i < argc; i++)
	{
		if (insert_in[i] != -1)
			right_order[insert_in[i]] = arrn[i];

	}






	if (right_order[1] != -1)
		insert0 = right_order[1];

	if (right_order[2] != -1)
		insert1 = right_order[2];

	if (right_order[3] != -1)
		insert2 = right_order[3];

	if (right_order[4] != -1)
		insert3 = right_order[4];

	if (right_order[5] != -1)
		insert4 = right_order[5];

	if (right_order[6] != -1)
		insert5 = right_order[6];


	


	if (insert2 == 0 && insert3 == 0 || insert0 + insert4 == 0 && insert1 + insert5 == 0)
	{
		cerr << "None of us claimed to be perfect";
		exit(1);
	}


	if (insert0 + insert4 == 0 || insert1 + insert5 == 0)
		insert6 = max(abs(insert0 + insert4), abs(insert1 + insert5));
	else
	{
		int a = abs(insert0 + insert4);
			int b = abs(insert1 + insert5);
			while (a > 0 && b > 0)
			{
				if (a > b)
					a %= b;
				else
					b %= a;

			}
			insert6 = a + b;
	}

	string insert00 = to_string(insert0);
	string insert11 = to_string(insert1);
	string insert22 = to_string(insert2);
	string insert33 = to_string(insert3);
	string insert44 = to_string(insert4);
	string insert55 = to_string(insert5);
	string insert66 = to_string(insert6);

	json dict =
	{
		{"text", {{"text1",
	{ json::parse(u8R"("Исполнитель Чертёжник перемещается на координатной плоскости, оставляя след в виде линии. Чертёжник может выполнять команду сместиться на (a, b), где a, b – целые числа. Эта команда перемещает Чертёжника из точки с координатами (x, y) в точку с координатами (x + a, y + b). Например, если Чертёжник находится в точке с координатами (4, 2), то команда сместиться на (2, ?3) переместит Чертёжника в точку (6, ?1). \n Цикл  \n ПОВТОРИ число РАЗ  \n последовательность команд \n КОНЕЦ ПОВТОРИ  \n означает, что последовательность команд будет выполнена указанное число раз (число должно быть натуральным).  \n Чертёжнику был дан для исполнения следующий алгоритм (количество повторений и смещения в первой из повторяемых команд неизвестны):  \n НАЧАЛО \n сместиться на (")"), "insert0", json::parse(u8R"(", ")"), "insert1", json::parse(u8R"(" ) \n ПОВТОРИ ... РАЗ \n сместиться на (..., ...) \n сместиться на ( ")"), "insert2", json::parse(u8R"(", ")"), "insert3", json::parse(u8R"(",) \n КОНЕЦ ПОВТОРИ \n сместиться на ( ")"), "insert4 ", json::parse(u8R"(", ")"), "insert5",json::parse(u8R"(") \n КОНЕЦ \n После выполнения этого алгоритма Чертёжник возвращается в исходную точку. Какое наибольшее число повторений могло быть указано в конструкции «ПОВТОРИ ... РАЗ»?")")}}},

	},

		 {"answers",{ { "text1", 	{json::parse(u8R"("Ответ:")"), "insert6"}}},
	},

	{"inserts", {
	{"insert0", insert00},
	{"insert1", insert11},
	{"insert2", insert22},
	{"insert3", insert33},
	{"insert4", insert44},
	{"insert5", insert55},
	{"insert6", insert66},
		}

			}
	};


	cout << dict << endl;


	return 0;
}