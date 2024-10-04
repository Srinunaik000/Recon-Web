import argparse
from modules.scanner import Scanner

def parse_arguments():
    parser = argparse.ArgumentParser(description="XSS Fuzzing Tool")

    # Add argument for file input
    parser.add_argument(
        '--file', '-f',
        type=str,
        help="Path to the file containing URLs"
    )

    # Add argument for a single URL input
    parser.add_argument(
        '--url', '-u',
        type=str,
        help="Single URL to test for XSS"
    )

    # Add argument for custom payloads
    parser.add_argument(
        '--payloads', '-p',
        type=str,
        help="Path to a file containing custom XSS payloads"
    )

    # Add argument for checking headers
    parser.add_argument(
        '--check-headers', 
        action='store_true',
        help="Check headers for reflected XSS"
    )

    # Add option to show only positive results
    parser.add_argument(
        '--show-positive',
        action='store_true',
        help="Only show results where payloads are reflected"
    )

    # Parse the arguments
    return parser.parse_args()

def main():
    args = parse_arguments()
    scanner = Scanner(args)
    scanner.run()

if __name__ == "__main__":
    main()
