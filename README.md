<h1>
Simulador de Consumidores BDI de lootboxes
</h1>
<h2>
Dependências:
</h2>
  -Python 3.8.3 ou melhor
  -plotly 5.3.1 ou melhor
  -pandas 1.0.5 ou melhor
  -numpy 1.18.5 ou melhor
  -scipy 1.5.0 ou melhor
<h2>
Execução(ALTERE PARÂMETROS PRIMEIRO):
</h2>
  na linha de comando, execute:
    python main.py
<h2>
Alteração de Parâmetros:
</h2>
  o arquivo defs.py contém os parâmetros utilizados pela simulação. Todos os não citados aqui não devem ser alterados:

  GEN -> Modo de geração das avaliações dos itens da lootbox. Pode ser: 
    -UNIFORM, para geração uniforme entre 0 e 2;
    -LOG, para geração logarítmica utilizando média 0 e desvio padrão 1;
    -EXPO, para geração exponencial com média 1;

  N -> número de itens dentro da lootbox

  SIM_N -> quantidade de consumidores simulado por iteração

  PRICE -> preço da lootbox

  PLAN_SIZE -> a ser utilizado para sobrescrever o tamanho do plano

  INSTINCT -> valor inicial de instinto

  CONFIDENCE -> valor inicial de confiança

  CONFIDENCE_RESET -> quando o plano for reconsiderado, o valor de confiança será reiniciado para o valor inicial dividido por este

  INSTMOD -> quanto o valor de instinto é reduzido cada vez que um plano é reconsiderado

  CONFMOD -> quanto o valor de confiança é incrementado/decrementado com base no item adquirido

  CONFIDENCE_THRESHOLD -> limite inferior de confiança

  INSTINCT_THRESHOLD -> limite inferior de instinto

  EVALUATION_FORMULA -> Fórmula de avaliação utilizada para determinar se uma coleção é desejável. Pode ser FRUGAL ou BASE

  MERCY -> Ativa o mecanismo de contenção de instinto quando setado em True

  VERBOSE -> Ativa escrita de texto de progresso no terminal

  PATH -> Local de escrita dos gráficos
