class Animal:
  def __init__(self, animal):
    self.animal = animal

  @property
  def animal(self):
    return self._animal
  
  @animal.setter
  def animal(self, animal):
    self._animal = animal
