import os
import uuid
from io import StringIO

import numpy as np
import pandas as pd
from django.core.files.base import ContentFile

from django.core.files.storage import default_storage

from files.models import File
from tasks.models import Task, Graph
from celery import shared_task

from tasks.serializers import SupplySerializer

import plotly.express as px
import plotly.io as pio
from apyori import apriori
from itertools import chain


@shared_task
def analytics(pk, file_id):
    path = File.objects.get(pk=file_id).file.path
    task = Task.objects.get(pk=pk)
    task.status = task.PROCESSING
    task.save()
    try:

        with default_storage.open(path, 'rb') as file:
            df = pd.read_csv(StringIO(file.read().decode('utf-8')))
        if task.delivery:
            delivery(df, task)
        else:
            f(df, task)
        task.status = task.COMPLETE
        task.save()
    except (Exception, FileNotFoundError) as exception:
        task.status = task.ERROR
        task.save()
        raise exception


def save_graph(graph, task, title, description):
    plot_file_path = f"{uuid.uuid4()}.png"
    graph.savefig(plot_file_path, dpi=300, bbox_inches='tight')
    graph.clf()

    file_instance = File.objects.create()
    file_instance.description = description
    file_instance.title = title
    with open(plot_file_path, 'rb') as file:
        file_instance.file.save('plot.png', ContentFile(file.read()), save=True)
        task.files.add(file_instance)

    os.remove(plot_file_path)


def save_plotly_express_graph(fig, task, title, description):
    plot_file_path = f"{uuid.uuid4()}.png"

    # Сохранение графика в файл с использованием Plotly
    pio.write_image(fig, plot_file_path)

    # Создание экземпляра файла и сохранение в базу данных
    file_instance = File.objects.create()
    file_instance.description = description
    file_instance.title = title

    with open(plot_file_path, 'rb') as file:
        file_instance.file.save('plot.png', ContentFile(file.read()), save=True)
        task.files.add(file_instance)

    # Удаление временного файла
    os.remove(plot_file_path)


