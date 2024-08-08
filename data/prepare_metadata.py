import json
import csv

# Function to read an external JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to convert phones to arpabet and IPA (dummy implementation)
def convert_to_arpabet_and_ipa(phone):
    # Remove the _B, _I, _E suffixes for the conversion
    base_phone = phone[:-2] if phone[-2] == '_' else phone
    # arpabet to ipa conversion
    arpa_key = ['aa', 'ae', 'ah', 'ao', 'aw', 'ax', 'axr', 'ay', 'eh', 'er', 'ey', 'ih', 'ix', 'iy', \
                    'ow', 'oy', 'uh', 'uw', 'ux' , 'b', 'ch', 'd', 'dh', 'dx', 'el', 'em', 'en', 'f', \
                    'g', 'h', 'hh', 'jh', 'k', 'l', 'm', 'n', 'ng', 'nx', 'p', 'q', 'r', 's', 'sh', \
                    't', 'th', 'v', 'w', 'wh', 'y', 'z', 'zh', 'ax-h', 'bcl', 'dcl', 'eng', 'gcl', 'hv', \
                    'kcl', 'pcl', 'tcl', 'pau', 'epi', 'h#']
    ipa_key = ['ɑ', 'æ', 'ʌ', 'ɔ', 'aʊ', 'ə', 'ɚ', 'aɪ', 'ɛ', 'ɝ', 'eɪ', 'ɪ', 'ɨ', 'i', 'oʊ', 'ɔɪ', \
                    'ʊ', 'u', 'ʉ', 'b', 'tʃ', 'd', 'ð', 'ɾ', 'l̩', 'm̩', 'n̩', 'f', 'ɡ', 'h', 'h', 'dʒ', 'k', \
                    'l', 'm', 'n', 'ŋ', 'ɾ̃', 'p', 'ʔ', 'ɹ', 's', 'ʃ', 't', 'θ', 'v', 'w', 'ʍ', 'j', 'z', \
                    'ʒ', 'ə̥', 'b̚', 'd̚', 'ŋ̍', 'ɡ̚', 'ɦ', 'k̚', 'p̚', 't̚', 'N/A', 'N/A', 'N/A']
    arpabet = base_phone
    ipa_conversion = dict(zip(arpa_key, ipa_key))
    ipa = ipa_conversion[arpabet]
    return arpabet, ipa

# Function to generate CSV from JSON data
def generate_phoneme_csv(json_file_path, csv_file_path, sample_id, speaker_id, sex, filepath):
    # Load JSON data
    data = read_json_file(json_file_path)

    # Define the columns for the CSV
    columns = [
        "start_word", "end_word", "word", "sample_id", "speaker_id",
        "start_phoneme", "end_phoneme", "sex", "arpabet", "ipa", "filepath", "index_phoneme"
    ]

    # Prepare CSV rows
    rows = []
    for word_info in data["words"]:
        start_word = int(word_info["start"] * 10000)  # assuming sample rate is 10kHz for demonstration
        end_word = int(word_info["end"] * 10000)      # convert seconds to sample indices
        word = word_info["word"]
        phones = word_info["phones"]

        for index, phone_info in enumerate(phones):
            start_phoneme = start_word if index == 0 else end_phoneme + 1
            end_phoneme = start_phoneme + int(phone_info["duration"] * 10000) - 1
            arpabet, ipa = convert_to_arpabet_and_ipa(phone_info["phone"])

            row = [
                start_word, end_word, word, sample_id, speaker_id,
                start_phoneme, end_phoneme, sex, arpabet, ipa, filepath, index
            ]
            rows.append(row)

    # Write CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"CSV file '{csv_file_path}' created successfully.")

# Example usage
json_file_path = '2_Enda_0.json'  # Path to your JSON file
csv_file_path = 'metadata.csv'  # Desired output CSV file path
sample_id = "sample_01"
speaker_id = "speaker_01"
sex = "m"
filepath = "../data/2_Enda_0.wav"

generate_phoneme_csv(json_file_path, csv_file_path, sample_id, speaker_id, sex, filepath)
