from .build import main, parse_args

if __name__ == "__main__":
    args = parse_args()
    main(args.output, args.format)

