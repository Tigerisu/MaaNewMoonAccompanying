import shutil
from pathlib import Path


def _clear_on_error_images():
    # 获取根目录
    root = Path(__file__).resolve().parent.parent

    # 文件夹路径
    on_error_folder = root / "debug" / "on_error"

    # 如果文件夹存在则删除
    if on_error_folder.exists():
        try:
            shutil.rmtree(on_error_folder)
        except Exception as e:
            pass


def pre_process():
    try:
        _clear_on_error_images()
    except Exception as e:
        print(f"预处理时出现问题: \n{e}\n这可能不影响使用，但建议在交流群内反馈！")
