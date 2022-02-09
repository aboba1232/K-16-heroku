from flask import Flask, render_template, request
from io import BytesIO

import pandas as pd
from pandas import *
import numpy as np

app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data_reg_answer_18_19 = pd.read_csv(BytesIO(file.read()))
            # Удалить ненужные колонки из данных регистрации
            data_reg_answer_18_19 = data_reg_answer_18_19.drop(
                ['Отметка времени', 'Укажите адрес Вашей электронной почты',
                 'Укажите Ваш контактный телефон',
                 'Выберите из списка наименование ГМО',
                 'Укажите возможную форму Вашего участия в работе ГМО',
                 'Укажите значимые для Вас темы в работе ГМО',
                 'Даю согласие на обработку персональных данных',
                 'Укажите Ваш уровень владения информационными технологиями'], axis=1)
            mas_fio = data_reg_answer_18_19['Укажите Ваши фамилию, имя и отчество']

            # удаление ОДИНАКОВЫХ ФИО из набора данных в файле регистрации

            new_data_reg_answer_18_19 = pd.DataFrame()
            new_data_reg_answer_18_19 = data_reg_answer_18_19.drop_duplicates(
                subset=['Укажите Ваши фамилию, имя и отчество'])

            # все Nan заменяем на ? (), только после этого все буквы делаем маленькими

            new_data_reg_answer_18_19.fillna('?',
                                             inplace=True)  # inplace=True, чтобы набор изменился после (обновился) замены

            # все ячейки к нижнему регистру привели (это можно делать только для строк) - для файла регистрации

            for column in new_data_reg_answer_18_19.columns:
                new_data_reg_answer_18_19[column] = new_data_reg_answer_18_19[column].str.lower()

            # создание датафрейма data_reg_answer_18_19_drop_dict, в котором будем учреждения и должности заменять цифрами

            data_reg_answer_17_18_drop_dict = pd.DataFrame()
            data_reg_answer_17_18_drop_dict = new_data_reg_answer_18_19.copy(deep=True)

            # In[103]:

            job_cop_1 = data_reg_answer_17_18_drop_dict.drop(
                ['Укажите Вашу квалификационную категорию', 'Укажите место Вашей работы', 'Укажите Вашу дату рождения'],
                axis=1)
            bou = {'сош': 1, 'гимн': 1, 'лицей': 1, 'общеобразовательная': 1, 'детский сад': 2, 'сад': 2, 'боу': 3,
                   'удо': 3, 'станция': 3, 'гцппмсп': 3, 'доу': 3, 'бук': 3, 'ано': 3, 'до': 3}

            # Замена названий учреждений цифрами в датафрейме data_reg_answer_18_19_drop_dict

            for key, val in bou.items():
                data_reg_answer_17_18_drop_dict['Укажите место Вашей работы'] = data_reg_answer_17_18_drop_dict[
                    'Укажите место Вашей работы'].replace(to_replace=r'.*' + key + '.*', value=val, regex=True)

            # приведение всех данных колонки к типу int64 (проверить для каждой из тех колонок, где должны быть цифры)

            data_reg_answer_17_18_drop_dict['Укажите место Вашей работы'].astype('int64')
            data_cop = data_reg_answer_17_18_drop_dict
            dolj = {'дир': 1, 'замдир': 1, 'завуч': 1, 'зав отделом': 1, 'педаг': 3, 'препод': 3, 'учитель': 3,
                    'логопед': 3, 'психолог': 3, 'воспитатель': 3, 'хореограф': 3, 'метод': 2,
                    'концер': 4, 'библ': 4, 'муз': 4, '?': 3, 'заведующий': 1, 'хор': 4, 'инструктор': 3}

            # Замена названий учреждений цифрами в датафрейме data_reg_answer_18_19_drop_dict

            for key, val in dolj.items():
                data_reg_answer_17_18_drop_dict['Укажите Вашу должность'] = data_reg_answer_17_18_drop_dict[
                    'Укажите Вашу должность'].replace(to_replace=r'.*' + key + '.*', value=val, regex=True)

            # приведение всех данных колонки к типу int64 (проверить для каждой из тех колонок, где должны быть цифры)

            data_reg_answer_17_18_drop_dict['Укажите Вашу должность'].astype('int64')

            # In[112]:

            # Замена должностей цифрами: 1 - администрация (директора, замдиректора, завуч, зав отделом, зам)
            # 2 - педагоги (педаг, препод, учитель, логопед, психолог, воспитатель, хореограф)
            # 3 - методисты (метод)
            # 4 - концертмейстер, библиотекарь, музейный методист (концерт, биб, муз)

            # In[113]:

            # final age - итоговый датафрейм со всеми людьми, которым 45 или больше лет

            # In[114]:

            age = data_reg_answer_17_18_drop_dict

            # In[115]:

            age = age.drop(
                ['Укажите Вашу должность', 'Укажите место Вашей работы', 'Укажите Вашу квалификационную категорию'],
                axis=1)

            # In[116]:

            age.rename(columns={'Укажите Вашу дату рождения': 'Возраст'}, inplace=True)

            # In[117]:

            a = age['Возраст']

            # In[118]:

            a = a.str.slice(start=6)

            # In[119]:

            a = a.astype('int64')

            # In[120]:

            a = 2022 - a

            # In[121]:

            age['Возраст'] = a

            # In[122]:

            final_age = age.loc[age['Возраст'] > 44]

            # In[123]:

            cvalification = data_reg_answer_17_18_drop_dict.loc[
                data_reg_answer_17_18_drop_dict['Укажите Вашу квалификационную категорию'] == 'первая']

            # In[124]:

            cvalification = cvalification.drop(
                ['Укажите Вашу дату рождения', 'Укажите Вашу должность', 'Укажите место Вашей работы'], axis=1)

            # In[125]:

            cvalification.rename(columns={'Укажите Вашу квалификационную категорию': 'Квалификационная категория'},
                                 inplace=True)

            # In[126]:

            job_test = data_reg_answer_17_18_drop_dict

            # In[127]:

            job_test = job_test.drop(
                ['Укажите Вашу квалификационную категорию', 'Укажите место Вашей работы', 'Укажите Вашу дату рождения'],
                axis=1)

            # In[128]:

            job_cop_2 = job_test

            # In[129]:

            job_test['Укажите Вашу должность'] = np.where((job_test['Укажите Вашу должность'] == 2), 0,
                                                          job_test['Укажите Вашу должность'])

            # In[130]:

            job_test['Укажите Вашу должность'] = np.where((job_test['Укажите Вашу должность'] == 4), 0,
                                                          job_test['Укажите Вашу должность'])

            # In[131]:

            final_job = job_test

            # In[132]:

            final_job = final_job.loc[final_job['Укажите Вашу должность'] != 0]

            # In[133]:

            final_job.rename(columns={'Укажите Вашу должность': 'Должность'}, inplace=True)

            # In[134]:

            final_job['Должность'] = final_job['Должность'].astype('str')

            # In[135]:

            dolj = {'1': 'Администрация', '3': 'Методист'}

            # In[136]:

            for key, val in dolj.items():
                final_job['Должность'] = final_job['Должность'].replace(to_replace=r'.*' + key + '.*', value=val,
                                                                        regex=True)
            final_age = final_age.drop(['№'], axis=1)
            final_age = final_age.reset_index()
            final_age = final_age.drop(['index'], axis=1)
            cvalification = cvalification.drop(['№'], axis=1)
            cvalification = cvalification.reset_index()
            cvalification = cvalification.drop(['index'], axis=1)
            final_job = final_job.drop(['№'], axis=1)
            final_job = final_job.reset_index()
            final_job = final_job.drop(['index'], axis=1)
            age_cop = final_age
            cv_cop = cvalification
            job_cop = final_job
            the_desc = age_cop.merge(cv_cop, how='inner')
            job_cop_2 = data_reg_answer_17_18_drop_dict.drop(
                ['Укажите Вашу квалификационную категорию', 'Укажите место Вашей работы', 'Укажите Вашу дату рождения'],
                axis=1)
            the_final_desc = the_desc.merge(job_cop_2, how='left')
            the_final_desc = the_final_desc.sort_values(by='Укажите Вашу должность', ignore_index=True)
            the_final_desc = the_final_desc.drop(['№'], axis=1)
            the_final_desc = the_final_desc.rename(columns={'Укажите Вашу должность': 'b'})
            the_final_desc = the_final_desc.drop('b', axis=1)
            the_final_desc = the_final_desc.merge(job_cop_1, how='left')
            the_final_desc = the_final_desc.drop('№', axis=1)
    return the_final_desc.to_html()
if __name__ == '__main__':
    app.run(debug=True)