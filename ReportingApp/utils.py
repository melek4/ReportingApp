import base64
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from datetime import date
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    plt.close()
    return graph


def get_Age_Genre_Barplot(x, y):
    plt.switch_backend('AGG')
    labels = ['25-29 ans', '30-34 ans', '35-39 ans',
              '40-44 ans', '45-49 ans', '50-55 ans', '55 ans et+']
    plt.figure(figsize=(8, 4))
    plt.bar(labels, x, label='Hommes', color='#00589C')
    plt.bar(labels, y, bottom=x, label='Femmes', color='#016FC4')
    plt.legend()
    plt.title('Age/Genre')
    plt.tight_layout()
    # plt.xticks(rotation=45)
    graph = get_graph()
    plt.close()
    return graph


def get_Age_Category_Barplot(w, x, y, z):
    YBottom = [0, 0, 0, 0, 0, 0, 0]
    ZBottom = [0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 7):
        YBottom[i] = w[i]+x[i]
        ZBottom[i] = w[i]+x[i]+y[i]

    plt.switch_backend('AGG')
    labels = ['25-29 ans', '30-34 ans', '35-39 ans',
              '40-44 ans', '45-49 ans', '50-55 ans', '55 ans et+']
    plt.figure(figsize=(8, 4))
    plt.bar(labels, w, label='Cadre', color='#00589C')
    plt.bar(labels, x, bottom=w, label='Maitrise', color='#016FC4')
    plt.bar(labels, y, bottom=YBottom, label='Execution', color='#1891C3')
    plt.bar(labels, z, bottom=ZBottom,
            label='Execution-Maitrise', color='#3AC0DA')
    plt.legend()
    plt.title('Age/Catégorie professionnelle')
    plt.tight_layout()
    # plt.xticks(rotation=45)
    graph = get_graph()
    plt.close()
    return graph


def get_Abs_Repartition_Donut_Chart(list_headings, list_percent, list_values):
    plt.pie(list_values, autopct='%1.1f%%',
            pctdistance=0.85)
    # centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    # fig = plt.gcf()
    # fig.gca().add_artist(centre_circle)
    plt.legend(list_headings, bbox_to_anchor=(1.5, 1),
               loc="upper right",)
    plt.title('Motifs/Nombre de jours')
    graph = get_graph()
    plt.close()
    return graph


def get_Days_Sex_Barplot(list_headings, list_values_F, list_values_H):

    plt.switch_backend('AGG')
    plt.bar(list_headings, list_values_H, label='Hommes', color='#00589C')
    plt.bar(list_headings, list_values_F, bottom=list_values_H,
            label='Femmes', color='#016FC4')
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=90)
    plt.title('Nombre de jours/Motif/Genre')
    graph = get_graph()
    plt.close()
    return graph


def get_Abs_Cat_Sex(C_data, M_data, E_data, EM_data):
    Female_data = [0, 0, 0, 0]
    Male_data = [0, 0, 0, 0]
    plt.switch_backend('AGG')
    labels = ['Cadre', 'Maitrise', 'Execution', 'Execution Maitrise']
    Female_data[0] = C_data[0]
    Female_data[1] = M_data[0]
    Female_data[2] = E_data[0]
    Female_data[3] = EM_data[0]
    Male_data[0] = C_data[1]
    Male_data[1] = M_data[1]
    Male_data[2] = E_data[1]
    Male_data[3] = EM_data[1]
    plt.figure(figsize=(8, 4))

    plt.barh(labels, Female_data, label='Femmes', color='#00589C')
    plt.barh(labels, Male_data, left=Female_data,
             label='Hommes', color='#016FC4')
    plt.legend()
    plt.tight_layout()
    # plt.xticks(rotation=45)
    graph = get_graph()
    plt.close()
    return graph


def get_Effectifs_Donut_Chart(val1, val2, val3, val4):
    labels = ['Cadre', 'Maitrise', 'Execution',
              'Execution-maitrise']
    list_values = [val1, val2, val3, val4]
    c = ['#00589C', '#016FC4', '#1891C3', '#3AC0DA']
    plt.pie(list_values, autopct='%1.1f%%',
            pctdistance=0.85, labels=labels, labeldistance=1.15, colors=c)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # plt.legend(labels, bbox_to_anchor=(1.5, 1),
    #            loc="upper right",)
    plt.title("Répartition de l'effectif par catégorie")
    graph = get_graph()
    plt.close()
    return graph


def get_Genre_Cat_Prof_Barchart(val1, val2, val3, val4):

    index = ['Cadre', 'Maitrise', 'Execution', 'Execution Maitrise']
    df = pd.DataFrame({'Hommes tech': val1,
                       'Femmes tech': val2, 'Hommes gest': val3, 'Femmes gest': val4}, index=index)
    df.plot.bar(
        rot=0, color={"Hommes tech": "#00589C", "Femmes tech": "#016FC4", "Hommes gest": "#1891C3", "Femmes gest": "#3AC0DA"})
    plt.title("Répartition par Genre*Catégorie*Profil")
    graph = get_graph()
    plt.close()
    return graph


def get_bar_chart_p4(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12):

    val_list1 = [v1, v5, v9]
    val_list2 = [v2, v6, v10]
    val_list3 = [v3, v7, v11]
    val_list4 = [v4, v8, v12]

    y = date.today().year
    index = [y, y-1, y-2]

    df = pd.DataFrame({'Cadres': val_list1,
                       'Maitrise': val_list2, 'Exécution': val_list3, 'Exécution maitrise': val_list4}, index=index)

    df.plot.bar(
        rot=0, color={"Cadres": "#00589C", "Maitrise": "#016FC4", "Exécution": "#1891C3", "Exécution maitrise": "#3AC0DA"})
    plt.title("Evolution de l'effectif")
    graph = get_graph()
    plt.close()
    return graph
