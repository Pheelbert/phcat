def prompt(shell=None):
    while True:
        command = input('[pheelpwn]> ').strip()
        print(f'Unrecognized command: "{command}"')

def main():
    prompt()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\b\r')
