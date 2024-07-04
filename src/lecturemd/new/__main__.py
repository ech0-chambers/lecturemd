from .new import parse_args, main

if __name__ == "__main__":
    args = parse_args()
    main(args.target, not(args.non_interactive), args.overwrite)