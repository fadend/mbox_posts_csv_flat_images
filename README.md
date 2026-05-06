# Extract posts from an mbox file

Create a CSV in the same format as https://github.com/fadend/gg_posts_csv_flat_images.

This is part of a project to preserve posts from a photo mailing list.

## Usage

Since this has no external dependencies, we can run it directly like so:

```
python mbox_posts_csv_flat_images/extract.py \
  --input_mbox "/Volumes/ThumbDrive/Test.mbox/mbox" \
  --output_dir $HOME/projects/mbox_output
```

You can also add the `--save_html` flag if you want to store HTML
copies of the posts as well for debugging purposes.

## Tests

Using the builtin testing framework.
```
python -m unittest tests/extract_test.py
```

## Acknowledgments

Formatting Python with [black](https://github.com/psf/black).
