import sys
import argparse
import p2p

def parse_arguments():
    reg_ds = 'The registrar application'
    usage_str = f'{sys.argv[0]} [-h] port'
    parser = argparse.ArgumentParser(description=reg_ds,
                                    usage=usage_str)
    parser.add_argument(
        'port',
        type=int,
        help='the port at which the server should listen')

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' port', file=sys.stderr)
        sys.exit(1)

    try:
        p2p.app.run(
            host='0.0.0.0', port=args.port, debug=True
        )
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
