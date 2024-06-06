banner = r"""
 _____                                _
/__   \___ _ __ _ __ ___   /\/\   ___| |_ ___ _ __ 
  / /\/ _ \ '__| '_ ` _ \ /    \ / _ \ __/ _ \ '__|
 / / |  __/ |  | | | | | / /\/\ \  __/ ||  __/ |
 \/   \___|_|  |_| |_| |_\/    \/\___|\__\___|_|
+-------------------------------------------------+
|                    TermMeter                    |
|                   ===========                   |
|            Author : Prashant Bhandari           |
+-------------------------------------------------+
| TermMeter is a Python class designed as a       |
| text-based progress meter for tracking the      |
| progress of tasks in the terminal. It inherits  |
| from the TextArtisan class, which provides      |
| methods for formatting terminal text.           |
+-------------------------------------------------+ 
"""
import sys
import time
from module.textartisan.text_artisan import TextArtisan


class TermMeter(TextArtisan):
    def __init__(self, title, total, width=50, eta=True, benchmark=False):
        """
        ================================
        Initialize the TermMeter object.
        ================================

        Parameters:
        -----------
        -> title: str, title of the progress meter.
        -> total: int, total number of steps for the task.
        -> width: int, width of the progress bar (default is 50).
        -> eta: bool, whether to display estimated time remaining (default is True).
        -> benchmark: bool, whether to display benchmark information (default is False).
        """
        super().__init__()
        self.title = title
        self.total = total
        self.width = width
        self.progress = 0
        self.eta = eta
        self.benchmark = benchmark

    def start(self):
        """
        =====================================================
        Start the progress meter by recording the start time.
        =====================================================
        """
        self.start_time = time.time()

    def update(self, progress):
        """
        ====================================================
        Update the progress meter with the current progress.
        ====================================================

        Parameters:
        -----------
        -> progress: int, current progress value.
        """
        if progress < 0 or progress > self.total:
            raise ValueError("Progress value out of range.")
        self.progress = progress  # Update progress attribute
        percent = 100 * (progress / float(self.total))
        bar_length = int(self.width * (progress / self.total))
        bar = self.decorate([self.COLORS["green"]], "━" * bar_length) + self.decorate(
            [self.COLORS["white"]], "━" * (self.width - bar_length)
        )
        formatted_eta = self._get_formatted_eta(progress)
        formatted_benchmark = self._get_formatted_benchmark_info(progress)
        formatted_title = self.decorate(
            [self.COLORS["blue"], self.BOLD, self.ITALIC], self.title
        )
        sys.stdout.write(
            f"\r{formatted_title} [{bar}] {percent:.2f}%{formatted_eta}{formatted_benchmark}"
        )
        if self.total == progress:
            print()

    def pause(self):
        """
        =====================================================
        Pause the progress meter by recording the pause time.
        =====================================================
        """
        self.pause_time = time.time()

    def resume(self):
        """
        ==================================================================================
        Resume the progress meter by adjusting the start time based on the pause duration.
        ==================================================================================
        """
        if hasattr(self, "pause_time"):
            self.start_time += time.time() - self.pause_time

    def _get_formatted_benchmark_info(self, progress):
        """
        ==================================================================
        Get benchmark information to display alongside the progress meter.
        ==================================================================

        Parameters:
        -----------
        -> progress: int, current progress value.

        Returns:
        --------
        -> benchmark_info: str, formatted benchmark information.
        """
        if self.benchmark:
            benchmark = self.get_benchmark_info(progress)
            formatted_benchmark_info = f" | Task : {benchmark['progress']}, ET : {benchmark['elapsed_time']:.2f}s, RT : {benchmark['remaining_time']:.2f}s"
        else:
            formatted_benchmark_info = ""
        return formatted_benchmark_info

    def _get_formatted_eta(self, progress):
        """
        =============================================================
        Calculate estimated time remaining and format it for display.
        =============================================================

        Parameters:
        -----------
        -> progress: int, current progress value.

        Returns:
        --------
        -> formatted_eta: str, formatted estimated time remaining.
        """
        if self.eta:
            eta = self.calculate_eta(progress)
            formatted_eta = self.decorate(
                [self.BOLD, self.COLORS["red"]],
                f"{int(eta['hours']):02d}:{int(eta['minutes'] % 60):02d}:{int(eta['seconds'] % 60):02d}",
            )
            return f" | ETA : {formatted_eta}"
        else:
            return ""

    def get_progress(self):
        """
        ===============================
        Get the current progress value.
        ===============================

        Returns:
        --------
        -> progress: int, current progress value.
        """
        return self.progress

    def reset(self):
        """
        =================================================================
        Reset the progress meter by clearing the start time and progress.
        =================================================================
        """
        self.start_time = None
        self.progress = 0

    def is_complete(self):
        """
        ===================================================
        Check if the progress meter has reached completion.
        ===================================================

        Returns:
        --------
        -> bool, True if progress is equal to total, False otherwise.
        """
        return self.progress == self.total

    def elapsed_time(self):
        """
        ============================================================
        Calculate the elapsed time since the progress meter started.
        ============================================================

        Returns:
        --------
        -> elapsed: float, elapsed time in seconds.
        """
        if self.start_time:
            return time.time() - self.start_time
        else:
            return 0

    def remaining_time(self):
        """
        =================================================================
        Calculate the estimated time remaining based on current progress.
        =================================================================

        Returns:
        --------
        -> remaining: float, estimated time remaining in seconds.
        """
        if self.start_time and self.progress > 0:
            elapsed = time.time() - self.start_time
            return ((self.total - self.progress) * elapsed) / self.progress
        else:
            return 0

    def get_benchmark_info(self, progress):
        """
        ==========================
        Get benchmark information.
        ==========================

        Parameters:
        -----------
        -> progress : int, Current progress value.

        Returns:
        --------
        -> benchmark_info: dict,
            A dictionary containing the progress ratio, elapsed time, and remaining time.
            - progress: str
                The ratio of progress completed.
            - elapsed_time: float
                The total elapsed time since the progress meter started.
            - remaining_time: float
                The estimated time remaining based on the current progress.
        """
        benchmark_info = {
            "progress": f"{progress}/{self.total}",
            "elapsed_time": self.elapsed_time(),
            "remaining_time": self.remaining_time(),
        }
        return benchmark_info

    def calculate_eta(self, progress):
        """
        =======================================
        Calculate the estimated time remaining.
        =======================================

        Parameters:
        -----------
        -> progress : int, Current progress value.

        Returns:
        --------
        -> eta : dict,
            A dictionary containing the estimated time remaining in seconds, minutes, and hours.
            - seconds: float
                The estimated time remaining in seconds.
            - minutes: float
                The estimated time remaining in minutes.
            - hours: float
                The estimated time remaining in hours.
        """
        eta_seconds = (
            (self.total - progress) * (time.time() - self.start_time) / progress
            if progress > 0
            else 0
        )
        eta_minutes = int(eta_seconds // 60)
        eta = {
            "seconds": eta_seconds,
            "minutes": eta_minutes,
            "hours": int(eta_minutes // 60),
        }
        return eta


def termmeter_intro():
    items = list(range(0, 50))
    processing_meter = TermMeter("Loading", len(items), 16)
    processing_meter.start()
    for i in items:
        processing_meter.update(items.index(i) + 1)
        if i == 25:
            processing_meter.pause()
            time.sleep(0.4)
            processing_meter.resume()
        time.sleep(0.1)
    print(
        TextArtisan().decorate([TextArtisan.BOLD, TextArtisan.COLORS["green"]], banner)
    )


if __name__ == "__main__":
    termmeter_intro()