def f(data, task):
    # Разделение данных на макароны в пачках
    pasta_in_packages = data[data['Количество'].apply(lambda x: x.is_integer())]

    # Разделение данных на макароны на развесе
    pasta_on_weight = data[~data['Количество'].apply(lambda x: x.is_integer())]

    # Суммирование количества и общей выручки для каждой категории
    quantity_in_packages = pasta_in_packages['Количество'].sum()
    quantity_on_weight = pasta_on_weight['Количество'].sum()

    total_revenue_in_packages = pasta_in_packages['Сумма к оплате'].sum()
    total_revenue_on_weight = pasta_on_weight['Сумма к оплате'].sum()

    # Построение круговой диаграммы для соотношения количества
    labels_quantity = ['Макароны в упаковках', 'Макароны на весу']
    sizes_quantity = [quantity_in_packages, quantity_on_weight]

    graph = Graph.objects.create(
        title="Соотношение количества макарон в упаковках и на весу",
        description="description",
        x_axis=labels_quantity,
        y_axis=sizes_quantity,
        x_title="Названия",
        y_title="Значения",
        type_graph=Graph.PIE,

    )
    task.graphs.add(graph)

    # Построение круговой диаграммы для соотношения по общей выручке
    labels_revenue = ['Выручка от макарон в упаковках', 'Выручка от макарон на весу']
    sizes_revenue = [total_revenue_in_packages, total_revenue_on_weight]

    graph = Graph.objects.create(
        title="Соотношение по общей выручке от макарон в упаковках и на весу",
        description="description",
        x_axis=labels_revenue,
        y_axis=sizes_revenue,
        x_title="Названия",
        y_title="Значения",
        type_graph=Graph.PIE,

    )
    task.graphs.add(graph)

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

    title = "№1. Распределение товаров по продажам в пачках"
    description = ("Данный график предоставляет диаграмму продаж каждого товара в штуках, начиная с"
                   " самого большого количества продаж за период и передвигаясь к самому маленькому. <br>"
                   "Ось y - наименование товара, ось х - количество проданных штук.")

    graph = Graph.objects.create(
        title=title,
        description=description,
        x_axis=list(total_quantity_revenue_packages['Количество']),
        y_axis=list(total_quantity_revenue_packages['Наименование товара']),
        x_title="Количество",
        y_title="Наименование товара",

    )
    task.graphs.add(graph)

    title = "№2. Распределение товаров по продажам на развес"
    description = ("Данный график предоставляет диаграмму продаж каждого товара в киллограммах, начиная с"
                   " самого большого количества продаж за период и передвигаясь к самому маленькому.<br>"
                   "Ось y - наименование товара, ось х - количество проданных киллограмм товара.")

    graph = Graph.objects.create(
        title=title,
        description=description,
        x_axis=list(total_quantity_revenue_weight['Количество']),
        y_axis=list(total_quantity_revenue_weight['Наименование товара']),
        x_title="Количество",
        y_title="Наименование товара",

    )
    task.graphs.add(graph)

    title = "№3. Распределение выручки за товары в пачках"
    description = ("На данном графике отображается суммарная выручка за период по каждому наименованию товара."
                   " Обратите внимание, что наименования отсортированы, как на графике продаж в штуках, для удобства "
                   "анализа количества проданных штук и суммы, на которую они были проданы. <br>"
                   "Ось у - наименование товара, ось х - сумма, на которую продан товар за период.")

    graph = Graph.objects.create(
        title=title,
        description=description,
        x_axis=list(total_quantity_revenue_packages['Сумма к оплате']),
        y_axis=list(total_quantity_revenue_packages['Наименование товара']),
        x_title="Сумма к оплате",
        y_title="Наименование товара",

    )
    task.graphs.add(graph)

    title = "№4. Распределение выручки за товары на развес"
    description = ("На данном графике отображается суммарная выручка за период по каждому наименованию товара. "
                   "Обратите внимание, что наименования отсортированы, как на графике продаж в киллограммах, "
                   "для удобства"
                   " анализа количества проданных киллограмм и суммы, на которую они были проданы. <br>"
                   "Ось у - наименование товара, ось х - сумма, на которую продан товар за период.")

    graph = Graph.objects.create(
        title=title,
        description=description,
        x_axis=list(total_quantity_revenue_weight['Сумма к оплате']),
        y_axis=list(total_quantity_revenue_weight['Наименование товара']),
        x_title="Сумма к оплате",
        y_title="Наименование товара",

    )
    task.graphs.add(graph)

    #####Диаграммы совместных временных рядов продаж по времени первых (20% от общего числа) самых популярных артикулов на каждую неделю

    # топ 20% товаров
    top_20_percent = total_quantity_revenue_packages.head(int(0.2 * len(total_quantity_revenue_packages)))

    # Объединение данных с исходными транзакциями
    merged_data = pd.merge(data, top_20_percent[['Товарная группа', 'Код товара']],
                           on=['Товарная группа', 'Код товара'])

    # Преобразование столбца 'Дата' в формат datetime
    merged_data['Дата'] = pd.to_datetime(merged_data['Дата'])

    # Группировка данных по товару и неделе
    weekly_data = merged_data.groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара', pd.Grouper(key='Дата', freq='W')])

    # Суммарное количество продаж по каждой неделе
    weekly_quantity = weekly_data['Количество'].sum().reset_index()

    # Объединение данных с исходными транзакциями
    merged_data_2 = pd.merge(data, total_quantity_revenue_weight[['Товарная группа', 'Код товара']],
                             on=['Товарная группа', 'Код товара'])

    # Преобразование столбца 'Дата' в формат datetime
    merged_data_2['Дата'] = pd.to_datetime(merged_data_2['Дата'])

    # Группировка данных по товару и неделе
    weekly_data_2 = merged_data_2.groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара', pd.Grouper(key='Дата', freq='W')])

    # Суммарное количество продаж по каждой неделе
    weekly_quantity_2 = weekly_data_2['Количество'].sum().reset_index()
    weekly_quantity_2['Дата'] = weekly_quantity_2['Дата'].dt.strftime('%Y-%m-%d')

    # Преобразование данных в формат, подходящий для Plotly Express
    fig_data = weekly_quantity.melt(id_vars=['Дата', 'Наименование товара'], value_vars='Количество',
                                    var_name='Метрика', value_name='Значение')

    title = "№5. Распределение продаж по неделям. Товары в пачках"
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")

    x_axis = fig_data["Дата"].dt.strftime('%Y-%m-%d').tolist()
    y_axis = []

    for name in set(weekly_quantity["Наименование товара"]):
        filtered_data = weekly_quantity[weekly_quantity["Наименование товара"] == name]
        y_axis.append({
            "дата": filtered_data["Дата"].dt.strftime('%Y-%m-%d').tolist(),
            "Наименование товара": name,
            "Количество": filtered_data["Количество"].to_list(),
        })

    graph = Graph.objects.create(
        title=title,
        description=description,
        x_axis=x_axis,
        y_axis=y_axis,
        x_title="Дата",
        y_title="Значение",
        type_graph=Graph.LINE,

    )
    task.graphs.add(graph)

    # Преобразование данных в формат, подходящий для Plotly Express
    fig_data = weekly_quantity_2.melt(id_vars=['Дата', 'Наименование товара'], value_vars='Количество',
                                      var_name='Метрика', value_name='Значение')
    # Отображение графика
    title = "№6. Распределение продаж по неделям. Товары на развес"
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")

    fig_data['Дата'] = pd.to_datetime(fig_data['Дата'])
    x_axis = fig_data["Дата"].dt.strftime('%Y-%m-%d').tolist()
    y_axis = []

    for name in set(weekly_quantity_2["Наименование товара"]):
        filtered_data = weekly_quantity_2[weekly_quantity_2["Наименование товара"] == name]
        filtered_data['Дата'] = pd.to_datetime(filtered_data['Дата'])
        y_axis.append({
            "дата": filtered_data["Дата"].dt.strftime('%Y-%m-%d').tolist(),
            "Наименование товара": name,
            "Количество": filtered_data["Количество"].to_list(),
        })

    graph = Graph.objects.create(
        title=title,
        description=description,
        x_axis=x_axis,
        y_axis=y_axis,
        x_title="Дата",
        y_title="Значение",
        type_graph=Graph.LINE,

    )
    task.graphs.add(graph)

    # Группировка данных по товару и дате
    cumulative_data = weekly_quantity.groupby(['Товарная группа', 'Код товара', 'Наименование товара', 'Дата'])

    # Кумулятивная сумма продаж по каждому товару
    cumulative_quantity = cumulative_data['Количество'].sum().groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара']).cumsum().reset_index()
    # Визуализация диаграммы накопления количества проданных товаров с использованием Plotly
    fig = px.line(cumulative_quantity, x='Дата', y='Количество', color='Наименование товара',
                  labels={'Количество': 'Кумулятивная сумма'})
    # # Включение всплывающих подсказок
    fig.update_traces(mode='lines+markers', hovertemplate='Дата: %{x}<br>Количество: %{y}')
    # # Легенда
    fig.update_layout(legend=dict(x=1, y=0.5))
    fig.update_layout(height=900, width=1500)
    # Отображение графика
    title = "№7. Диаграмма накопления количества проданных товаров по пачкам"
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")

    # TODO SAVE GRAPH
    save_plotly_express_graph(fig, task, title, description)

    # Группировка данных по товару и дате
    cumulative_data_2 = weekly_quantity_2.groupby(['Товарная группа', 'Код товара', 'Наименование товара', 'Дата'])

    # Кумулятивная сумма продаж по каждому товару
    cumulative_quantity_2 = cumulative_data_2['Количество'].sum().groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара']).cumsum().reset_index()

    # Визуализация диаграммы накопления количества проданных товаров с использованием Plotly
    fig = px.line(cumulative_quantity_2, x='Дата', y='Количество', color='Наименование товара',
                  labels={'Количество': 'Кумулятивная сумма'})
    # # Включение всплывающих подсказок
    fig.update_traces(mode='lines+markers', hovertemplate='Дата: %{x}<br>Количество: %{y}')
    # # Легенда
    fig.update_layout(legend=dict(x=1, y=0.5))
    fig.update_layout(height=900, width=1500)
    # Отображение графика
    title = "№8. Диаграмма накопления количества проданных товаров на развес"
    description = ("На данном графике блаблабл балабал балбала балабала аблаала аблалаба"
                   "балалаллаба аллбалалба аблалала аба лалба абалабабалалабаблалалбабалла"
                   "алаабалблбалбалалбаблаблалалалааблаблалалбалбла")
    # TODO SAVE GRAPH
    save_plotly_express_graph(fig, task, title, description)


