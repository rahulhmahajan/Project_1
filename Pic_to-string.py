import base64


# Convert an image file into Base64 string
def image_to_string(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# Example usage
if __name__ == "__main__":
    img_path = "tool.png"  # <-- put your image file here
    img_string = image_to_string(img_path)

    # Print first 200 characters so terminal is not flooded
    print("Image as string (first 200 chars):")
    print(img_string[:200] + "...\n")

    # Save the string into a text file
    with open("image_string.txt", "w") as f:
        f.write(img_string)

    print("Full Base64 string saved to image_string.txt")
