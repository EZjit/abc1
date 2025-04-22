import argparse
import re
from typing import List


class PhoneExtractor:
    def __init__(self) -> None:
        self.phone_pattern: re.Pattern = re.compile(r'(?:\+?7|8|)(?:[-\s().]*\d){9,10}', re.VERBOSE)
        self.unique_phones: dict = {}

    def _normalize_phone(self, phone_number: str) -> str | None:
        # Delete all non-numeric symbols
        digits = re.sub(r'\D', '', phone_number)

        # Check the length and correct
        if len(digits) == 10:
            digits = '7' + digits
        elif len(digits) == 11:
            if digits.startswith('8'):
                digits = '8' + digits[1:]
            elif not digits.startswith('7'):
                return None
        else:
            return None

        # Format phone number
        return f'+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}'

    def extract(self, file_path: str) -> List[str]:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            # Find all strings matches our phone pattern
            for phone_number in self.phone_pattern.finditer(text):
                candidate = phone_number.group().strip()
                if not candidate:
                    continue
                normalized_number = self._normalize_phone(candidate)
                if normalized_number and normalized_number not in self.unique_phones:
                    self.unique_phones[normalized_number] = None
        return list(self.unique_phones.keys())


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract and normalize phone numbers from text file')
    parser.add_argument('file_path', type=str, help='Path to a file')
    args = parser.parse_args()
    extractor = PhoneExtractor()
    phones = extractor.extract(args.file_path)
    for phone in phones:
        print(phone)


if __name__ == '__main__':
    main()
