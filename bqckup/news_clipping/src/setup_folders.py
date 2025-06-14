import os
import json
from pathlib import Path

def create_folder_structure():
    """Create the required folder structure for the GI Agent News Clipping project."""
    # Define base directory and required folders
    base_dir = Path(__file__).parent.parent
    folders = [
        'src',
        'data',
        'config',
        'output'
    ]
    
    print("📂 Creating folder structure...")
    
    # Create each folder if it doesn't exist
    for folder in folders:
        folder_path = base_dir / folder
        folder_path.mkdir(exist_ok=True)
        print(f"✓ Created {folder} directory")

    # Create initial README files in each folder
    for folder in folders:
        readme_path = base_dir / folder / "README.md"
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {folder.title()} Directory\n\n")
                if folder == 'src':
                    f.write("Contains Python source code files for the news clipping agent.\n")
                elif folder == 'data':
                    f.write("Stores collected news data.\n")
                elif folder == 'config':
                    f.write("Contains configuration files including API settings.\n")
                elif folder == 'output':
                    f.write("Stores generated output files (HTML, CSV, etc).\n")
            print(f"✓ Created README in {folder} directory")

    print("\n✨ Folder structure created successfully!")
    return base_dir

if __name__ == "__main__":
    create_folder_structure() 