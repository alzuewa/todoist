from pathlib import Path

import tests


def get_resource_path(local_file_path):
    return Path(tests.__file__).parent.parent.joinpath(local_file_path).absolute()
