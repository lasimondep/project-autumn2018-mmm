#define _CRT_SECURE_NO_WARNINGS

#include "C:\Program Files (x86)\Microsoft Visual Studio\json.hpp"// https://github.com/nlohmann/json/releases/download/v3.6.1/json.hpp, путь свой

using namespace nlohmann;


#include <iostream>
#include <stdio.h>
#include <string>
#include <ctime> 

using namespace std;




int main(int argc, char *argv[])// на вход: кол-во символов в пароле, кол-во используемых для пароля символов до 26, место на доп сведения, кол-во пользователей; 0 означает не учитывать
{

	srand(time(NULL));
	setlocale(LC_ALL, "ru_RU.UTF-8");
	int insert0 = 6 + rand() % 42;// кол-во символов в пароле, можно безнаказанно менять
	int insert1 = 4 + rand() % 23;//кол-во используемых для пароля символов, т.к. в их качестве используются заглавные буквы латинского алфавита, менять осторожно, можно получить хтонь
	int bit = 0;
	int temp = insert1;
	while (temp % 2 == 0)
	{
		temp = temp / 2;
		bit++;

	}
	string insert2 = "";//строчка с этими символами через запятую
	int insert3 = 2 + rand() % 42;//место на дополнительные сведения о пользователе, можно безнаказанно менять
	int insert4 = 10 + rand() % 150;//кол-во пользователей, можно менять безнаказанно


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
		if (arrn[i] < 0 || arrn[i] > 26 && insert_in[i] == 2)
			error = 1;
	}

	
	if (error)
	{
		cerr << " — Папа, почему меня зовут Опыт?" << endl << "— Потому что Опыт — это имя, которое мы даём своим ошибкам.";
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
		insert0 = right_order[1];

	if (right_order[2] != -1)
		insert1 = right_order[2];

	if (right_order[3] != -1)
		insert3 = right_order[3];

	if (right_order[4] != -1)
		insert4 = right_order[4];


	 bit = 0;
	temp = insert1;
	while (temp % 2 == 0)
	{
		temp = temp / 2;
		bit++;

	}

	double byte = ceil(bit * insert0 / 8);
	int insert5 = insert4 * (insert3 + byte);//ответ
	
	for (int i = 0; i < insert1; i++)
	{
		insert2.insert(i*3, 1, char('A' + i));
		if (i != insert1 - 1)
		{
			insert2.insert(i*3 + 1, 1, char(','));
			insert2.insert(i*3 + 2, 1, char(' '));
		}
	}
	
	string insert00 = to_string(insert0);
	string insert11 = to_string(insert1);
	string insert33 = to_string(insert3);
	string insert44 = to_string(insert4);
	string insert55 = to_string(insert5);

	json dict =
	{
		{"text",{ {"text1",{  json::parse(u8R"("При регистрации в компьютерной системе каждому пользователю выдаётся пароль, состоящий из")"), "insert0", json::parse(u8R"("символов и содержащий только символы из ")"), "insert1", json::parse(u8R"("-символьного набора: ")"), "insert2", json::parse(u8R"(" В базе данных для хранения сведений о каждом пользователе отведено одинаковое и минимально возможное целое число байт. При этом используют посимвольное кодирование паролей, все символы кодируют одинаковым и минимально возможным количеством бит. Кроме собственно пароля, для каждого пользователя в системе хранятся дополнительные сведения, для чего отведено ")"), "insert3", json::parse(u8R"("байт на одного пользователя. Определите объём памяти (в байтах), необходимый для хранения сведений о ")"), "insert4", json::parse(u8R"("пользователях/пользователе. В ответе запишите только целое число — количество байт.")")}}},

	},

		 {"answers",{ { "text1", 	{json::parse(u8R"("Ответ:")"), "insert5"}}},
	},

	{"inserts", { 
	{"insert0", insert00},
	{"insert1", insert11},
	{"insert2", insert2},
	{"insert3", insert33},
	{"insert4", insert44},
	{"insert5", insert55},
		}

			}
	};


	cout << dict << endl;



	return 0;
}