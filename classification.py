from optflow import MotionEstimator, HomographyTransformationGetter

transformations_getter = HomographyTransformationGetter()

motion_estimator = MotionEstimator(
    max_points=900,
    min_distance=14,
    transformations_getter=transformations_getter,
    draw_flow=False,
)


def classify_video(shaky_unusable=None, shaky_usable=None, stationary_frame=None, non_stationary_frame=None,
                   avg_magnitude=None, displacement=None):

    # Classification logic
    if avg_magnitude > 25.0:
        if avg_magnitude > 39 and displacement >= 20000.0:
            print("-------: shaky un usable :-------")
            shaky_unusable += 1
        else:
            print("-------: shaky usable :-------")
            shaky_usable += 1
    else:
        if displacement > 1000.0:
            print("-------: non stationary :-------")
            non_stationary_frame += 1
        else:
            print("-------: stationary :-------")
            stationary_frame += 1

    return shaky_usable, shaky_unusable, stationary_frame, non_stationary_frame
