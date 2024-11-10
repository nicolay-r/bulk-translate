import importlib
import sys


def dynamic_init(src_dir, class_filepath, class_name=None):
    sys.path.append(src_dir)
    class_path_list = class_filepath.split('/')
    class_path_list[-1] = '.'.join(class_path_list[-1].split('.')[:-1])
    class_name = class_path_list[-1].title() if class_name is None else class_name
    class_path = ".".join(class_path_list + [class_name])
    print(f"Dynamic loading for the file and class `{class_path}`")
    cls = auto_import(class_path, is_class=False)
    return cls


def auto_import(name, is_class=False):
    """ Import from the external python packages.
    """
    def __get_module(comps_list):
        return importlib.import_module(".".join(comps_list))

    components = name.split('.')
    m = getattr(__get_module(components[:-1]), components[-1])

    return m() if is_class else m
