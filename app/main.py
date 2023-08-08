import cv2


def main():
    img = cv2.imread("/home/user/data/opencv-logo.png", 0)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
