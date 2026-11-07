from pyfiglet import Figlet

def test_slant_renders():
    art = Figlet(font="slant").renderText("Hi")
    assert art.strip() != ""
    assert len(art.splitlines()) > 1
