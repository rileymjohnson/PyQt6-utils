from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl

from pathlib import Path


def save_url_as_mhtml(url: str, save_file: str | Path) -> None:
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    loader = QWebEngineView()
    loader.setZoomFactor(1)
    loader.load(QUrl(url))
    page = loader.page()

    def _download_state_changed(download_state):
        if download_state == QWebEngineDownloadRequest \
            .DownloadState \
            .DownloadCompleted:
            app.quit()

    def _download_requested(web_download):
        web_download \
            .stateChanged \
            .connect(_download_state_changed)

    page \
        .profile() \
        .downloadRequested \
        .connect(_download_requested)

    def _load_finished(_):
        page.save(
            Path(save_file).resolve().as_posix(),
            QWebEngineDownloadRequest \
                .SavePageFormat \
                .MimeHtmlSaveFormat
        )

    loader \
        .loadFinished \
        .connect(_load_finished)

    app.exec()
