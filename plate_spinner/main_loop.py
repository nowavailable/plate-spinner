import sys
import asyncio
import time
from .db.data_store_factory import DataStoreFactory
import yaml
import importlib

cap: int = 50


def wait_main_loop():
    print("start: wait_main_loop")
    time.sleep(5)
    print("end: wait_main_loop")


def get_config(config_file_path):
    config = None
    if config_file_path:
        with open(config_file_path) as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config


"""
RDBに登録されたジョブを複数件ずつ取り出し、asyncioのloopに渡して処理する。
"""


def main_loop(config_path, specified_jobnames=[], sharding_keys=[], start_with_jobs=False, foreground=False):
    config = get_config(config_path)
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
    running = None
    try:
        running = data_store.store_running(
            config if start_with_jobs else None
        )
        db_session.commit()
    except Exception:
        db_session.rollback()

    prepare_to_exit = False # 無限ループの停止信号
    while True:
        loop = asyncio.get_event_loop()

        # 停止信号が出るまで無限にループ
        if not prepare_to_exit:
            """
            configはたまに読み直す
            """
            config = get_config(config_path)
            try:
                must_persist = data_store.check_mode_in_running(running=running)
                if must_persist:
                    db_session.commit()
            except Exception:
                db_session.rollback()

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
                    sharding_keys=sharding_keys,
                    limit=cap
                )
                # 同トランザクション内でupdate
                if len(dequeues) > 0:
                    data_store.store_taken_at(dequeues)
                    db_session.commit()
                    """
                    dequeueしたレコードからcommamdsを導出
                    """
                    for jobqueue in dequeues:
                        m = importlib.import_module("jobs." + jobqueue.job_name)
                        commands.append(m.perform())

            except Exception as e:
                db_session.rollback()
                # db_session.close()
                # raise
                # TODO: レポーティング
                print(e)
                loop.close()
                commands = []
                continue

            if len(commands) == 0:
                wait_main_loop()

            """
            commandsをJOBとしてスケジューリング
            """
            if len(commands) > 0 and not loop.is_running():
                loop.run_until_complete(asyncio.wait(commands))

            if data_store.check_killswitch():
                prepare_to_exit = True

        loop.close()
        """
        停止信号が出ていて且つ実行中のジョブが無くなったらメインループを終了
        """
        if prepare_to_exit:
            db_session.close()
            break

    # 終了処理
    try:
        data_store.remove_running()
        db_session.commit()
    except Exception:
        db_session.rollback()
