# context, fname, train, test, id, label
from dataclasses import dataclass
import pandas as pd


@dataclass
class DataModel:
    _dname : str = ''
    _sname : str = ''
    _fname : str = ''
    _train : str = ''
    _test : str = ''
    _id : str = ''
    _label : str = ''
   
    @property
    def dname(self) -> str : return self._dname
    @dname.setter
    def dname(self, dname: str) : self._dname = dname
    @property
    def sname(self) -> str: return self._sname
    @sname.setter
    def sname(self, sname: str): self._sname = sname
    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname: str): self._fname = fname

    @property
    def train(self) -> str: return self._train

    @train.setter
    def train(self, train: pd.DataFrame): self._train = train

    @property
    def test(self) -> str: return self._test

    @test.setter
    def test(self, test: pd.DataFrame): self._test = test

    @property
    def id(self) -> str: return self._id

    @id.setter
    def id(self, id: str): self._id = id

    @property
    def label(self) -> str: return self._label

    @label.setter
    def label(self,label: str): self._label = label