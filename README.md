# Mbox-to-Text

`mbox_to_txt.py` is a simple Python script that takes an mbox file and converts it into a text file.

It was created to process a Gmail sent box into a text file that could be used as a corpus for other tools. As such, it
does some filtering on the mail:

  * All mail not sent by the specified author is ignored.
  * All mail that is to the specified author is ignored.
  * All mail that is not text/plain is ignored (most messages include text/plain, however).
  * If a message cannot be converted to ASCII, it is ignored.
  * An attempt to remove quoted replies, embedded links, and other probably-not-typed-by-the-author text is made.

Additionally, flowed e-mails are processed per RFC 3637.

## Usage

    python mbox_to_txt.py Sent.mbox "<sydius@gmail.com>" > corpus.txt

## Limitations

This script was made to process the e-mail sent by Gmail, as such it will probably need modification to properly filter
mail sent by other clients. This should be relatively straight-forward by modifying the collection of regular
expressions at the top of the script.

Because of its purpose in creating a corpus of analysis, it errs on the side of removing information. It very likely
removes some amount of text that was sent by the author erroneously. It also does not do a perfect job of removing text
not sent by the author, so the output should be inspected and the script modified accordingly.

## Retrieving Gmail Sent Mail

To retrieve your sent mail from Gmail in the format read by this script, you can visit:

http://google.com/takeout

Once there, follow the instructions to export your Gmail "sent" label. You will, after some time, receive an archive
containing the `Sent.mbox` file.
