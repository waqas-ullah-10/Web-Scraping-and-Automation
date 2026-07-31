"""
File Organizer
==============
Automatically sorts files in a target directory into subfolders based on
file type (Images, Documents, Videos, etc). Can run once or on a repeating
schedule.

"""

from pathlib import Path
import shutil

# Folder containing the files to organize
SOURCE_FOLDER = Path("D:\CS-Work (UET)\InternShip\ALGOhub\Python codes\Algohub_Week 5_Web Scraping & Automation\scraped_data")

# File categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi"],
}


def get_category(extension):
    """Return folder name based on file extension."""
    extension = extension.lower()

    for folder, extensions in FILE_TYPES.items():
        if extension in extensions:
            return folder

    return "Others"


def get_unique_destination(destination):
    """
    Prevent overwriting existing files.
    Example:
    report.pdf
    report_1.pdf
    report_2.pdf
    """
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            destination.parent
            / f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not new_name.exists():
            return new_name

        counter += 1


def organize_files():
    """Organize all files inside SOURCE_FOLDER."""

    if not SOURCE_FOLDER.exists():
        print("Source folder does not exist.")
        return

    moved = 0

    for item in SOURCE_FOLDER.iterdir():

        if item.is_dir():
            continue

        category = get_category(item.suffix)

        destination_folder = SOURCE_FOLDER / category
        destination_folder.mkdir(exist_ok=True)

        destination_file = destination_folder / item.name
        destination_file = get_unique_destination(destination_file)

        shutil.move(str(item), str(destination_file))

        print(f"Moved: {item.name}  →  {category}")

        moved += 1

    print("\nOrganization Complete!")
    print(f"Total files moved: {moved}")


if __name__ == "__main__":
    organize_files()