def delivery(data, task):
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
    # топ 20% товаров
    top_20_percent = total_quantity_revenue_packages.head(int(0.2 * len(total_quantity_revenue_packages)))

    # Объединение данных с исходными транзакциями
    merged_data = pd.merge(data, top_20_percent[['Товарная группа', 'Код товара']],
                           on=['Товарная группа', 'Код товара'])

    # Преобразование столбца 'Дата' в формат datetime
    merged_data['Дата'] = pd.to_datetime(merged_data['Дата'])

    # Группировка данных по товару и неделе
    weekly_data = merged_data.groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара', pd.Grouper(key='Дата', freq='W')])

    # Суммарное количество продаж по каждой неделе
    weekly_quantity = weekly_data['Количество'].sum().reset_index()
    # Объединение данных с исходными транзакциями
    merged_data_2 = pd.merge(data, total_quantity_revenue_weight[['Товарная группа', 'Код товара']],
                             on=['Товарная группа', 'Код товара'])

    # Преобразование столбца 'Дата' в формат datetime
    merged_data_2['Дата'] = pd.to_datetime(merged_data_2['Дата'])

    # Группировка данных по товару и неделе
    weekly_data_2 = merged_data_2.groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара', pd.Grouper(key='Дата', freq='W')])

    # Суммарное количество продаж по каждой неделе
    weekly_quantity_2 = weekly_data_2['Количество'].sum().reset_index()
    # Группировка данных по товару и дате
    cumulative_data = weekly_quantity.groupby(['Товарная группа', 'Код товара', 'Наименование товара', 'Дата'])

    # Кумулятивная сумма продаж по каждому товару
    cumulative_quantity = cumulative_data['Количество'].sum().groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара']).cumsum().reset_index()

    # Группировка данных по товару и дате
    cumulative_data_2 = weekly_quantity_2.groupby(['Товарная группа', 'Код товара', 'Наименование товара', 'Дата'])

    # Кумулятивная сумма продаж по каждому товару
    cumulative_quantity_2 = cumulative_data_2['Количество'].sum().groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара']).cumsum().reset_index()

    # Объединение данных с исходными транзакциями
    merged_data = pd.merge(data, total_quantity_revenue_packages[['Товарная группа', 'Код товара']],
                           on=['Товарная группа', 'Код товара'])

    # Преобразование столбца 'Дата' в формат datetime
    merged_data['Дата'] = pd.to_datetime(merged_data['Дата'])

    # Группировка данных по товару и неделе
    weekly_data = merged_data.groupby(
        ['Товарная группа', 'Код товара', 'Наименование товара', pd.Grouper(key='Дата', freq='W')])

    # Суммарное количество продаж по каждой неделе
    weekly_quantity = weekly_data['Количество'].sum().reset_index()
    average_intensity = weekly_quantity.groupby(['Товарная группа', 'Код товара', 'Наименование товара'])[
        'Количество'].mean().reset_index()
    average_intensity = average_intensity.sort_values(by=['Товарная группа', 'Код товара', 'Наименование товара'],
                                                      ascending=[True, True, True])
    average_intensity_2 = \
        weekly_quantity.groupby(
            ['Товарная группа', 'Код товара', 'Наименование товара', pd.Grouper(key='Дата', freq='W')])[
            'Количество'].mean().reset_index()
    average_intensity_2 = average_intensity_2.sort_values(
        by=['Товарная группа', 'Код товара', 'Наименование товара', 'Дата'], ascending=[True, True, True, True])

    quantile_25 = weekly_quantity.groupby(['Товарная группа', 'Код товара', 'Наименование товара'])[
        'Количество'].quantile(0.25)
    quantile_75 = weekly_quantity.groupby(['Товарная группа', 'Код товара', 'Наименование товара'])[
        'Количество'].quantile(0.75)
    quantile_95 = weekly_quantity.groupby(['Товарная группа', 'Код товара', 'Наименование товара'])[
        'Количество'].quantile(0.95)

    # Объединение данных
    merged_quantiles_df = pd.merge(quantile_25, quantile_75, left_index=True, right_index=True, suffixes=('_25', '_75'))
    merged_quantiles_df = pd.merge(merged_quantiles_df, quantile_95, left_index=True, right_index=True,
                                   suffixes=('', '_95'))
    merged_quantiles_df = pd.merge(merged_quantiles_df, average_intensity.reset_index(),
                                   on=['Товарная группа', 'Наименование товара']).drop(columns=['index'])

    # Переименование столбцов
    merged_quantiles_df.columns = ['Товарная группа', 'Наименование товара', '0.25-квантиль', '0.75-квантиль',
                                   '0.95-квантиль', 'Код товара', 'Средний расход']

    # Фильтрация товаров, где квантили 25 и 75 совпадают
    same_quantiles_products = merged_quantiles_df[
        merged_quantiles_df['0.25-квантиль'] == merged_quantiles_df['0.75-квантиль']]

    # Подсчет количества каждого сочетания
    quantiles_combinations_count = same_quantiles_products.groupby(
        ['0.25-квантиль', '0.75-квантиль']
    ).size().reset_index(name='Количество')

    all_deliveries = []

    for selected_product in data['Наименование товара'].unique():
        # Фильтрация данных для выбранного товара
        product_data = data[data['Наименование товара'] == selected_product].copy()

        # Преобразование столбца 'Дата' в формат datetime
        product_data.loc[:, 'Дата'] = pd.to_datetime(product_data['Дата'])

        # Получение параметров товара из таблицы с квантилями
        quantiles_row = merged_quantiles_df[merged_quantiles_df['Наименование товара'] == selected_product]

        if not quantiles_row.empty:
            quantiles_row = quantiles_row.iloc[0]
            quantile_25 = quantiles_row['0.25-квантиль']
            quantile_75 = quantiles_row['0.75-квантиль']
            quantile_95 = quantiles_row['0.95-квантиль']
        else:
            # Обработка случая, когда продукт не найден в merged_quantiles_df
            # print(f"Квантили не найдены для {selected_product}. Пропуск.")
            continue  # Переход к следующему продукту

        # Инициализация переменных для каждого продукта
        if len(product_data) > 1:
            storage_cost_per_week = product_data['Сумма по прейскуранту'].iloc[1] * 0.07
            current_date = min(product_data['Дата'])  # первая дата поставки
            current_stock = 0  # текущий остаток на складе
            deliveries = []  # данные о каждой поставке
            count_of_oversupply = 0
            current_stock_start = 0
            lost_revenue = 0

            # Симуляция поставок и продаж
            for index, row in product_data.iterrows():
                # если дата в текущей строке больше чем current_date
                if row['Дата'] > current_date:
                    # Выбор квантиля в зависимости от остатка
                    if current_stock >= (np.ceil(quantile_95)) and count_of_oversupply >= 0:
                        count_of_oversupply += 1
                        delivery_quantity = np.ceil(quantile_25)  # поставка 25 квантиль
                    else:
                        count_of_oversupply = 0
                        delivery_quantity = np.ceil(quantile_95)  # возвращаемся к 95 квантиль

                    current_stock_start += delivery_quantity
                    current_stock += delivery_quantity  # увеличиваем текущий остаток
                    storage_cost = current_stock * storage_cost_per_week  # стоимость хранения, учитывая колво товара

                    # Подсчет продаж за неделю
                    weekly_sales_quantity = product_data[(product_data['Дата'] >= current_date) & (
                            product_data['Дата'] < current_date + pd.DateOffset(7))]['Количество'].sum()
                    weekly_sales_value = product_data[(product_data['Дата'] >= current_date) & (
                            product_data['Дата'] < current_date + pd.DateOffset(7))]['Сумма к оплате'].sum()

                    # Проверка, хватит ли товара на неделю
                    if current_stock >= weekly_sales_quantity:
                        current_stock -= weekly_sales_quantity
                    else:
                        current_stock = 0

                    lost_revenue = current_stock_start - weekly_sales_quantity  # упущенная выручка
                    if lost_revenue < 0:
                        lost_revenue *= product_data['Сумма по прейскуранту'].iloc[1]
                    else:
                        lost_revenue = 0

                    # Запись данных о поставке
                    deliveries.append({
                        'Наименование товара': selected_product,
                        'Дата': current_date,
                        'Поставка, шт': delivery_quantity,
                        'Остаток на начало недели, шт': current_stock_start,
                        'Продажи за неделю, шт': weekly_sales_quantity,
                        'Остаток на складе, шт': current_stock,
                        'Стоимость хранения за неделю, руб': storage_cost,
                        'Прибыль от продаж, руб': weekly_sales_value,
                        'Чистая прибыль': weekly_sales_value - storage_cost,
                        'Упущенная выручка, руб': lost_revenue
                    })

                    if current_stock_start >= weekly_sales_quantity:
                        current_stock_start -= weekly_sales_quantity
                    else:
                        current_stock_start = 0

                    lost_revenue = 0
                    # Обновление текущей даты
                    current_date += pd.DateOffset(7)

            # Append results for the current product to the overall list
            all_deliveries.extend(deliveries)
        # else:
        #     print(f"Недостаточно строк в DataFrame для {selected_product}")

    # Создание и вывод таблицы с поставками для всех товаров
    all_deliveries_df = pd.DataFrame(all_deliveries)
    # Словарь для соответствия имен столбцов CSV и полей в сериализаторе
    column_mapping = {
        'Наименование товара': 'name',
        'Дата': 'date',
        'Поставка, шт': 'supply',
        'Остаток на начало недели, шт': 'balance_first',
        'Продажи за неделю, шт': 'sell',
        'Остаток на складе, шт': 'balance_storage',
        'Стоимость хранения за неделю, руб': 'price_storage',
        'Прибыль от продаж, руб': 'profit',
        'Чистая прибыль': 'profit_clean',
        'Упущенная выручка, руб': 'profit_missed',
    }

    for index, row in all_deliveries_df.iterrows():
        row = row.to_dict()
        row = {column_mapping[key]: value for key, value in row.items()}
        row['task'] = task.id
        supply_serializer = SupplySerializer(data=row)
        if supply_serializer.is_valid():
            supply_serializer.save()

    # Фильтрация данных: удаление строк, где номер карты представлен как '<..>'
    filtered_data = data[data['Номер Карты'] != '<..>']

    # Группировка данных по дате и номеру карты, сбор товаров в каждой группе
    grouped_data = filtered_data.groupby(['Дата', 'Номер Карты'])['Наименование товара'].apply(list).reset_index()

    # Преобразование сгруппированных данных в формат, поддерживаемый библиотекой apyori
    transactions = grouped_data['Наименование товара'].values.tolist()

    # Разворачивание списков транзакций в один плоский список
    all_items = list(chain.from_iterable(transactions))

    # Создание DataFrame с колонкой 'Item' и подсчетом встречаемости каждого товара
    item_counts = pd.Series(all_items).value_counts().reset_index()
    item_counts.columns = ['Item', 'Count']

    # Выбор топ-10 часто встречаемых товаров
    top_items = item_counts.head(10)

    graph = Graph.objects.create(
        title="Топ-10 часто встречаемых товаров",
        description="description",
        x_axis=list(top_items['Count']),
        y_axis=list(top_items['Item']),
        x_title="Частота",
        y_title="Наименование товара",

    )
    task.graphs.add(graph)

    # Построение модели с использованием алгоритма apriori
    rules = apriori(transactions, min_support=0.001, min_confidence=0.2)
    results = list(rules)

    # Разбор и вывод результатов
    result = ''
    for rule in results:

        items = ', '.join(rule.items)
        support = round(rule.support, 4)

        result += f"Товары: {items}\n"

        result += f"Support: {support}\n"

        for stat in rule.ordered_statistics:
            confidence = round(stat.confidence, 4)
            lift = round(stat.lift, 4)
            items_base = ', '.join(stat.items_base)
            items_add = ', '.join(stat.items_add)

            result += f"  Правило: {items_base} => {items_add}\n"
            result += f"    Confidence: {confidence}\n"
            result += f"    Lift: {lift}\n"

        result += "=" * 50 + "\n"

    result += ";"

    result += 'Прибыль за весь период: ' + str(round(all_deliveries_df['Прибыль от продаж, руб'].sum())) + ' рублей\n'
    result += 'Чистая прибыль за весь период: ' + str(round(all_deliveries_df['Чистая прибыль'].sum())) + ' рублей\n'
    result += 'Упущенная выручка: ' + str(round(all_deliveries_df['Упущенная выручка, руб'].sum())) + ' рублей\n'

    task.text = result
