import cv2
import depthai as dai
import numpy as np

def getFrame(queue):
    # Get frame from queue
    frame = queue.get()
    # Convert frame to OpenCV format and return
    return frame.getCvFrame()

def getMonoCamera(pipeline, isLeft):
    # Configurable mono camera
    mono = pipeline.createMonoCamera()

    # Set Camera Resolution
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

    if isLeft:
        # Get left camera
        mono.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    else:
        mono.setBoardSocket(dai.CameraBoardSocket.CAM_B)
    return mono

if __name__ == '__main__':
    # Define a pipeline
    pipeline = dai.Pipeline()

    # Set up left and right cameras
    monoLeft = getMonoCamera(pipeline, isLeft=True)
    monoRight = getMonoCamera(pipeline, isLeft=False)

    # Set output Xlink for left camera
    xoutLeft = pipeline.createXLinkOut()
    xoutLeft.setStreamName('left')

    # Set output xlink for right camera
    xoutRight = pipeline.createXLinkOut()
    xoutRight.setStreamName('right')

    # Attach cameras to output Xlink
    monoLeft.out.link(xoutLeft.input)
    monoRight.out.link(xoutRight.input)

    # Pipeline is defined, now we can connect to the device
    with dai.Device(pipeline) as device:

        # Get output queues
        leftQueue = device.getInputQueue('left', maxSize=1)
        rightQueue = device.getOutputQueue('right', maxSize=1)

        # Set display window name
        cv2.namedWindow("Stereo Pair")
        # Variable use to toggle between side by side view and one rame view
        sideBySide = True

        while True:
            # Get left frame
            leftFrame = getFrame(leftQueue)
            # Get right frame
            rightFrame = getFrame(rightQueue)

            if sideBySide:
                # Show side by side view
                imOut = np.hstack((leftFrame, rightFrame))
            else :
                # Show overlapping frames
                imOut = np.uint8(leftFrame/2 + rightFrame/2)

            # Display output image
            cv2.imshow("Stereo Pair", imOut)

            # Check for keyboard input
            key = cv2.waitKey(1)
            if key == ord('q'):
                # Quit when q is pressed
                break
            elif key == ord('t'):
                # Toggle display when t is pressed
                sideBySide = not sideBySide


