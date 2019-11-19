import pytest

from page.base import Base


@pytest.mark.parametrize('s_meun,t_meun',
                         Base().get_meun_data('call.yaml'))
def test_1(s_meun,t_meun):
    print(s_meun,t_meun)

path = r'D:\mytools\SmokingTestCase\testcase\test_orther.py'
pytest.main(['-s',path])