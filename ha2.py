import csv

def read_file(file_name: str) -> list:
    """
    Читает csv файл с данными  и возвращает список строк (список списков),
    где первый список - это название колонок.
    """
    with open(file_name, encoding="utf8") as csvfile:
        db = csv.reader(csvfile, delimiter=';')
        db = list(db)
        return db


def menu(file_name: str):
    """
    Создает меню для выбора действий по обработке данных отчета.
    """
    data = read_file(file_name)

    print('Выберите действие из меню:\n')
    print('Вывести в понятном виде иерархию команд:\n'
          'департамент и все команды, которые входят в него - наберите 1', '\n')
    print('Вывести сводный отчёт по департаментам:\nназвание, численность,'
          '"вилка" зарплат в виде мин – макс, среднюю зарплату - наберите 2', '\n')
    print('Сохранить сводный отчёт из предыдущего пункта в виде csv-файла.\n'
          'При этом необязательно вызывать сначала команду из п.2 - наберите 3', '\n')
    print('Завершить работу - наберите 4')

    while True:
        choice = input()
        if choice == '1':
            print('Выводим структуру:')
            make_hierarchy(data)
        elif choice == '2':
            print('Получаем сводный отчет:')
            make_report(data)
        elif choice == '3':
            print('Записываем сводный отчет в файл')
            make_report(data, save_report=True)
        elif choice == '4':
            return print('Завершаем работу')
        else:
            print('Выберите: 1, 2, 3 или 4')

def make_hierarchy(db: list):
    """
    Формирует структуру департаментов и выводит ее на экран.
    """
    columns = db[0]
    data = db[1:]
    depart, group = [columns.index('Департамент'), columns.index('Отдел')]
    struct_set = {(x[depart], x[group]) for x in data}
    struct_set = sorted(struct_set, key = lambda x: x[0])
    dep = ''
    for x in struct_set:
        if x[0] != dep:
            print(x[0])
            dep = x[0]
        print('    ' + x[1])


def make_report(db: list, save_report: bool = False):
    """
    Создание сводного отчёта по департаментам: название, численность,
    "вилка" зарплат в виде мин – макс, средняя зарплата.
    При save_report = False (дефолтное значение) выводит на экран,
    при save_report = True сохраняет с ним файл.
    """
    columns = db[0]
    data = db[1:]
    depart, salary = [columns.index('Департамент'), columns.index('Оклад')]
    departs = {employee[depart] for employee in data}
    dep_salary = dict()
    for dep in departs:
        employees = filter(lambda employee: employee[depart] == dep, db)
        dep_salary[dep] = [int(empl[salary]) for empl in employees]
        dep_salary[dep] = [len(dep_salary[dep]), min(dep_salary[dep]),
                           sum(dep_salary[dep]) / len(dep_salary[dep]),
                           max(dep_salary[dep])]
    if save_report == False:
        print('Название департамента', 'Численность', 'Мин.', 'Ср.знач.', 'Макс.')
        for depart in departs:
            print(depart, *dep_salary[depart])

    if save_report == True:
        with open('report.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Департ.', 'числ-ть', 'мин.', 'ср.знач.', 'макс.'])
            for depart in departs:
                writer.writerow([depart] + dep_salary[depart])

if __name__ == '__main__':
    menu('Corp_Summary.csv')