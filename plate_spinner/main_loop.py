import asyncio
import time
from .db.data_store_factory import DataStoreFactory
import yaml

cap: int = 50


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
    # config = get_config(config_path)
    data_store = DataStoreFactory.get_instance()
    db_session = data_store.session

    """
    ジョブキューはふたつあり、そのいずれかのみを使うダブルビン方式。
    なのでそのいずれを使うかを最初に判定・決定する必要がある。
    """
    data_store.check_mode()

    """
    このプロセスの情報をRDBに記録しておく。そのレコードの emergency カラムを
    FalseからTrueに更新すると、プロセスが停止させられる。
    """
    try:
        data_store.store_runnning()
        db_session.commit()
    except Exception:
        db_session.rollback()

    loop = asyncio.get_event_loop() # asyncioのloop
    prepare_to_exit = False         # 無限ループの停止信号
    while True:
        # 停止信号が出るまで無限にループ
        if not prepare_to_exit:
            """
            configはたまに読み直す
            """
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
                dequeues = data_store.dequeue(
                    specified_jobnames=specified_jobnames,
                    sharding_keys=sharding_keys
                )
                # 同トランザクション内でupdate
                if len(dequeues) > 0:
                    data_store.store_taken_at(dequeues)
                    db_session.commit()

                    # commandsへと昇華。



            except Exception as e:
                db_session.rollback()
                # db_session.close()
                # raise
                # TODO: レポーティング
                # print(e)

                commands = []
                continue

            if len(commands) == 0:
                wait_main_loop()

            # commands をJOBとしてスケジューリング
            for command in commands:
                pass

            if data_store.check_killswitch():
                prepare_to_exit = True

        """
        現在実行中のジョブ数が、制限数以内であるかどうか。
        制限を超えていたらメインループをしばらくsleep
        """
        current_job_count = len(asyncio.all_tasks(loop))
        if check_overflow(current_job_count):
            wait_main_loop()

        """
        停止信号が出ていて且つ実行中のジョブが無くなったらメインループを終了
        """
        if prepare_to_exit and current_job_count == 0:
            db_session.close()
            break

    """
    終了処理
    """
    try:
        data_store.remove_runnning()
        db_session.commit()
    except Exception:
        db_session.rollback()
