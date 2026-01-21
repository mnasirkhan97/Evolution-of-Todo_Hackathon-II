import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cli import TodoCLI

def main():
    cli = TodoCLI()
    cli.start()

if __name__ == "__main__":
    main()
