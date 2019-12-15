import asyncio
import time
from .db.data_store_factory import DataStoreFactory
from .db.jobqueue_sun import JobQueueSun
from .db.running import Running
import yaml


cap = 50

def check_overflow(current_job_count):
    if current_job_count >= cap:
        wait_main_loop()


def wait_main_loop():
    print("start: wait_main_loop")
    time.sleep(5)
    print("end: wait_main_loop")


def get_config(config_file_path):
    config = None

    if config_file_path:
        with open(config_file_path) as config_file:
            config = yaml.load(config_file)

    return config


def main_loop(config_path, specified_jobnames=[], sharding_keys=[], foreground=False):

    config = get_config(config_path)

    # TODO: 接続先DBに対してもconfigの利用
    data_store = DataStoreFactory.get_instance(config)
    db_session = data_store.session()
    data_store.store_runnning()

    # ループ
    loop = asyncio.get_event_loop()

    while True:
        # configの読み直し
        config = get_config(config_path)
        print(config)

        commands = []
        try:
            # デキューのためのSELECTクエリのwhere句には、
            # ・ジョブの種別をデキューの段階で絞るか
            # （=つまりある種のジョブのために独立したプロセスを動かすか）
            # ・シャーディングキーの指定があるか
            # のバリエーションがある。

            # 何件かづつバルクで取得

            # db_session.query

            # 同トランザクション内でupdate
            # data_store.store_taken_at()

            pass
        except:
            db_session.rollback()
            # db_session.close()
            # raise
            commands = []
            # TODO: レポーティング
            continue

        if len(commands) == 0:
            wait_main_loop()

        # commands をJOBとしてスケジューリング
        for command in commands:
            pass

        # # for debug
        # current_job_count = 51
        current_job_count = len(asyncio.all_tasks(loop))
        if check_overflow(current_job_count):
            wait_main_loop()

        if data_store.check_killswitch():
            # TODO: 現在のキューとジョブ群の終了を待った上で。
            db_session.close()
            break

        print("1")

    data_store.remove_runnning()
