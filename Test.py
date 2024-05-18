import depthai as dai
import cv2

pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()

manip = pipeline.createImageManip()
# manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
manip.initialConfig.setResize(600, 451)
cam.isp.link(manip.inputImage)

xout = pipeline.createXLinkOut()
xout.setStreamName("out")
manip.out.link(xout.input)

with dai.Device(pipeline) as device:
    f = device.getOutputQueue('out').get().getCvFrame()
    cv2.imshow("frame", f)
    cv2.waitKey(0)