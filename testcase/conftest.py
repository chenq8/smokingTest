from page.call_page import Call
import pytest



@pytest.fixture()
def getmeun():
    data=Call().get_data('call.yaml')
    meun_data = [(x,y) for x,y in
        zip(data['secondary_meun'],data['third_meun'])]
    return meun_data

