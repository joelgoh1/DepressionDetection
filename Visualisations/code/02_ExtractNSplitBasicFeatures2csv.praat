# Set the folder path containing audio and TextGrid files
folder$ = "C:\work\Corpus\EDAIC\wavNscript\"
report_file$ = (folder$ + "interval_voice_report.csv")

# Create the CSV header
header$ = "File,Interval Number,Interval Start (s),Interval End (s),Text," + "Mean Pitch (Hz),Pitch SD (Hz),Mean Intensity (dB),Intensity SD (dB)," + "Jitter (local) (%),Shimmer (local) (%),HNR (dB),Duration (s)"

appendFileLine: (folder$ + "interval_voice_report.csv"), header$ 

# Get a list of all WAV files in the folder
strfilelst = Create Strings as file list: "audioFiles", folder$ + "*.wav"
n = Get number of strings

# Loop through each audio file
for i from 1 to n
    # Get the audio file name
    select strfilelst
    file_name$ = Get string: i
    sound = Read from file: folder$ + file_name$

    # Load the corresponding TextGrid
    textgrid_name$ = replace$ (file_name$, "_AUDIO.wav", "_Transcript.TextGrid", 0)
    textgrid = Read from file: folder$ + textgrid_name$

    # Get the number of intervals in the first tier (modify if needed)
    tier = 1
    num_intervals = Get number of intervals: tier

    # Loop through each interval in the TextGrid
    for j from 1 to num_intervals
        select textgrid
        xmin = Get start point: tier, j
        xmax = Get end point: tier, j
        text$ = Get label of interval: tier, j

        # Extract the segment from the sound object
	select sound
        sound_interval = Extract part: xmin, xmax, "rectangular", 1, "no"

        # 1. Pitch (F0)
	select sound_interval
        pitch = To Pitch: 0.0, 75, 300
        mean_pitch = Get mean: 0, 0, "Hertz"
        sd_pitch = Get standard deviation: 0, 0, "Hertz"

        # 2. Intensity (Energy)
	select sound_interval
        intensity = To Intensity: 75, 0.0
        mean_intensity = Get mean: 0, 0
        sd_intensity = Get standard deviation: 0, 0

        # 3. Voice Quality Metrics (Jitter, Shimmer, HNR)
	select sound_interval
	plus pitch
	pointprocess = To PointProcess (cc)
        jitter_local = Get jitter (local): 0, 0, 0.0001, 0.02, 1.3
	select sound_interval
	plus pointprocess 
        shimmer_local = Get shimmer (local): 0, 0, 0.0001, 0.02, 1.3, 1.6
	select sound_interval
        hnr = To Harmonicity (cc): 0.01, 75.0, 0.1, 1.0
        mean_hnr = Get mean: 0, 0

        # 4. Duration
        duration = xmax - xmin

        # Format the results into a CSV row
        result$ = file_name$ + "," + string$(j) + "," + string$(xmin) + "," + string$(xmax) + "," + text$ + "," + string$(mean_pitch) + "," + string$(sd_pitch) + "," + string$(mean_intensity) + "," + string$(sd_intensity) + "," + string$(jitter_local) + "," + string$(shimmer_local) + "," + string$(mean_hnr) + "," + string$(duration)

        # Write the results to the report file
        appendFileLine: (folder$ + "interval_voice_report.csv"), result$ 

        # Clean up the interval sound object
	select sound_interval
	plus pitch
	plus pointprocess 
	plus hnr
	plus sound_interval 
	plus intensity 
        Remove
    endfor

    # Clean up the sound and TextGrid objects
    select sound
    plus textgrid
    Remove
endfor

# Notify the user
printline ("Interval-based voice report generated successfully: " + report_file$)
