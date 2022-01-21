from distutils.core import setup

import py2exe, glob

setup(
    # este é o arquivo que é executado quando você inicia o jogo a partir da linha de comando.
    console=["main.py"],
    # arquivos de dados - estes são os arquivos não-python, como imagens e sons
    data_files=[
        ("sprites", glob.glob("sprites\\*.json")),
        ("sfx", glob.glob("sfx\\*.ogg") + glob.glob("sfx\\*.wav")),
        ("levels", glob.glob("levels\\*.json")),
        ("img", glob.glob("img\\*.gif") + glob.glob("img\\*.png")),
        ("", ["settings.json"]),
    ],
)
