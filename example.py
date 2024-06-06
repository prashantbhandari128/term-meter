from termmeter.term_meter import TermMeter
import time

# Initialize TermMeter for tracking progress
processing_meter = TermMeter("Processing", total=50, width=50, benchmark=True)

# Start the progress meter
processing_meter.start()

# Simulate task execution
for i in range(1, 50):
    # Do some processing here...
    if i == 25:  # Pause processing_meter in the middle of progress.
        processing_meter.pause()
        time.sleep(0.45)  # Simulate some other activity.
        processing_meter.resume()
    time.sleep(0.1)
    # Update progress
    processing_meter.update(i + 1)