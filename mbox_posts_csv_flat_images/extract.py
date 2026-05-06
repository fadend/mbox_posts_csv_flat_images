"""Extracts HTML text and photos from an mbox file."""

import argparse
import csv
import hashlib
import mailbox
import os
import re
import sys

# Expected output CSV columns.
OUTPUT_COLS = ("Title", "Content", "Date", "Image Featured", "Tags")


def extract_body_content(html: str) -> str:
    return re.sub(r"^.*<body(\s[^>]*)?>\s*|\s*</body>.*$", "", html, flags=re.DOTALL)


def convert_mbox_to_csv(
    mbox_path: str, output_dir: str, max_posts: int = -1, save_html=False
):
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    with open(os.path.join(output_dir, "posts.csv"), "wt", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_COLS)
        w.writeheader()
        for message_index, message in enumerate(mailbox.mbox(mbox_path), max_posts):
            if max_posts >= 0 and message_index >= max_posts:
                break
            subject = message["Subject"]
            if not subject:
                print(
                    f"Missing Subject for message {message_index} in {mbox_path}",
                    file=sys.stderr,
                )
                continue
            content = ""
            content_id_to_image_bytes = {}
            for part in message.walk():
                content_id = part.get("Content-Id")
                content_type = part.get_content_type()
                if content_type == "text/html":
                    content = part.get_payload(decode=True).decode("utf8")
                elif content_type == "image/jpeg":
                    if not content_id:
                        print(
                            f"Missing Content-Id for jpeg for message {message_index} in {mbox_path}",
                            file=sys.stderr,
                        )
                    else:
                        # The Content-Id values seem to be surrounded in brackets.
                        content_id = content_id.strip("<>")
                        content_id_to_image_bytes[content_id] = part.get_payload(
                            decode=True
                        )
            if not content:
                print(
                    f"Missing content for message {message_index} in {mbox_path}",
                    file=sys.stderr,
                )
                continue

            hash = hashlib.blake2b(digest_size=10)
            hash.update(content.encode("utf8"))
            normed_subject = re.sub(
                r"_+", "_", re.sub(r"[^a-z0-9]", "_", subject.lower())
            ).strip("_")
            basename = normed_subject + "_" + hash.hexdigest()

            content_id_to_file = {}
            first_image = ""

            def update_img(m):
                nonlocal first_image
                nonlocal content_id_to_file
                original = m[0]
                src = m[1]
                if not src.startswith("cid:"):
                    return original
                content_id = src[4:]
                if content_id not in content_id_to_image_bytes:
                    print(
                        f"Unknown img {content_id} in message {message_index} in {mbox_path}",
                        file=sys.stderr,
                    )
                    return original
                if content_id not in content_id_to_file:
                    filename = f"images/{basename}_{len(content_id_to_file)}.jpeg"
                    with open(os.path.join(output_dir, filename), "wb") as f:
                        f.write(content_id_to_image_bytes[content_id])
                    content_id_to_file[content_id] = filename
                filename = content_id_to_file[content_id]
                if not first_image:
                    first_image = filename
                return f'<img src="{filename}">'

            content = re.sub(r'<img\b[^>]* src=\"([^"]+)\"[^>]*>', update_img, content)

            if save_html:
                html_file = os.path.join(output_dir, basename + ".html")
                with open(html_file, "wt", encoding="utf8") as f:
                    f.write(content)

            row = {key: "" for key in OUTPUT_COLS}
            row["Title"] = subject
            row["Content"] = extract_body_content(content)
            row["Date"] = message["Date"]
            row["Image Featured"] = first_image
            w.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="mbox_posts_csv_flat_images")
    parser.add_argument(
        "--input_mbox",
        help="mbox format file. Note: may be contained within a .mbox dir.",
        required=True,
    )
    parser.add_argument(
        "--output_dir", help="Directory in which to generate output", required=True
    )
    parser.add_argument(
        "--max_posts",
        help="Max posts to output. Useful for test runs.",
        type=int,
        default=-1,
    )
    parser.add_argument(
        "--save_html",
        help="Save separate .html files as well. Useful for debugging",
        action="store_true",
    )
    args = parser.parse_args()
    convert_mbox_to_csv(
        mbox_path=args.input_mbox,
        output_dir=args.output_dir,
        max_posts=args.max_posts,
        save_html=args.save_html,
    )
