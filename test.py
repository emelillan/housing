from pathlib import Path
import os


def main():
    top = Path(__file__ + '../..').resolve()
    arrow = top / 'assets/arrow.png'
    print('source image:', arrow)
    print('destination image:', top / 'output' / os.path.basename(arrow))


if __name__ == '__main__':
    main()
    print('This is a test')
