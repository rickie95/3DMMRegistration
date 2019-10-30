from PyQt5.Qt import QFileDialog


def load_file_dialog(parent, filters, multiple_files=False):
    dlg = QFileDialog()
    options = dlg.Options()
    options |= QFileDialog.DontUseNativeDialog
    if multiple_files:
        file_name, _ = dlg.getOpenFileNames(parent, "Load a model", "", filters, "File WRML (*.wrl)", options=options)
    else:
        file_name, _ = dlg.getOpenFileName(parent, "Load a model", "", filters, "File WRML (*.wrl)", options=options)
    if file_name == "":
        return None
    return file_name


def save_file_dialog(parent, filters):
    dlg = QFileDialog()
    options = dlg.Options()
    options |= dlg.DontUseNativeDialog
    filename, _ = dlg.getSaveFileName(parent, None, "Save model", filter=filters, options=options)
    if filename == "":
        return None
    return filename
