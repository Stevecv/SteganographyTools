from PIL import Image


def menu():
    print("1. Encode text into an image")
    print("2. Decode text from an image")
    inp = input("  > ")

    if inp == "1":
        image_path = input("Enter the image path > ")
        image = Image.open(image_path)
        image.convert("RGB")
        loaded_image = image.load()

        text = input("Enter the text (or text file ending in \".txt\") > ")
        if text.endswith(".txt"):
            try:
                f = open(text, "r")
                text = f.read()
            except FileNotFoundError:
                print("File not found!")
                menu()

        pixel_count = image.size[0]*image.size[1]
        length = len(text)
        if length+4 > pixel_count / 8:
            print("Your text is too long for this image!")
            menu()
            return

        binary_length = format(length, '032b')
        binary_meta_1 = binary_length[:8]
        binary_meta_2 = binary_length[8:16]
        binary_meta_3 = binary_length[16:24]
        binary_meta_4 = binary_length[24:32]

        text = chr(int(binary_meta_1, 2)) + chr(int(binary_meta_2, 2)) + chr(int(binary_meta_3, 2)) +chr(int(binary_meta_4, 2)) + text

        start_index = 0
        counter = 0
        for char in text:
            binary = format(ord(char), '08b')
            for bit in binary:
                x = counter % image.size[0]
                y = int(counter / image.size[0])
                color = loaded_image[x, y]
                binary = format(color[1], '08b')[:7] + bit

                image.putpixel((x, y), (color[0], int(binary, 2), color[2]))

                counter += 1

            start_index += 8

        name = input("Enter a name to save the image as > ")
        image.save(name + ".png")

    if inp == "2":
        image_path = input("Enter the image path > ")
        image = Image.open(image_path)
        image.convert("RGB")
        loaded_image = image.load()

        binary = ""
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                color = loaded_image[x, y]
                binary += format(color[1], '08b')[-1]

        text = ""
        for i in range(int(len(binary) / 8)):
            byte = binary[i*8:(i*8)+8]
            text += chr(int(byte, 2))

        binary_length = format(ord(text[0]), '08b') + format(ord(text[1]), '08b') + format(ord(text[2]), '08b') + format(ord(text[3]), '08b')
        print(text[4:int(binary_length, 2)+4])


while True:
    menu()
