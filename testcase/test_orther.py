import uiautomator2 as u2
import time

from runlog.testLog import startLog

startLog()
d = u2.connect()
# r = d.shell('logcat -v time > d:log.log')
# time.sleep(5)
# r.close()
r = d.shell("logcat", stream=True)
# r: requests.models.Response
deadline = time.time() + 10 # run maxium 10s
try:
    for line in r.iter_lines(): # r.iter_lines(chunk_size=512, decode_unicode=None, delimiter=None)
        if time.time() > deadline:
            break
        print("Read:", line.decode('utf-8'))
finally:
    r.close()