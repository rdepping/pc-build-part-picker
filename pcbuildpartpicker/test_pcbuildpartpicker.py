import pcbuildpartpicker


def test_main_prints_hello_world(capsys):
    pcbuildpartpicker.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello World!\n"
