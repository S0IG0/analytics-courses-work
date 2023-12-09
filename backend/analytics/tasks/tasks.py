import os
import uuid
from io import StringIO
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from django.core.files.base import ContentFile

from django.core.files.storage import default_storage

from files.models import File
from tasks.models import Task
from celery import shared_task


@shared_task
def analytics(pk, file_id):
    path = File.objects.get(pk=file_id).file.path
    task = Task.objects.get(pk=pk)
    task.status = task.PROCESSING
    task.save()
    try:
        with default_storage.open(path, 'rb') as file:
            df = pd.read_csv(StringIO(file.read().decode('utf-8')))
        f(df, task)
        task.status = task.COMPLETE
        task.save()
    except (Exception, FileNotFoundError) as exception:
        print("ERROR", exception)
        task.status = task.ERROR
        task.save()



#
# # Словарь с соответствием английских и русских названий столбцов
# column_mapping = {
#     'SKU': 'Артикул',
#     'Name': 'Наименование',
#     'Category': 'Категория',
#     'Brand': 'Бренд',
#     'Seller': 'Продавец',
#     'Deliveryscheme': 'Схема доставки',
#     'Balance': 'Остаток',
#     'Comments': 'Комментарии',
#     'Rating': 'Рейтинг',
#     'Price': 'Цена',
#     'Max price': 'Максимальная цена',
#     'Min price': 'Минимальная цена',
#     'Average price': 'Средняя цена',
#     'Sales': 'Продажи',
#     'Revenue': 'Выручка',
#     'Revenue potential': 'Потенциальная выручка',
#     'Lost profit': 'Потерянная прибыль',
#     'Days in stock': 'Дней в наличии',
#     'Days with sales': 'Дней с продажами',
#     'Average if in stock': 'Среднее при наличии',
#     'URL': 'Ссылка',
#     'Photo': 'Фото',
#     'full_category': 'Полная категория'
# }


def save_graph(graph, task, description):
    plot_file_path = f"{uuid.uuid4()}.png"
    graph.savefig(plot_file_path, dpi=300, bbox_inches='tight')
    graph.clf()

    file_instance = File.objects.create()
    file_instance.description = description
    with open(plot_file_path, 'rb') as file:
        file_instance.file.save('plot.png', ContentFile(file.read()), save=True)
        task.files.add(file_instance)

    os.remove(plot_file_path)


