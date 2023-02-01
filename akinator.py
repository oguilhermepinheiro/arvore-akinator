from animal import Animal
from perguntas import Perguntas
from time import sleep
import os.path
import pickle

class Akinator:
  def __init__(self):
    self._raiz = Animal('Baleia')
    self._dados_arvore = [None]*(255)

  def menu_iniciar(self):
    print('Bem vindo ao jogo Akinator!')
    print('Pense em um animal e eu vou tentar adivinhar...')
    sleep(3)
    print('Você tem mais 3 segundos...')
    sleep(3)

  def verifica_resposta(self, resposta):
    if resposta[0].upper() == 'S':
      return True
    else:
      return False

  def verifica_se_animal(self, animal):
    pergunta_animal = input(f'Você pensou no(a) {animal.animal}? ')
    return self.verifica_resposta(pergunta_animal)

  def cria_nova_pergunta(self, animal_antigo: Animal):
    animal_pensado = input('Qual animal você pensou? ')
    pergunta_diferenca = input(f'Me diga uma pergunta que diferencie o(a) {animal_antigo.animal} do(a) {animal_pensado}: ')
    nova_pergunta = Perguntas(pergunta_diferenca, animal_antigo, Animal(animal_pensado))
    sleep(2)
    print('Ok, anotado! Vou tentar melhorar...')
    return nova_pergunta

  def encontra_animal(self, pergunta: Perguntas):
    pergunta_decisoria = input(pergunta.pergunta)
    if self.verifica_resposta(pergunta_decisoria) is False:
      if type(pergunta.nao) is Animal:
        return [False, pergunta, pergunta.nao]
      else:
        dados_encontra_animal = self.encontra_animal(pergunta.nao)
        return dados_encontra_animal
        # retornar os valores quando voltar pra cá da recursividade
    else:
      if type(pergunta.sim) is Animal:
        return [True, pergunta, pergunta.sim]
      else:
        dados_encontra_animal = self.encontra_animal(pergunta.sim)
        return dados_encontra_animal
        # retornar os valores quando voltar pra cá da recursividade

  def carregar_arvore(self):
    for  i in range(len(self._dados_arvore)):
      if type(self._dados_arvore[i]) is Perguntas:
        self._dados_arvore[i].nao = self._dados_arvore[(i*2)+1]
        self._dados_arvore[i].sim = self._dados_arvore[(i*2)+2]
    self._raiz = self._dados_arvore[0]

  def ler_arvore(self):
    for  i in range(len(self._dados_arvore)):
      if type(self._dados_arvore[i]) is Animal:
        print(self._dados_arvore[i].animal, i)
      elif self._dados_arvore[i] is None:
        pass
      else:
        print(self._dados_arvore[i].pergunta, i)

  def salvar_arvore(self, raiz_atual, indice_atual):
    self._dados_arvore[indice_atual] = raiz_atual
    if type(self._dados_arvore[indice_atual]) is Animal:
      pass
    else:
      if self._dados_arvore[indice_atual].nao is not None:
        raiz_atual = self._dados_arvore[indice_atual].nao
        indice_prox_esq = ((indice_atual+1)*2)-1
        self.salvar_arvore(raiz_atual, indice_prox_esq)
      if self._dados_arvore[indice_atual].sim is not None:
        raiz_atual = self._dados_arvore[indice_atual].sim
        indice_prox_dir = (((indice_atual+1)*2)-1)+1
        self.salvar_arvore(raiz_atual, indice_prox_dir)

  def escrever_arquivo(self):
    with open("dados_akinator.pkl", "wb") as arquivo:
      pickle.dump(self._dados_arvore, arquivo)
  
  def ler_arquivo(self):
    with open("dados_akinator.pkl", "rb") as arquivo:
      self._dados_arvore = pickle.load(arquivo)

  def iniciar_programa(self):
    jogo_em_andamento = True
    carregar_jogo_passado = input('Deseja carregar o jogo passado? ')
    if self.verifica_resposta(carregar_jogo_passado) is False:
      if os.path.isfile('dados_akinator.pkl'):
        os.remove('dados_akinator.pkl')
        print('Certo, estou excluindo o jogo passado...')
        sleep(2)
      print('Vamos começar!')
      sleep(1)
    else:
      if os.path.isfile('dados_akinator.pkl'):
        self.ler_arquivo()
        self.carregar_arvore()
      print('Certo, vamos começar a partir do jogo passado!')
      sleep(2)
    while jogo_em_andamento:
      self.menu_iniciar()
      # Começar o jogo sem nenhum dado preenchido, apenas um animal para chutar
      if type(self._raiz) is Animal:
        pergunta_chute = input(f'Você pensou no(a) {self._raiz.animal}?')
        if self.verifica_resposta(pergunta_chute):
          print('Parabéns, você venceu!')
          sleep(2)
        else:
          nova_pergunta = self.cria_nova_pergunta(self._raiz)
          sleep(3)
          self._raiz = nova_pergunta
      # Aqui o jogo já tem uma pergunta inicial, ou seja, a raíz já é uma pergunta
      else:
        respostas_encontra_animal = self.encontra_animal(self._raiz)
        verifica_lado = respostas_encontra_animal[0]
        verifica_pergunta = respostas_encontra_animal[1]
        animal_encontrado = respostas_encontra_animal[2]
        if self.verifica_se_animal(animal_encontrado):
          print('Parabéns, você venceu!')
          sleep(2)
        else:
          nova_pergunta = self.cria_nova_pergunta(animal_encontrado)
          if verifica_lado is True:
            verifica_pergunta.sim = nova_pergunta
          else:
            verifica_pergunta.nao = nova_pergunta
          sleep(3)
      pergunta_reiniciar = input('Deseja recomeçar? ')
      if self.verifica_resposta(pergunta_reiniciar) is False:
        pergunta_salvar =  input('Deseja salvar o jogo? ')
        if self.verifica_resposta(pergunta_salvar) is False:
          print('Jogo finalizando...')
          sleep(3)
          jogo_em_andamento = False
        else:
          self.salvar_arvore(self._raiz, 0)
          self.escrever_arquivo()
          print('Jogo finalizando...')
          sleep(3)
          jogo_em_andamento = False

teste = Akinator()
teste.iniciar_programa()