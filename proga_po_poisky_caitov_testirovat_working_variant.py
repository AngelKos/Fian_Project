#В той же папка где находится эта программа нужно создать пустой файл txt  с названием result и в эту же папку помеситьфайл с названием образовательных учереждений
#После запуска нужно ввести полное название файла с названием образовательных учереждений и ждать в среднем занимает минут 30 -40 можт час если начинает выдавать строку об ошибки и попытке
# то можно подождать до каких то нормальных чисел авось получится но если там где -то под 100 - 1000 попытка то врядли все хорошо
# Успешное окончание файла когда напишет The end of proga
# Для работ нужны библиотеки bs4, time, grab, lxml, pycurl

import sys
from bs4 import BeautifulSoup
import time
from grab import Grab

import re 
def Delete_SQL(string): #Удаляет палочки
    i = string.find('|')
    res = string.partition("|")
    result = res[2]
    if(result.find("|") != -1):
        res = result.partition("|")
        result = res[2]
    return result
def Delete_extended(string): #Удаляет строки из массива delete
    delete = ["RAS", "Russian Academy of Sciences", "of Russian Academy of Sciences", "of the Russian Academy of Sciences", ", Russia", ", RUSSIA", "\n", "}]", ","]
    for part in delete:
        string = string.replace(part, "")
    return string
def Delete_index(string): #Удаляет индекс
    string = re.sub(r'\d{6}','',string)
    return string
def String_format(string): #Удаление всего в правильной последовательности
    string = Delete_SQL(string)
    string = Delete_extended(string)
    string = Delete_index(string)
    return string

def search_of_cites () :
    #print('Введите запрос')
    #Query = str(input())
    #print('Введите кол-во первых n сайтов')
    #number_of_cites = int(input())
    #
    Num_of_cites = 5 # Здесь задается чисо выводимых в массив сайтов 
    Cikl_bool = True
    num_it = 0
    while Cikl_bool :
        Cikl_bool = False
        g = Grab()
        condition = True
        condition_n = 100
        n  = 0
        try:
            resp = g.go('http://google.ru/search?q='+Query)
            time.sleep(2)
            condition = False
        except:
            Bol =True
            while Bol:
                n = 0
                try:
                    resp = g.go('http://google.ru/search?q='+Query)
                    time.sleep(2)
                    Bol = False
                except:
                    n +=1
                    print ('что-то пошло не так делаю попытку запроса номер ' + str(n))
                    
        if g.response.code == 429:
            print(429)

        with open('file1.html','wb') as f:
            f.write(resp.body)
        with open('file1_t.txt','w') as f:
            f.write(str(resp.body))
        with open('file1_t.txt','r') as f:
            text = f.read()
            
        soup = BeautifulSoup(text, 'html.parser')

        #нужно переключение на следующую страницу поисковика
        
        data1 = soup.findAll('div', {'class': 'r'})
        data = list()
        for i in range(len(data1)):
            t = str(data1[i].findNext('a'))
            if t.find('http') != -1 and t.find('https://maps.google.ru')==-1 and t.find('https://www.google.ru/search')==-1:
                data.append(t[t.find('http'):])
        names_of_cites = []
        for i in range(len(data)):
            j = 0
            c = '?'
            while ( ord(str(data[i])[0+j]) != 8250) and(str(data[i])[0+j] != '>') and (str(data[i])[0+j] != c) and (str(data[i])[0+j] != '"') and (str(data[i])[0+j] != ' ') :
                j = j+1
                if data[i][0:j] == 'https://books.google.ru/books':
                    c = ' '
            if not(str(data[i])[0:0+j] in names_of_cites):
                names_of_cites.append(str(data[i])[0:0+j])
        print('n = ' +str(num_it))
        if len(names_of_cites) < Num_of_cites :
            with open('error_cites.txt','a') as fe:
                fe.write(Query+'\n')
            if num_it <20:
                print('unknown bag '+str(num_it))
                Cikl_bool = True
                time.sleep(1)
                num_it = num_it + 1
            else:
                print('else'+str(num_it))
                for i in range(Num_of_cites - len(names_of_cites)):
                    names_of_cites.append('https://'+str(time.time())+str(i))
        if len (names_of_cites) > Num_of_cites:
            names_of_cites = names_of_cites[:Num_of_cites]
    return names_of_cites

#Ниже идет отладочная программа которая будет закоменчена в конечном варианте
print ('the name of file')
filename = str(input())
with open(filename, 'r') as f:
   
    for i in f:
        #print(i)
        if ord(i[0])!= 10 and i[0] != '-':
            #if i[0] == '-':
                #with open ('result.txt', 'a') as f2:
                    #f2.write('New Block\n\n')
                #print('New Block\n')
            #else:
            if i.find('||') != -1:
                with open ('result.txt', 'a') as f2:
                    f2.write('New Block\n\n')
                print('New Block')
            Query = Delete_SQL(i)
            print (i)
            dat = search_of_cites()
            with open ('result.txt', 'a') as f2:
                for i in range(len(dat)):
                    print(str(dat[i]))
                    f2.write(dat[i])
                    f2.write('\n')
                f2.write('\n')
print ('The end of proga')
                
