import uiautomator2 as u2
def test(**kwargs):
    d = u2.connect()
    print(d(**kwargs).info)

test(text='Settings')