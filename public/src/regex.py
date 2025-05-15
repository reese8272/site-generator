import re

def extract_markdown_images(text):
    result = []

    if isinstance(text, str):
        match = re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', text)
        result.extend(match)
    elif isinstance(text, list):
        for entry in text:
            result.extend(re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', entry))
    else:
        raise Exception(f"Error, invalid type passed. You entered a {type(text)}. Must be a list or string")
    
    return result


def extract_markdown_links(text):
    result = []

    if isinstance(text, str):
        match = re.findall(r'\[(.*?)\]\((.*?)\)', text)
        result.extend(match)
    elif isinstance(text, list):
        for entry in text:
            result.extend(re.findall(r'\[(.*?)\]\((.*?)\)', entry))
    else:
        raise Exception(f"Error, invalid type passed. You entered a {type(text)}. Must be a list or string")

    return result

if __name__ == "__main__":
    example_string = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    print("Example of using the image function, both with a text and with a list")
    print(extract_markdown_images(example_string))
    print(" ")
    example_list = ["This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"]
    print(extract_markdown_images(example_list))

    print(' ')
    link_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev"
    link_list = ["This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev", "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev"]
    print("Example using the link function, both with string and list")
    print(extract_markdown_links(link_string))
    print(" ")
    print(extract_markdown_links(link_list))