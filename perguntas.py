class Perguntas:
  def __init__(self, pergunta, nao, sim):
    self.pergunta = pergunta
    self.nao = nao
    self.sim = sim

  @property
  def pergunta(self):
    return self._pergunta
  
  @pergunta.setter
  def pergunta(self, pergunta):
    self._pergunta = pergunta

  @property
  def nao(self):
    return self._nao
  
  @nao.setter
  def nao(self, nao):
    self._nao = nao

  @property
  def sim(self):
    return self._sim
  
  @sim.setter
  def sim(self, sim):
    self._sim = sim
