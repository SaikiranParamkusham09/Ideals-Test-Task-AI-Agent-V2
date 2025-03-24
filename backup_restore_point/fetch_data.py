import json
from pathlib import Path

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    return data_dir

def read_json_file(file_path):
    """Try reading JSON file with different encodings"""
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return json.load(f)
        except UnicodeDecodeError:
            continue
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON with {encoding} encoding: {e}")
            continue
    
    raise ValueError(f"Could not read {file_path} with any of the attempted encodings")

def convert_json_encoding():
    """Convert existing JSON files to proper UTF-8 encoding"""
    data_dir = ensure_data_directory()
    
    try:
        # Convert postings.json
        print("Converting postings.json...")
        postings_file = data_dir / 'postings.json'
        postings_data = read_json_file(postings_file)
        
        with open(postings_file, 'w', encoding='utf-8') as f:
            json.dump(postings_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully converted {postings_file} to UTF-8")
        
        # Convert candidates.json
        print("Converting candidates.json...")
        candidates_file = data_dir / 'candidates.json'
        candidates_data = read_json_file(candidates_file)
        
        with open(candidates_file, 'w', encoding='utf-8') as f:
            json.dump(candidates_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully converted {candidates_file} to UTF-8")
        
        return True
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = convert_json_encoding()
    if success:
        print("JSON files converted successfully")
    else:
        print("Failed to convert JSON files. Please check the error messages above.") 