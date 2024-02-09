import chiasmus
import helpers
import argparse
import json


def detect_chiasmus(lang, text, top, remove_duplicates):
    cd = chiasmus.ChiasmusDetector(lang, remove_duplicates)
    return cd(text, top)


def main():
    parser = argparse.ArgumentParser(description='stylotool')
    parser.add_argument('lang', type=str, help='language code (de)')
    parser.add_argument('text', type=str, help='text file to be analyzed')
    parser.add_argument('save', type=str, help='json file to save results')
    parser.add_argument('--chiasmus', action='store_true', help='use chiasmus detection')
    parser.add_argument('--top', type=int, default=-1, help="store only the top n results")
    parser.add_argument('--remove_duplicates', action='store_true', help='remove duplicates (currently only used for chiasmus)')
    args = parser.parse_args()

    with open(args.text, 'r') as f:
        text_content = f.read()

    results = {}

    if args.chiasmus:
        results['chiasmus'] = detect_chiasmus(args.lang, text_content, args.top, args.remove_duplicates)


    with open(args.save, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
