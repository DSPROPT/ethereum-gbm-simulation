import numpy as np
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si
import pandas as pd

# Buscar dados históricos
dados = si.get_data('ETH-EUR')

# Calcular o retorno logarítmico
dados['log_return'] = np.log(dados['close'] / dados['close'].shift(1))

# Estimar os parâmetros para GBM
u = dados['log_return'].mean() # média
var = dados['log_return'].var() # variância
drift = u - (0.5 * var) # deriva
stdev = dados['log_return'].std()  # desvio padrão

np.array(drift)
np.array(stdev)

# Definir o número de simulações
num_simulacoes = 10
dias = 365

# Simular caminhos de preços
preco_final = []
for i in range(num_simulacoes):
    caminho_precos = []
    S0 = dados['close'][-1] # preço inicial
    caminho_precos.append(S0)
    for d in range(dias):
        dW = np.random.normal(loc=0, scale=drift+stdev)
        preco_futuro = S0 * np.exp(dW)
        caminho_precos.append(preco_futuro)
        S0 = preco_futuro
    preco_final.append(caminho_precos)
preco_final = pd.DataFrame(preco_final)

# Plotar resultados
plt.figure(figsize=(10,5))
plt.title('Simulação do Preço do Ethereum (GBM)')
plt.ylabel('Preço (€)')
plt.xlabel('Dias')
plt.plot(preco_final.transpose())
plt.show()
