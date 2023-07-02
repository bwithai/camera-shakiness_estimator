import argparse
import json
import os
from functools import partial

from classification import classify_video
from optflow import MotionEstimator, HomographyTransformationGetter
import cv2

from video import Video, VideoFromFrames


def run():
    global video, output_path
    parser = argparse.ArgumentParser(description="Camera shakiness Estimator.")
    parser.add_argument("file", type=str, help="Video file to process")
    args = parser.parse_args()

    input_path = args.file

    if os.path.isfile(input_path) and input_path.endswith((".mp4", ".avi")):
        # Input path is a video file
        video = Video(input_path=input_path)
    elif os.path.isdir(input_path) and any(file.endswith((".jpg", ".png")) for file in os.listdir(input_path)):
        # Input path is a directory containing frames
        video = VideoFromFrames(input_path=input_path)
    else:
        # Invalid input path
        print("Invalid input path.")

    transformations_getter = HomographyTransformationGetter()

    motion_estimator = MotionEstimator(
        max_points=900,
        min_distance=14,
        transformations_getter=transformations_getter,
        draw_flow=True,
    )

    frames = 0
    non_stationary_frame = 0
    stationary_frame = 0
    shaky_unusable = 0
    shaky_usable = 0

    segments = []
    frame_number = 0
    start_frame = 0

    for frame in video:
        frame_number += 1
        frames += 1

        transformation, avg_magnitude, displacement = motion_estimator.update(frame)

        shaky_usable, shaky_unusable, \
            stationary_frame, non_stationary_frame = classify_video(shaky_unusable, shaky_usable,
                                                                    stationary_frame, non_stationary_frame,
                                                                    avg_magnitude, displacement)

        # print("----------------------------------: ", avg_magnitude, " :-------------------: ",displacement, " :---")

        # Check if it's time to create a new segment
        if frame_number % int(video.output_fps * 2) == 0 or frame_number == video.length:
            end_frame = frame_number
            segment = {
                "start_frame": start_frame,
                "end_frame": end_frame,
                "class": max(
                    [
                        ("shaky_usable", shaky_usable / frames),
                        ("shaky_unusable", shaky_unusable / frames),
                        ("nonshaky_stationary", stationary_frame / frames),
                        ("nonshaky_nonstationary", non_stationary_frame / frames),
                    ],
                    key=lambda x: x[1],
                )[0],
                "probabilities": {
                    "shaky_usable": round((shaky_usable / frames), 2),
                    "shaky_unusable": round((shaky_unusable / frames), 2),
                    "nonshaky_stationary": round((stationary_frame / frames), 2),
                    "nonshaky_nonstationary": round((non_stationary_frame / frames), 2),
                },
            }
            segments.append(segment)
            # Reset counters for the next segment
            frames = 0
            non_stationary_frame = 0
            stationary_frame = 0
            shaky_unusable = 0
            shaky_usable = 0
            start_frame = end_frame + 1

            # Create the JSON output
            output = {
                "input_path": input_path,
                "fps": int(video.output_fps),
                "segments": segments
            }

            # Save the JSON output to a file after adding each new segment
            output_path = "output.json"
            with open(output_path, "w") as f:
                json.dump(output, f, indent=2)

        frame = cv2.resize(frame, (800, 600))
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            continue

    print("Output saved to:", output_path)


if __name__ == "__main__":
    run()
