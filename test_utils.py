import pytest
from utils import *

def test_sumvalues():
    assert sumvalues([1,2,3,4,5]) == 15
    assert sumvalues([1.1,2.1,3.1,4.1,5.1]) == 15.5
    assert sumvalues([1.1,'2.1',3.1,'4.1','5.1']) == 15.5
    with pytest.raises(Exception):
        assert sumvalues(['a', '1', 'b'])

def test_maxvalue():
    assert maxvalue([1,2,3,4,5]) == 5
    assert maxvalue([1.1,2.1,3.1,4.1,5.1]) == 5.1
    assert maxvalue([1.1,'2.1',3.1,'4.1','5.1']) == 5.1
    with pytest.raises(Exception):
        assert maxvalue(['a', '1', 'b'])

def test_minvalue():
    assert minvalue([1,2,3,4,5]) == 1
    assert minvalue([1.1,2.1,3.1,4.1,5.1]) == 1.1
    assert minvalue([1.1,'2.1',3.1,'4.1','5.1']) == 1.1
    with pytest.raises(Exception):
        assert minvalue(['a', '1', 'b'])

def test_meanvalue():
    assert meanvalue([1,2,3,4,5]) == 3
    assert meanvalue([1.1,2.1,3.1,4.1,5.1]) == 3.1
    assert meanvalue([1.1,'2.1',3.1,'4.1','5.1']) == 3.1
    with pytest.raises(Exception):
        assert meanvalue(['a', '1', 'b'])

def test_countvalue():
    assert countvalue([1,2,3,4,5], 1) == 1
    assert countvalue([1.1,2.1,3.1,4.1, 1.1], 1.1) == 2
    assert countvalue([1.1,'2.1',3.1,'1.1','1.1'], 1.1) == 3
    assert countvalue(['a', '1', 'b'], 'a') == 1