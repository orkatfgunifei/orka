#coding: utf-8

import sys


def main(args=None):
    """Rotina Principal"""
    if args is None:
        args = sys.argv[1:]

    # Porta Padrão
    port = 8070
    run = False

    for termo in args:

        if termo == '-p':
            port = args[args.index(termo)]
        elif termo == 'run':
            run = True
        elif termo == 'ola':
            print "Olá :)"

    if run:
        from app import app
        print "\n\nBem Vindo a plataforma Orka"
        print ("\nAbra o navegador em http://localhost:%s:" % (port))
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()