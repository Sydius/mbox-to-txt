import mailbox
import re


def munge_message(text):
    text = re.sub(r'(\n|^)On.*\n?.*wrote:\n+(.|\n)*$', '', text)
    text = re.sub(r'(\n|^)From:(.|\n)*$', '', text)
    text = re.sub(r'(\n|^)---------- Forwarded message ----------(.|\n)*$', '', text)
    text = re.sub(r'(\n|^)-----BEGIN PGP MESSAGE-----\n(.|\n)*-----END PGP MESSAGE-----\n', '', text)
    text = re.sub(r'<[^ ]+>', '', text)
    return text


def unquoted_line(line):
    quote_depth = 0
    while line.startswith('>'):
        line = line[1:]
        quote_depth += 1
    return (line, quote_depth)


def unstuff_line(line):
    if line.startswith(' '):
        return line[1:]
    return line


def unflow_line(line, delsp):
    if len(line) < 1:
        return (line, False)
    if line.endswith(' '):
        if delsp:
            line = line[:-1]
        return (line, True)
    return (line, False)


def unflow_text(text, delsp):
    full_line = ''
    full_text = ''
    lines = text.splitlines()
    for line in lines:
        (line, quote_depth) = unquoted_line(line)
        line = unstuff_line(line)
        (line, soft_break) = unflow_line(line, delsp)
        full_line += line
        if not soft_break:
            full_text += '>' * quote_depth + full_line + '\n'
            full_line = ''
    return full_text


def part_to_text(part):
    if part.get_content_type() != 'text/plain':
        return None
    charset = part.get_content_charset()
    if not charset:
        return None
    text = str(part.get_payload(decode=True), encoding=charset, errors='ignore')
    try:
        text = str(text.encode('ascii'), 'ascii')
    except UnicodeEncodeError:
        return None
    except UnicodeDecodeError:
        return None
    if part.get_param('format') == 'flowed':
        text = unflow_text(text, part.get_param('delsp', False))
    return text


def message_to_text(message):
    text = ''
    for part in message.walk():
        part = part_to_text(part)
        if part:
            text += part
    return text


def print_mailbox(mailbox, author):
    for message in mailbox:
        if not message['From']:
            continue
        if author not in message['From']:
            continue
        if not message['To']:
            continue
        if author in message['To']:
            continue
        text = message_to_text(message)
        text = munge_message(text)
        if text and len(text) > 0:
            print(text)


def main():
    mb = mailbox.mbox('Sent.mbox', create=False)
    print_mailbox(mb, '<sydius@gmail.com>')


if __name__ == '__main__':
    main()