def f(data, task):
    # data = data.rename(columns=column_mapping)
    # data = data.drop_duplicates()
    #
    # count_delivery_ozon = 0
    # delivery_ozon = []
    # delivery_NOT_ozon = []
    # other = []
    #
    # for i in data['Продавец']:
    #     if 'доставка OZON' in i:
    #         count_delivery_ozon += 1
    #         delivery_ozon.append(i)
    #     elif not 'OZON' in i:
    #         delivery_NOT_ozon.append(i)
    #     else:
    #         other.append(i)
    #
    # # Создаем список для оси X (продавцы)
    # sellers = ['Доставка от OZON', 'Собственная доставка']
    # # Создаем список для оси Y (количество продавцов)
    # counts = [len(set(delivery_ozon)), len(set(delivery_NOT_ozon))]
    #
    # # Строим столбчатую диаграмму
    # plt.bar(sellers, counts, color=['pink', 'skyblue'])
    # plt.xlabel('Тип доставки')
    # plt.ylabel('Количество продавцов')
    # plt.title('Распределение продавцов по типам доставки')
    #
    # # Добавляем текстовые метки с точным количеством
    # for i, count in enumerate(counts):
    #     plt.text(i, count + 0.1, str(count), ha='center', va='bottom')
    #
    # save_graph(plt, task)
    #
    # # Группировка данных по схеме доставки и подсчет уникальных продавцов
    # seller_counts_by_delivery_scheme = data.groupby('Схема доставки')['Продавец'].nunique()
    #
    # # Разные цвета для столбцов
    # colors = ['skyblue', 'lightgreen', 'lightcoral', 'gold', 'lightblue']
    #
    # # Визуализация данных в виде столбчатой диаграммы
    # ax = seller_counts_by_delivery_scheme.plot(kind='bar', color=colors)
    # plt.xlabel('Схема доставки')
    # plt.ylabel('Количество уникальных продавцов')
    # plt.title('Распределение продавцов по схеме доставки')
    #
    # # Добавление точного количества на график
    # for i, v in enumerate(seller_counts_by_delivery_scheme):
    #     ax.text(i, v + 0.1, str(v), ha='center', va='bottom')
    #
    # plt.xticks(rotation=45, ha='right')  # Добавляем поворот меток оси X для удобства чтения
    # save_graph(plt, task)
    #
    # # Создаем новый столбец 'Категория' без последнего элемента
    # data['Новая категория'] = data['Категория'].apply(lambda x: '/'.join(x.split('/')[:-1]))
    #
    # # Создадим DataFrame с группировкой по 'Категория'
    # category_stats = data.groupby('Новая категория').agg({'Выручка': 'sum', 'Продажи': 'sum'}).reset_index()
    #
    # # Рассчитаем средний чек
    # category_stats['Средний чек'] = category_stats['Выручка'] / category_stats['Продажи']
    #
    # # Сортировка по среднему чеку
    # category_stats_sorted = category_stats.sort_values('Средний чек', ascending=False)
    #
    # # Разделение на верхнюю и нижнюю части
    # top_50_percent = category_stats_sorted.head(int(len(category_stats_sorted) * 0.3))
    # bottom_50_percent = category_stats_sorted.tail(int(len(category_stats_sorted) * 0.7))
    #
    # # Визуализация верхних 50%
    # plt.figure(figsize=(20, 6))
    # plt.bar(range(len(top_50_percent)), top_50_percent['Средний чек'], color='skyblue')
    # plt.xlabel('Категория (Топ-30%)')
    # plt.ylabel('Средний чек')
    # plt.title('Средний чек по категориям (Топ-30%)')
    # plt.xticks([])  # Пустой список для отключения подписей на оси x
    # save_graph(plt, task)
    #
    # # Визуализация нижних 50%
    # plt.figure(figsize=(20, 6))
    # plt.bar(range(len(bottom_50_percent)), bottom_50_percent['Средний чек'], color='skyblue')
    # plt.xlabel('Категория (Последние 70%)')
    # plt.ylabel('Средний чек')
    # plt.title('Средний чек по категориям (Последние 70%)')
    # plt.xticks([])  # Пустой список для отключения подписей на оси x
    # save_graph(plt, task)
    #
    # # Визуализация
    # plt.figure(figsize=(12, 8))
    #
    # plt.scatter(category_stats_sorted['Продажи'], category_stats_sorted['Выручка'], color='blue',
    #             label='Зависимость выручки и продаж')
    #
    # plt.xlabel('Продажи')
    # plt.ylabel('Выручка')
    # plt.title('Зависимость выручки от продаж')
    # plt.legend()
    # save_graph(plt, task)
    #
    # plt.figure(figsize=(20, 6))
    # plt.bar(category_stats_sorted["Новая категория"], category_stats_sorted["Выручка"], color='skyblue')
    # plt.xlabel('Категория')
    # plt.ylabel('Выручка')
    # plt.title('Распределение выручки')
    # plt.xticks([])  # Пустой список для отключения подписей на оси x
    # save_graph(plt, task)
    #
    # plt.figure(figsize=(20, 6))
    # plt.bar(category_stats_sorted["Новая категория"], category_stats_sorted["Продажи"], color='skyblue')
    # plt.xlabel('Категория')
    # plt.ylabel('Продажи')
    # plt.title('Распределение продаж')
    # plt.xticks([])  # Пустой список для отключения подписей на оси x
    # save_graph(plt, task)

    # # Группировка данных по продавцам и подсчет уникальных брендов
    # seller_brand_counts = data.groupby('Продавец')['Бренд'].nunique().reset_index()
    #
    # # Переименование колонки 'Бренд' на 'Количество брендов'
    # seller_brand_counts = seller_brand_counts.rename(columns={'Бренд': 'Количество брендов'})
    #
    # # Топ-N продавцов с самым большим количеством брендов
    # top_n = 40
    # top_sellers = seller_brand_counts.nlargest(top_n, 'Бренд')
    #
    # # Визуализация данных
    # plt.figure(figsize=(10, 6))
    # plt.bar(top_sellers['Продавец'], top_sellers['Бренд'], color='skyblue')
    # plt.xticks(rotation=45, ha='right')
    # plt.xlabel('Продавец')
    # plt.ylabel('Количество уникальных брендов')
    # plt.title(f'Tоп-{top_n} продавцов с самым большим количеством брендов')
    # plt.tight_layout()
    # save_graph(plt, task)
    #
    # # Подсчет количества продавцов для каждого количества уникальных брендов
    # brand_counts_distribution = seller_brand_counts['Бренд'].value_counts().reset_index()
    # brand_counts_distribution.columns = ['Количество брендов', 'Количество продавцов']
    #
    # # Визуализация данных в виде круговой диаграммы
    # plt.figure(figsize=(8, 8))
    # plt.pie(brand_counts_distribution['Количество продавцов'], labels=brand_counts_distribution['Количество брендов'],
    #         autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    # plt.title('Распределение количества продавцов по количеству брендов')
    # save_graph(plt, task)
    # Разделение данных на макароны в пачках
    pasta_in_packages = data[data['Количество'].apply(lambda x: x.is_integer())]

    # Разделение данных на макароны на развесе
    pasta_on_weight = data[~data['Количество'].apply(lambda x: x.is_integer())]
    # Группировка данных по товарной группе и коду товара для макарон в пачках И на развес
    grouped_data_packages = pasta_in_packages.groupby(['Товарная группа', 'Код товара', 'Наименование товара'])
    total_quantity_revenue_packages = grouped_data_packages.agg(
        {'Количество': 'sum', 'Сумма к оплате': 'sum'}).reset_index()

    grouped_data_weight = pasta_on_weight.groupby(['Товарная группа', 'Код товара', 'Наименование товара'])
    total_quantity_revenue_weight = grouped_data_weight.agg(
        {'Количество': 'sum', 'Сумма к оплате': 'sum'}).reset_index()

    # Сортировка по убыванию суммарного количества продаж
    total_quantity_revenue_packages = total_quantity_revenue_packages.sort_values(by='Количество', ascending=False)
    total_quantity_revenue_weight = total_quantity_revenue_weight.sort_values(by='Количество', ascending=False)

    sns.set(font_scale=0.8)
    plt.figure(figsize=(16, 22))
    sns.barplot(x='Количество', y='Наименование товара', data=total_quantity_revenue_packages, palette='viridis')
    plt.title('Диаграмма продаж макарон в пачках (Количество пачек)')
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")
    save_graph(plt, task, description)

    # макароны на развес
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Количество', y='Наименование товара', data=total_quantity_revenue_weight, palette='viridis')
    plt.title('Диаграмма продаж макарон на развес (Количество проданных килограмм)')
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")
    save_graph(plt, task, description)

    # Выручка в рублях, макароны в пачках
    # Установка размера шрифта
    sns.set(font_scale=0.8)
    plt.figure(figsize=(16, 22))
    sns.barplot(x='Сумма к оплате', y='Наименование товара', data=total_quantity_revenue_packages, palette='viridis')
    plt.title('Выручка в рублях. Макароны в ПАЧКАХ')
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")
    save_graph(plt, task, description)

    # Выручка в рублях, макароны на развес
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Сумма к оплате', y='Наименование товара', data=total_quantity_revenue_weight, palette='viridis')
    plt.title('Выручка в рублях. Макароны на РАЗВЕС')
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")
    save_graph(plt, task, description)
