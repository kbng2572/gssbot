import os
import sys
from pathlib import Path

def rebrand(root_dir, old_name, new_name, old_emoji, new_emoji):
    root = Path(root_dir).resolve()
    
    # Define replacements for name variations and emoji
    replacements = {
        old_name.lower(): new_name.lower(),
        old_name.capitalize(): new_name.capitalize(),
        old_name.upper(): new_name.upper(),
        old_emoji: new_emoji
    }

    # Files and directories to skip
    skip_dirs = {'.git', '__pycache__', 'node_modules', 'dist', 'build', '.idea', '.vscode'}
    skip_exts = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz', '.pyc', '.exe'}

    print(f"🚀 Rebranding from '{old_name}' ({old_emoji}) to '{new_name}' ({new_emoji})...")

    # Step 1: Process all files and directories
    # Use reverse sorting by path length (bottom-up) to ensure directory renaming doesn't break walking
    paths = sorted(root.rglob('*'), key=lambda p: len(p.parts), reverse=True)

    for path in paths:
        # Skip ignored directories
        if any(skip in path.parts for skip in skip_dirs):
            continue

        # Handle file content replacement
        if path.is_file():
            if path.suffix.lower() not in skip_exts:
                try:
                    content = path.read_text(encoding='utf-8')
                    new_content = content
                    for old, new in replacements.items():
                        new_content = new_content.replace(old, new)
                    
                    if new_content != content:
                        path.write_text(new_content, encoding='utf-8')
                        print(f"📝 Updated content: {path.relative_to(root)}")
                except (UnicodeDecodeError, PermissionError):
                    # Skip files that are not text or not readable
                    pass

        # Handle renaming (files and directories)
        new_name_str = path.name
        changed_name = False
        for old, new in replacements.items():
            if old in new_name_str:
                new_name_str = new_name_str.replace(old, new)
                changed_name = True
        
        if changed_name:
            new_path = path.with_name(new_name_str)
            try:
                path.rename(new_path)
                print(f"📁 Renamed: {path.relative_to(root)} -> {new_name_str}")
            except Exception as e:
                print(f"❌ Failed to rename {path}: {e}")

if __name__ == "__main__":
    # You can customize these if needed
    OLD_NAME = "nanobot"
    NEW_NAME = "gssbot"
    OLD_EMOJI = "🐈"
    NEW_EMOJI = "👁️"

    # Run from current directory
    try:
        rebrand(".", OLD_NAME, NEW_NAME, OLD_EMOJI, NEW_EMOJI)
        print("\n✨ Rebranding complete! Your project is now " + NEW_NAME + " " + NEW_EMOJI)
    except Exception as e:
        print(f"\n💥 An error occurred: {e}")
        sys.exit(1)
