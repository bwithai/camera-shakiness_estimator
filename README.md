# Camera Shaking Estimator

## Table of Contents
- [Installation and Run](#installation)
- [Usage](#usage)
- [Using Frames](#using-frames)
- [Face Warning](#face-warning)


## Installation and Run

```bash
# Select Python 3.10 or > Interpreter
# set up your python environment variable 

pip install -r requirements.txt

python process_video.py .demo/test1.mp4 # Give the video file name

# Or

python process_video.py ./input_content_frames # Give the directory name contain the frames
```
    
## Using Frames
The directory which contain frame mush contain `seqinfo.ini` file

To create a seqinfo.ini file, you need to gather the necessary information about the video sequence, such as the frame rate, resolution, and sequence length. Here's an example of how you can create a seqinfo.ini file:
```
[Sequence]
name=video_sequence
imDir=.
imExt=.jpg
frameRate=30
seqLength=100
imWidth=1920
imHeight=1080
```
`name`: Provide a name for the video sequence.

`imDir`: Specify the directory where the frame images are located. The . represents the current directory.

`imExt`: Specify the extension of the frame images. Replace .jpg with the actual extension of your frame images (e.g., .png, .jpeg, etc.).

`frameRate`: Set the desired frame rate for the video.

`seqLength`: Specify the total number of frames in the video sequence.

`imWidth`: Set the width of the frames in pixels.

`imHeight`: Set the height of the frames in pixels.


## Face Warning

### 1. If face such type of warning
> [ WARN:0@0.479] global loadsave.cpp:248 findDecoder imread_('input_content_frames/000001.jpg'): can't open/read file: check file path/integrity

This is because of the name you give to your frames. replace your frames formate at video.py at line 361. the demo contain this formate`"{:04d}{}".format(self.frame_number, self.image_extension)`

### 2. If face
> homography_matrix, points_used = cv2.findHomography(
cv2.error: OpenCV(4.8.0) /io/opencv/modules/calib3d/src/fundam.cpp:385: error: (-28:Unknown error code -28) The input arrays should have at least 4 corresponding point sets to calculate Homography in function 'findHomography'

The video contains high shake, making it difficult to accurately calculate the transformation. Please stabilize the video or choose another video with less shake.