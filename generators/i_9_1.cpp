#define _CRT_SECURE_NO_WARNINGS

#include "C:\Program Files (x86)\Microsoft Visual Studio\json.hpp"

using namespace nlohmann;


#include <iostream>
#include <stdio.h>
#include <string>
#include <ctime> 

using namespace std;




int main(int argc, char *argv[])// на вход: частота дискретизации в к√ц, разрешение, размер полученного файла в мб, все величины положительные
{ 
	srand(time(NULL));
	setlocale(LC_ALL, "ru_RU.UTF-8");
	int insert0 = 16*(1 + rand() % 4);//частота дискретизации
	int insert1 = 16*(pow(2, rand()%3));//разрешение
	int insert2 = 17 + rand() % 456;//кол-во мб


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


	if (insert1 < 0 || insert2 < 0 || insert1 < 0)
	{
		cerr << "screamer.jpg";
		exit(1);
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


	int insert3 = ceil(insert2*pow(2,20)/(insert1*insert0*500));


	string insert00 = to_string(insert0);
	string insert11 = to_string(insert1);
	string insert22 = to_string(insert2);
	string insert33 = to_string(insert3);

	json dict =
	{
		{"text", {{"text1",
	{ json::parse(u8R"("ѕроизводитс€ четырЄхканальна€ (квадро) звукозапись с частотой дискретизации ")"), "insert0", json::parse(u8R"(" к√ц и ")"), "insert1", json::parse(u8R"("-битным разрешением. –езультаты записи записываютс€ в файл, сжатие данных не производитс€; размер полученного файла Ч ")"), "insert2", json::parse(u8R"(" ћбайт. ќпределите приблизительно врем€ записи (в секундах), ответ округлите до большего.")")}}},

	},

		 {"answers",{ { "text1", 	{json::parse(u8R"("ќтвет:")"), "insert3"}}},
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