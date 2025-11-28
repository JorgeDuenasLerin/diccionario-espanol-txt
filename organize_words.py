import json
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List


def process_chunk(chunk: List[str]) -> Dict[int, Dict[str, List[str]]]:
    """
    Process a chunk of words and organize them in a nested dictionary:
    {
        word_length: {
            first_letter: [list of words]
        }
    }
    """
    result: Dict[int, Dict[str, List[str]]] = {}

    for line in chunk:
        word = line.strip()
        if not word:
            continue

        first_char = word[0].lower()
        length = len(word)

        # Initialize nested dictionaries if needed
        result.setdefault(length, {}).setdefault(first_char, [])

        # Add word if it is unique in this bucket
        if word not in result[length][first_char]:
            result[length][first_char].append(word)

    return result


def merge_results(results: List[Dict[int, Dict[str, List[str]]]]) -> Dict[int, Dict[str, List[str]]]:
    """
    Merge multiple dictionaries produced by process_chunk into a single dictionary,
    ensuring uniqueness and sorting words alphabetically.
    """
    final_result: Dict[int, Dict[str, List[str]]] = {}

    for result in results:
        for length, letters in result.items():
            final_result.setdefault(length, {})

            for letter, words in letters.items():
                final_result[length].setdefault(letter, [])

                # Add only unique words
                for word in words:
                    if word not in final_result[length][letter]:
                        final_result[length][letter].append(word)

                # Sort alphabetically
                final_result[length][letter].sort()

    return final_result


def main():
    input_file = input("Enter input file path: ")
    output_file = input("Enter output file path: ")

    # Determine number of parallel processes
    num_processes = max(1, multiprocessing.cpu_count() - 1)
    print(f"Processing '{input_file}' using {num_processes} parallel processes...")

    # Read non-empty lines from file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]

    print(f"Loaded {len(lines):,} words")
    if lines:
        print("Sample words:", ', '.join(line.strip() for line in lines[:5]))

    # Split lines into chunks for parallel processing
    chunk_size = max(1, len(lines) // (num_processes * 4))
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    print(f"Processing {len(chunks)} chunks...")

    # Process chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(process_chunk, chunks))

    # Merge results
    print("Merging results...")
    organized_words = merge_results(results)

    # Convert structure to JSON-friendly format
    output_data: Dict[str, Dict[str, List[str]]] = {}
    for length in sorted(organized_words.keys()):
        output_data[str(length)] = {letter: sorted(words) 
                                    for letter, words in sorted(organized_words[length].items())}

    # Save JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Done! Results saved to '{output_file}'")

    # Print statistics
    total_words = sum(len(words) for letters in organized_words.values() for words in letters.values())
    print("\nWord count by length:")
    for length in sorted(organized_words.keys()):
        length_count = sum(len(words) for words in organized_words[length].values())
        print(f"  Length {length}: {length_count} words")

    print(f"\nTotal unique words: {total_words:,}")
    print(f"Different word lengths: {len(organized_words)}")

    # Show example structure
    print("\nExample structure (first few entries):")
    example = {
        length: {letter: organized_words[length][letter][:3]
                 for letter in sorted(organized_words[length].keys())[:2]}
        for length in sorted(organized_words.keys())[:2]
    }
    print(json.dumps(example, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
