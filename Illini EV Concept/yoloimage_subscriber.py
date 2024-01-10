import rclpy  # Python library for ROS 2
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from ultralytics import YOLO  # Yolov8 library

class YoloImageSubscriber(Node):
    """
    Create an YoloYoloImageSubscriber class, which is a subclass of the Node class.
    """

    def __init__(self):
        """
        Class constructor to set up the node
        """
        # Initiate the Node class's constructor and give it a name
        super().__init__('yolo_image_subscriber')

        # video_frame topic
        topic_name = 'yolovideo_frame'

        # Load Yolov8 model
        self.model = YOLO('yolov8n.pt')

        # Create the publisher. This publisher will publish an Image
        # to the yolovideo_frame topic. The queue size is 10 messages.
        self.publisher_ = self.create_publisher(Image, topic_name, 10)

        # Create the subscriber. This subscriber will receive an Image
        # from the video_frame topic. The queue size is 10 messages.
        self.subscription = self.create_subscription(
            Image,
            'video_frame',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()

    def listener_callback(self, data):
        """
        Callback function.
        """
        # Display the message on the console
        self.get_logger().info('Receiving video frame')

        # Convert ROS Image message to OpenCV image
        current_frame = self.br.imgmsg_to_cv2(data)

        # Segmentation of Current Frame Using Yolov8 Predictions
        results = self.model.predict(source=current_frame, imgsz=480, conf=0.5)

        # Publish the image.
        # The 'cv2_to_imgmsg' method converts an OpenCV
        # image to a ROS 2 image message
        self.publisher_.publish(self.br.cv2_to_imgmsg(results[0].plot(), "bgr8"))

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the node
    yolo_image_subscriber = YoloImageSubscriber()

    # Spin the node so the callback function is called.
    rclpy.spin(yolo_image_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    yolo_image_subscriber.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()


if __name__ == '__main__':
    main()
