#!/usr/bin/env python3
"""Simple command-line tool to translate SRT subtitle files."""
import argparse
from googletrans import Translator


def translate_srt(input_file: str, output_file: str, src: str = 'auto', dest: str = 'ko') -> None:
    """Translate an SRT file line by line."""
    translator = Translator()
    translated_lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            striped = line.strip()
            if striped.isdigit() or '-->' in line or not striped:
                # Keep sequence numbers and timestamps as-is
                translated_lines.append(line)
            else:
                result = translator.translate(line, src=src, dest=dest)
                translated_lines.append(result.text + '\n')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate SRT subtitles to another language")
    parser.add_argument('-i', '--input', required=True, help='Path to input SRT file')
    parser.add_argument('-o', '--output', required=True, help='Path for translated SRT file')
    parser.add_argument('--src', default='auto', help='Source language code (default: auto)')
    parser.add_argument('--dest', default='ko', help='Destination language code (default: ko)')
    args = parser.parse_args()

    translate_srt(args.input, args.output, src=args.src, dest=args.dest)


if __name__ == '__main__':
    main()
