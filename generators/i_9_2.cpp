#define _CRT_SECURE_NO_WARNINGS

#include "json.hpp"

using namespace nlohmann;


#include <iostream>
#include <stdio.h>
#include <string>
#include <ctime> 

using namespace std;




int main(int argc, char *argv[])// на вход: кол-во пикселей по гор, по верт, кол-во цветов
{
	srand(time(NULL));
	setlocale(LC_ALL, "ru_RU.UTF-8");
	int t = rand() % 2;
	int insert0 = 1;//пиксели по гор
	int insert1 = 1;//пиксели по верт
	int insert2 = 1;//кол-во цветов
	int bit = 0;
	int temp = insert2;
	while (temp % 2 == 0)
	{
		bit++;
		temp = temp / 2;
	}
	while (insert1*bit*insert0 % 8192 != 0)
	{
		insert0 = pow(2, 2 + rand() % 10)*t + 100 * (1 + rand() % 10)*(1 - t);
		insert1 = pow(2, 2 + rand() % 10)*t + 100 * (1 + rand() % 10)*(1 - t);
		insert2 = pow(2, 3 + rand() % 5);
	}


	char *sp[4];




	int insert_in[4];

	int arrn[4];
	for (int i = 0; i < 4; i++)
		insert_in[i] = -1;


	for (int i = 1; i < argc; i++)
	{
		sp[i] = strtok(argv[i], "=");
		insert_in[i] = atoi(sp[i]);
		sp[i] = strtok(NULL, "=");
		arrn[i] = atoi(sp[i]);

	}




	int right_order[4];

	for (int i = 1; i < 4; i++)
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


	 bit = 1;
	temp = insert2;
	while (temp > 1)
	{
		bit++;
			temp = temp / 2;
	}
	if (insert2 == pow(2, bit-1))
		bit--;


	if (insert1*bit*insert0 % 8192 != 0 || insert1 < 0 || insert2 < 0 || insert1 < 0)
	{
		cerr << "screamer.jpg";
		exit(1);
	}

	int insert3 = insert0*insert1*bit/8192;


	string insert00 = to_string(insert0);
	string insert11 = to_string(insert1);
	string insert22 = to_string(insert2);
	string insert33 = to_string(insert3);

	json dict =
	{
		{"text", {{"text1",
	{ json::parse(u8R"("Какой минимальный объём памяти (в Кбайт) нужно зарезервировать, чтобы можно было сохранить любое растровое изображение размером ")"), "insert0", json::parse(u8R"("x")"), "insert1", json::parse(u8R"(" пикселей при условии, что в изображении могут использоваться ")"), "insert2", json::parse(u8R"(" различных цветов? В ответе запишите только целое число, единицу измерения писать не нужно.")")}}},

	},

		 {"answers",{ { "text1", 	{json::parse(u8R"("Ответ:")"), "insert3"}}},
	},

	{"inserts", {
	{"insert0", insert00},
	{"insert1", insert11},
	{"insert2", insert22},
	{"insert3", insert33},
		}

			}
	};


	cout << dict << endl;


	return 0;
}
