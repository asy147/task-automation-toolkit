import os.path
import argparse
from pathlib import Path
import shutil


print("\n" * 2)

def collision_file_mover(src, dest):
    """
    Moves a file to the destination directory, renaming it if a collision occurs.

    Parameters:
        src (Path): The source file path.
        dest (Path): The destination directory path.

    Returns:
        Path: The final destination path where the file was moved.

    Example:
        new_path = collision_file_mover(Path("source.txt"), Path("target_dir"))
        print(f"File moved to: {new_path}")
    """
    cnt = 1
    base, ext = src.stem, src.suffix
    final_dest = dest / f"{base}{ext}"
    while final_dest.exists():
        final_dest = dest / f"{base}_{cnt}{ext}"
        cnt += 1
    shutil.move(str(src), str(final_dest))
    return final_dest

def main():
    target_folder = Path("../ttest-files/")
    
    # extension → category folder
    CATEGORY_MAP = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Music": [".mp3", ".wav"],
        "Logs": [".log"],
    }

    counters = {} #init counters for categories for final output

    # 1. Create parser
    parser = argparse.ArgumentParser(description="Organize files by extension")

    # 2. Add arguments
    parser.add_argument(
        "path",                # positional argument
        nargs="?",             # make it optional
        default=".",           # default = current directory
        help="Target directory (default: current dir)"
    )
    parser.add_argument(
        "--show-cwd",
        action="store_true",
        help="Print the current working directory"
    )

    #parser.add_argument(#leaving this off for now
    #    "--by-date",           # optional flag
    #    action="store_true",   # becomes True if provided
    #    help="Organize files by last modified date"
    #)

    # 3. Parse arguments
    args = parser.parse_args()

    # 4. Use them
    print("Target path is", target_folder, "\n")#, args.path)

    #check if folder exists
    if not target_folder.exists():
        print("Error: folder does not exist")
    elif not target_folder.is_dir():
        print("Error: path is not a folder")

    if args.show_cwd:
        print(os.getcwd())
    
    #loop for organizing
    for file_path in target_folder.iterdir():
        if file_path.is_file():  # skip folders
            # Find the category for this file extension
            counters["Total Files"] = counters.get("Total Files", 0) + 1
            category = None
            for cat, exts in CATEGORY_MAP.items():
                if file_path.suffix in exts: #see if common extension
                    category = cat
                    break  # Stop searching once found
            if category:
                category_folder = target_folder / category
                if not category_folder.exists():
                    print(f"Folder '{category_folder}' does not exist, creating folder...")
                    category_folder.mkdir(parents=True, exist_ok=True)
                #move files to folders
                #shutil.copy(str(file_path), str(category_folder))
                collision_file_mover(file_path, category_folder)
                counters[category] = counters.get(category, 0) + 1
            else:
                #print(file_path, "not a known ext")
                unknown_folder = target_folder / "Unknown"
                if not unknown_folder.exists():
                    unknown_folder.mkdir(parents=True, exist_ok=True)
                collision_file_mover(file_path, unknown_folder)
                counters["Unknown"] = counters.get("Unknown", 0) + 1

    print("\n" + "-" * 30)
    print("Organized files summary:")
    for category, count in counters.items():
        print(f"- {category}: {count}")
        
if __name__ == "__main__":
    main()

