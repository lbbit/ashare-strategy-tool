from ashare_strategy.runtime import bundle_root, executable_dir


def test_runtime_paths_return_path_objects():
    assert bundle_root().exists()
    assert executable_dir() is not None
