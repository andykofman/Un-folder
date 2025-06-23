import os
import shutil
# wxPython is required for all dialogs. Install with: pip install wxPython
import wx

def select_multiple_folders():
    print("[DEBUG] Launching wx.DirDialog for multi-folder selection...")
    app = wx.App(False)
    dialog = wx.DirDialog(None, "Select folders to flatten (Ctrl+Click or Shift+Click for multi-select)",
                         style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.DD_MULTIPLE)
    folder_paths = []
    if dialog.ShowModal() == wx.ID_OK:
        print("[DEBUG] wx.DirDialog returned OK.")
        paths = dialog.GetPaths()
        print(f"[DEBUG] wx.DirDialog selected paths: {paths}")
        if isinstance(paths, (list, tuple)):
            folder_paths = list(paths)
        else:
            folder_paths = [paths]
    else:
        print("[DEBUG] wx.DirDialog was cancelled.")
    print(f"[DEBUG] Returning folder_paths: {folder_paths}")
    dialog.Destroy()
    # Do NOT call app.Destroy() here, let it go out of scope after all dialogs
    return folder_paths, app

def select_destination_folder(app):
    print("[DEBUG] Launching wx.DirDialog for destination folder selection...")
    dialog = wx.DirDialog(None, "Select destination folder", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    destination_folder = None
    if dialog.ShowModal() == wx.ID_OK:
        destination_folder = dialog.GetPath()
        print(f"[DEBUG] Destination folder selected: {destination_folder}")
    else:
        print("[DEBUG] Destination folder dialog was cancelled.")
    dialog.Destroy()
    return destination_folder

def flatten_folders(folder_paths, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for source_folder in folder_paths:
        for root, dirs, files in os.walk(source_folder):
            # Skip __pycache__ and hidden folders
            dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith('.')]
            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_folder, file)

                # Rename if there's a collision
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(destination_file):
                    new_name = f"{base}_{counter}{ext}"
                    destination_file = os.path.join(destination_folder, new_name)
                    counter += 1

                shutil.copy2(source_file, destination_file)
                print(f"Copied {source_file} -> {destination_file}")

def select_folders():
    print("[DEBUG] Starting select_folders()...")
    folder_paths, app = select_multiple_folders()
    print(f"[DEBUG] Folders selected: {folder_paths}")
    if not folder_paths:
        print("[DEBUG] No folders selected, showing info dialog.")
        wx.MessageBox("No folders selected.", "Info", wx.OK | wx.ICON_INFORMATION)
        app.Destroy()
        return

    destination_folder = select_destination_folder(app)
    if not destination_folder:
        print("[DEBUG] No destination folder selected, showing info dialog.")
        wx.MessageBox("No destination folder selected.", "Info", wx.OK | wx.ICON_INFORMATION)
        app.Destroy()
        return

    print("[DEBUG] Calling flatten_folders...")
    flatten_folders(folder_paths, destination_folder)
    print("[DEBUG] Flattening complete, showing done dialog.")
    wx.MessageBox("All folders have been flattened!", "Done", wx.OK | wx.ICON_INFORMATION)
    app.Destroy()

if __name__ == "__main__":
    select_folders()

