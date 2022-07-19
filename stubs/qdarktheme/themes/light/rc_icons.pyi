from qdarktheme.qtpy import QtCore as QtCore

qt_resource_data: bytes
qt_resource_name: bytes
qt_resource_struct: bytes

def qInitResources() -> None: ...
def qCleanupResources() -> None: ...
