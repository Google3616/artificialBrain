import cv2
import numpy as np

class VideoProcessor:
    def __init__(self, width=40, height=30, image_path=None):
        """Initialize video processing with an optional static image."""
        self.WIDTH = width
        self.HEIGHT = height
        self.CENTER_X, self.CENTER_Y = width // 2, height // 2

        # Precompute distance-based threshold scaling
        distances = np.sqrt((np.arange(width) - self.CENTER_X)[:, None]**2 + (np.arange(height) - self.CENTER_Y)**2)
        max_distance = np.max(distances)
        self.threshold_map = (distances / max_distance) * 0.8  # Increase threshold up to 0.8 at the edges
        self.threshold_map = self.threshold_map.T  # Fix shape to match (height, width)

        self.image_mode = False

        if image_path:
            self.image = cv2.imread(image_path)
            if self.image is None:
                raise ValueError("Failed to load image. Check the file path.")
            self.image_mode = True  # Enable image processing mode
            print(f"Using static image: {image_path}")
        else:
            # Initialize video capture if no image is provided
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def apply_threshold(self, img):
        """Applies a dynamic threshold based on distance from the center."""
        img = img.astype(np.float32) / 255.0
        img = np.where(img > self.threshold_map, img, 0)
        return (img * 255).astype(np.uint8)

    def apply_threshold_edges(self, img, threshold=0.7):
        """Applies a fixed threshold for edge detection."""
        img = img.astype(np.float32) / 255.0
        img[img < threshold] = 0
        return (img * 255).astype(np.uint8)

    def update(self):
        """Captures a frame (or uses the static image), processes it, and returns five thresholded arrays."""
        if self.image_mode:
            frame = self.image.copy()
        else:
            ret, frame = self.cap.read()
            if not ret:
                return None

        # Resize frame to match processing dimensions
        small_frame = cv2.resize(frame, (self.WIDTH, self.HEIGHT), interpolation=cv2.INTER_NEAREST)

        # Convert to grayscale for edge detection
        gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

        # Edge detection (Sobel)
        edges_x = cv2.Sobel(gray_frame, cv2.CV_64F, 1, 0, ksize=3)
        edges_y = cv2.Sobel(gray_frame, cv2.CV_64F, 0, 1, ksize=3)
        edges_x = cv2.convertScaleAbs(edges_x)
        edges_y = cv2.convertScaleAbs(edges_y)

        # Split into R, G, and B channels
        blue_channel, green_channel, red_channel = cv2.split(small_frame)

        # Apply thresholding
        red_thresh = self.apply_threshold(red_channel)
        green_thresh = self.apply_threshold(green_channel)
        blue_thresh = self.apply_threshold(blue_channel)
        edges_x_thresh = self.apply_threshold_edges(edges_x)
        edges_y_thresh = self.apply_threshold_edges(edges_y)

        return red_thresh, green_thresh, blue_thresh, edges_x_thresh, edges_y_thresh

    def release(self):
        """Releases video capture resources."""
        if not self.image_mode:
            self.cap.release()
        cv2.destroyAllWindows()
