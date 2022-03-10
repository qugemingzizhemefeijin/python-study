"""
celery是一个基于分布式消息传输的异步任务队列，它专注于实时处理，同时也支持任务调度。它的执行单元为任务（task），利用多线程，
如Eventlet，gevent等，它们能被并发地执行在单个或多个职程服务器（worker servers）上。任务能异步执行（后台运行）或同步执行（等待任务完成）。
在生产系统中，celery能够一天处理上百万的任务。
"""

# 需要在dos窗口下运行下面命令
# celery -A _001celeryHelloWorld worker -l info -P eventlet

from celery import Celery
import time

app = Celery('tasks', broker='redis://127.0.0.1/0', backend='redis://127.0.0.1/1')
# 连接redis，创建apptask

@app.task
def hello(x, y):
    time.sleep(1)
    return x + y

"""
输出结果如下：

 -------------- celery@2007151234 v5.2.3 (dawn-chorus)
--- ***** -----
-- ******* ---- Windows-10- 2022-03-09 16:48:49
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x248d0ebed30
- ** ---------- .> transport:   redis://127.0.0.1:6379/0
- ** ---------- .> results:     redis://127.0.0.1/1
- *** --- * --- .> concurrency: 8 (eventlet)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . _001celeryHelloWorld.hello

[2022-03-09 16:48:49,460: INFO/MainProcess] Connected to redis://127.0.0.1:6379/0
[2022-03-09 16:48:49,484: INFO/MainProcess] mingle: searching for neighbors
[2022-03-09 16:48:50,498: INFO/MainProcess] mingle: all alone
[2022-03-09 16:48:50,503: INFO/MainProcess] pidbox: Connected to redis://127.0.0.1:6379/0.
[2022-03-09 16:48:50,506: INFO/MainProcess] celery@2007151234 ready.
"""
