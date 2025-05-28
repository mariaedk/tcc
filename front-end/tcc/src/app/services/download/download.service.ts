import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DownloadService {
  private downloading = false;

  isDownloading(): boolean {
    return this.downloading;
  }

  startDownload(): boolean {
    if (this.downloading) return false;
    this.downloading = true;
    return true;
  }

  finishDownload(): void {
    this.downloading = false;
  }
}
