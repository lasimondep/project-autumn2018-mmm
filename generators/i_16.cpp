#define _CRT_SECURE_NO_WARNINGS

#include "C:\Program Files (x86)\Microsoft Visual Studio\json.hpp"
using namespace nlohmann;


#include <iostream>
#include <stdio.h>
#include <string>
#include <ctime> 

using namespace std;




int main(int argc, char *argv[])// на вход: система счисления; первое число из ряда чисел в десятичной системе; второе число из ряда чисел в десятичной системе; цифра, которая будет искаться в их записи в новой системе счисления. Все числа положительные, первое строго больше четвёртого, третье строго больше второго
{

	srand(time(NULL));
	setlocale(LC_ALL, "ru_RU.UTF-8");
	int insert2 = 2 + rand() % 15;//система счисления
	int insert0 = rand() % (min(10, insert2));// цифра, которую ищем — от нуля до девяти, если это позволяет промежуток
	int a = 5 + rand() % 80;//начало промежутка, на котором ищем
	int b = a + 5 + rand() % 5;// конец промежутка, на котором ищем
	string insert1 = "";//натуральные числа из интервала от а до б; часть его внутренностей, если в этом есть необходимость, заменяется на ...

	char *sp[5];


	int insert_in[5];

	int arrn[5];
	for (int i = 0; i < 5; i++)
		insert_in[i] = -1;

	bool error = 0;

	for (int i = 1; i < argc; i++)
	{
		sp[i] = strtok(argv[i], "=");
		insert_in[i] = atoi(sp[i]);
		sp[i] = strtok(NULL, "=");
		arrn[i] = atoi(sp[i]);
		if (arrn[1] > arrn[4] || arrn[3] > arrn[2] || arrn[1] < 0 || arrn[2] < 0 || arrn[3] < 0 || arrn[4] < 0)
			error = 1;
	}

	if (error)
	{
		cerr << "Где-то в мире загрустила одна черепашка, лишь правильный ввод данных развеселит её." << endl;
		exit(1);
	}



	int right_order[5];

	for (int i = 1; i < 5; i++)
		right_order[i] = -1;

	for (int i = 1; i < argc; i++)
	{
		if (insert_in[i] != -1)
			right_order[insert_in[i]] = arrn[i];

	}




	if (right_order[1] != -1)
		insert2 = right_order[1];

	if (right_order[2] != -1)
		a = right_order[2];

	if (right_order[3] != -1)
		b = right_order[3];

	if (right_order[4] != -1)
		insert1 = right_order[4];

	if (b - a < 5)
	{
		for (int i = a; i <= b; i++)
		{
			insert1 += to_string(i);
			if (i != b)
				insert1 += ", ";
		}
	}

	if (b-a > 4)
	{
		insert1 += to_string(a);
		insert1 += ", ";
		insert1 += to_string(a+1);
		insert1 += ", ... ,";
		insert1 += to_string(b-1);
		insert1 += ", ";
		insert1 += to_string(b);

	}
	int insert3 = 0;
	char buffer[20];
	for (int i = a; i <= b; i++)
	{
		_itoa(i, buffer, insert2);
		int temp = atoi(buffer);
		while (temp > 0)
		{
			if (temp % 10 == insert0)
				insert3++;
			temp = temp / 10;
		}
	}

	string insert00 = to_string(insert0);
	string insert22 = to_string(insert2);
	string insert33 = to_string(insert3);
	json dict =
	{
		{"text", {{"text1",
	{ json::parse(u8R"("Укажите, сколько всего раз встречается цифра ")"), "insert0", json::parse(u8R"(" в записи чисел")"), "insert1", json::parse(u8R"(" в системе счисления с основанием ")"), "insert2", json::parse(u8R"(".")")}}},

	},

		 {"answer", {{ "text1",
		{json::parse(u8R"("Ответ:")"), "insert3"}}},},

	{"inserts", {
	{"insert0", insert00},
	{"insert1", insert1},
	{"insert2", insert22},
	{"insert3", insert33},
		}

			}
	};


	cout << dict << endl;


	return 0;
}