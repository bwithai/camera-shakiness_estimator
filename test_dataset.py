import argparse
import csv

from classification import classify_video
from optflow import HomographyTransformationGetter, MotionEstimator
from video import Video


def run():
    parser = argparse.ArgumentParser(description="Receives a list of files and outputs a csv")
    parser.add_argument("files", type=str, nargs="+", help="Video files to process")

    args = parser.parse_args()

    # Create a CSV file to write the results
    with open("output.csv", "w", newline="") as csvfile:
        fieldnames = ["input_path", "class"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Process Videos
        for input_path in args.files:
            video = Video(input_path=input_path)
            transformations_getter = HomographyTransformationGetter()

            motion_estimator = MotionEstimator(
                max_points=900,
                min_distance=14,
                transformations_getter=transformations_getter,
                draw_flow=False,
            )

            frames = 0
            non_stationary_frame = 0
            stationary_frame = 0
            shaky_unusable = 0
            shaky_usable = 0

            for frame in video:
                frames += 1

                transformation, avg_magnitude, displacement = motion_estimator.update(frame)

                shaky_usable, shaky_unusable, \
                    stationary_frame, non_stationary_frame = classify_video(shaky_unusable, shaky_usable,
                                                                            stationary_frame, non_stationary_frame,
                                                                            avg_magnitude, displacement)

            video_categories = {
                "shaky_usable": shaky_usable / frames,
                "shaky_unusable": shaky_unusable / frames,
                "nonshaky_stationary": stationary_frame / frames,
                "nonshaky_nonstationary": non_stationary_frame / frames,
            }

            video_class = max(video_categories, key=video_categories.get)
            input_path = input_path

            # Write the row to the CSV file
            writer.writerow({"input_path": input_path, "class": video_class})

    print("Output saved to: output.csv")


if __name__ == "__main__":
    run()
