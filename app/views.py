from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import pandas as pd
# import scipy.sparse as sp
import numpy as np


def index(request):
   context = {}
   return render(request, 'app/index.html', context)


def chord_diagram(request):
   context = {}
   return render(request, 'app/chord_diagram.html', context)


def upload_data(request):
    """
    Import data from file.
    """
    if request.method == "POST":
        try:
            excel_file = request.FILES['excel']
        except:
            bericht = "Please insert a file."
            messages.info(request, bericht)
            return redirect('index')
        

    # convert excel to pandas dataframe
    df = pd.read_excel(excel_file)
    print(df)
    hot_encoding(df, ["cat", "mouse", "random", "telephone"])
    return redirect('index')


def hot_encoding(df, keywords):
    """
    Create dataframe with binary occurrence of keywords.
    """
    for keyword in keywords:
        df[keyword] = df.text.apply(lambda x: 1 if keyword in x else 0)

    df_hot = df[keywords]
    # correlatiematrix
    matrix = df_hot.corr()
    # negatief gecorreleerde waarden met 0 vervangen en diagonaal weghalen
    matrix[matrix < 0] = 0
    matrix[matrix == 1] = 0
    
    # clean
    matrix = matrix.round(2)
    matrix = matrix.multiply(100).astype(int)

    # labels
    names = matrix.columns
    names = [naam.capitalize() for naam in np.array(names)]
    return JsonResponse({"matrix":  list(matrix), "names": names}, safe=False)
    # cols = df_hot.columns
    # X = sp.csr_matrix(df_hot.astype(int).values)
    # Xc = X.T * X

    # # diagonaal zijn links met zichzelf -> niet meenemen
    # Xc.setdiag(0)

    # # df van co-occurence matrix in dense format
    # df_kern = pd.DataFrame(Xc.todense(), index=cols, columns=cols)
    # df_kern = df_kern.stack().reset_index()
    # df_kern.columns = ['source', 'target', 'weight']

    # # niet-verbonden nodes
    # not_connected = df_kern[df_kern['weight'] == 0]

    # # verwijder niet-verbonden nodes voor diagram
    # df_kern = df_kern[df_kern['weight'] != 0]
    


def data_matrix(request):
    """
    Ajax call om omzet voor elke maand te bepalen.
    """
    matrix = [[0, 0, 0, 12, 6, 0, 6, 0, 13, 0, 12, 4, 3, 6, 0],
      [0, 0, 21, 0, 0, 22, 0, 0, 9, 32, 0, 0, 0, 0, 13],
      [0, 21, 0, 0, 0, 8, 4, 0, 0, 0, 7, 0, 0, 0, 2],
      [12, 0, 0, 0, 2, 4, 2, 2, 4, 6, 0, 14, 15, 14, 11],
      [6, 0, 0, 2, 0, 2, 0, 2, 4, 0, 0, 13, 1, 0, 4],
      [0, 22, 8, 4, 2, 0, 14, 1, 0, 0, 0, 0, 10, 0, 0],
      [6, 0, 4, 2, 0, 14, 0, 0, 0, 0, 9, 0, 6, 0, 0],
      [0, 0, 0, 2, 2, 1, 0, 0, 1, 0, 0, 7, 6, 7, 4],
      [13, 9, 0, 4, 4, 0, 0, 1, 0, 18, 0, 0, 0, 4, 9],
      [0, 32, 0, 6, 0, 0, 0, 0, 18, 0, 1, 0, 0, 0, 17],
      [12, 0, 7, 0, 0, 0, 9, 0, 0, 1, 0, 0, 0, 0, 0],
      [4, 0, 0, 14, 13, 0, 0, 7, 0, 0, 0, 0, 21, 14, 0],
      [3, 0, 0, 15, 1, 10, 6, 6, 0, 0, 0, 21, 0, 4, 0],
      [6, 0, 0, 14, 0, 0, 0, 7, 4, 0, 0, 14, 4, 0, 0],
      [0, 13, 2, 11, 4, 0, 0, 4, 9, 17, 0, 0, 0, 0, 0]]

    names = ['Klacht',
      'Onderhoud',
      'Afspraak',
      'Storing',
      'Lekkage',
      'Ketel',
      'Lawaai',
      'Verbruik',
      'Offerte',
      'Contract',
      'Ventilatie',
      'Verwarming',
      'Warm water',
      'Thermostaat',
      'Warmtepomp']

    return JsonResponse({"matrix":  matrix, "names": names}, safe=False)
