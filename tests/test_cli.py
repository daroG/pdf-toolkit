def test_cli_module_imports_with_default_path():
    from pdf_toolkit.cli import cli

    assert cli.app.file_path == ''
