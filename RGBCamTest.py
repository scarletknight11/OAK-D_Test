import depthai
import depthai as dai
import cv2

#pipeline
pipeline = dai.Pipeline()

#color
camRGB = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")

#left stereo cam
monoLeft = pipeline.create(dai.node.MonoCamera)
monoLeft.setBoardSocket(dai.CameraBoardSocket.CAM_A)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName("left")

#right stereo cam
monoRight = pipeline.create(dai.node.MonoCamera)
monoRight.setBoardSocket(dai.CameraBoardSocket.CAM_B)
xoutRight = pipeline.create(dai.node.XLinkOut)
xoutRight.setStreamName("right")

# Linking
camRGB.preview.link(xoutRgb.input)
monoRight.out.link(xoutRight.input)
monoLeft.out.link(xoutLeft.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=2, blocking=False)
    qLeft = device.getOutputQueue(name="left", maxSize=2, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=2, blocking=False)

    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
        inLeft = qLeft.get() # blocking call, will wait until a new data has arrived
        inRight = qRight.get() # blocking call, will wait until a new data has arrived

        # Retrieve 'bgr' (opencv format) frame
        cv2.imshow("rgb", cv2.cvtColor(inRgb.getCvFrame(), cv2.COLOR_RGB2BGR))
        cv2.imshow("left", inLeft.getCvFrame())
        cv2.imshow("right", inRight.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break