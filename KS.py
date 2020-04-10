# -*- coding: utf-8 -*-
Versão 1 - **09/04/2020**
"""

def KSOut(arquivo,Perf,Escore,Buckets=10):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    '''
    arquivo   = nome do arquivo, formato dataFrame
    Perf      = nome da variável que indica a performance observada, bom deve ser 1
    Escore    = nome da variável que indica o escore
    Buckets   = número de buckets para calculo do KS (padrão 10)
    '''
    # Algumas vezes é necessário mudar a parametrização aqui
    data = arquivo.rename(columns={ Perf: 'Perf', Escore: 'Escore'})
    Perf=data.Perf
    Escore=data.Escore
    data['Bom'] =data['Perf']
    data['Mau'] =1-data['Perf']
    data['Bucket'] = pd.qcut(data.Escore, Buckets)
    # Agrupa os dados pelos grupos
    grouped = data.groupby('Bucket', as_index = False)
    tabela = pd.DataFrame(grouped.min().Escore, columns = ['Min_scr'])
    tabela['Max_scr'] = grouped.max().Escore
    tabela['Min_scr'] = grouped.min().Escore
    tabela['Mau'] = grouped.sum().Mau
    tabela['Bom'] = grouped.sum().Bom
    tabela['Total'] = tabela.Mau + tabela.Bom
    # Ordena os dados da tabela pelo escore
    tabela1 = (tabela.sort_values(by = 'Min_scr')).reset_index(drop = True)
    # Construção dos campos
    tabela1['odds'] = (tabela1.Bom / tabela1.Mau).apply('{0:.2f}'.format)
    tabela1['bad_rate'] = (tabela1.Mau / tabela1.Total).apply('{0:.2%}'.format)
    tabela1['distrib'] = (tabela1.Total / data.Perf.count()).apply('{0:.1%}'.format)
    # # Calcula a estatística KS
    tabela1['ks'] = np.round(((tabela1.Mau / data.Mau.sum()).cumsum() - (tabela1.Bom / data.Bom.sum()).cumsum()), 4) * 100
    # Define a função para marcar o máximo KS da tabela
    flag = lambda x: '<----' if x == tabela1.ks.max() else ''
    tabela1['max_ks'] = tabela1.ks.apply(flag)
    tabela1.to_excel("Tabela_KS.xlsx")
    print(tabela1)
    # Elaboração do Gráfico
    Mau_ks = np.round(((tabela1.Mau / data.Mau.sum()).cumsum()), 4) * 100
    Bom_ks = np.round(((tabela1.Bom / data.Bom.sum()).cumsum()), 4) * 100
    ks_val = max(np.round(((tabela1.Mau / data.Mau.sum()).cumsum() - (tabela1.Bom / data.Bom.sum()).cumsum()), 4) * 100)
    ks = pd.DataFrame({'Mau_Acum':Mau_ks,'Bom_Acum': Bom_ks})
    ax = ks.plot.line(color=['r', 'g'])
    with PdfPages(r'Grafico_KS.pdf') as export_pdf:
        plt.title("Gráfico do KS (Valor Percentual=%0.2f)"% ks_val, color='black', fontsize=16)
        ax.set_ylabel("Percentual", color="black", fontsize=14)
        ax.set_xlabel("Buckets", color="black", fontsize=14)
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        ax.grid(linestyle='-', linewidth='0.3', color='grey' )
        export_pdf.savefig()

def KSVal(arquivo,Perf,Escore,Buckets=10):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    '''
    arquivo   = nome do arquivo, formato dataFrame
    Perf      = nome da variável que indica a performance observada, bom deve ser 1
    Escore    = nome da variável que indica o escore
    Buckets   = número de buckets para calculo do KS (padrão 10)
    '''
    # Algumas vezes é necessário mudar a parametrização aqui
    data = arquivo.rename(columns={ Perf: 'Perf', Escore: 'Escore'})
    Perf=data.Perf
    Escore=data.Escore
    data['Bom'] =data['Perf']
    data['Mau'] =1-data['Perf']
    data['Bucket'] = pd.qcut(data.Escore, Buckets)
    # Agrupa os dados pelos grupos
    grouped = data.groupby('Bucket', as_index = False)
    tabela = pd.DataFrame(grouped.min().Escore, columns = ['Min_scr'])
    tabela['Mau'] = grouped.sum().Mau
    tabela['Bom'] = grouped.sum().Bom
    # Calcula a estatística KS
    tabela['ks'] = np.round(((tabela.Mau / data.Mau.sum()).cumsum() - (tabela.Bom / data.Bom.sum()).cumsum()), 4) * 100
    ks = max(tabela.ks)
    return ks