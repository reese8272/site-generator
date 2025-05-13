from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        # only process text type nodes
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        # Process this TEXT node for all delimiter pairs
        current_text = node.text
        while delimiter in current_text:
            start_index = current_text.find(delimiter)
            if start_index == -1:
                break

            end_index = current_text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                raise Exception(f"No closing delimiter found for {delimiter}")
            
            before_text = current_text[:start_index]
            delimited_text = current_text[start_index + len(delimiter): end_index]
            current_text = current_text[end_index + len(delimiter):]

            # add the "before text" if it exists
            if before_text:
                result.append(TextNode(before_text, TextType.TEXT))

            # add the delimited text with the new type
            result.append(TextNode(delimited_text, text_type))

        # add any remaining text
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    return result


if __name__ == "__main__":
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)