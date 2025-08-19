#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "numpy",
#     "pillow",
# ]
# ///
"""
Center transparent PNG images based on their center of mass.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def center_transparent_png(input_path, output_path=None, output_size=500, verbose=True):
    """
    Centers a transparent PNG based on the center of mass of non-transparent pixels.
    
    Args:
        input_path: Path to the input PNG file
        output_path: Path to save the centered PNG (if None, uses input_name_out.png)
        output_size: Size of the output square image (default: 500x500)
        verbose: Print processing details
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Handle output path
        input_path = Path(input_path)
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_out.png"
        else:
            output_path = Path(output_path)
        
        # Open the image and convert to RGBA if needed
        img = Image.open(input_path).convert('RGBA')
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Extract alpha channel
        alpha = img_array[:, :, 3]
        
        # Create binary mask where non-transparent pixels are 1
        mask = (alpha > 0).astype(np.float32)
        
        # Find the center of mass
        total_mass = np.sum(mask)
        
        if total_mass == 0:
            print(f"Warning: {input_path} is completely transparent!", file=sys.stderr)
            return False
        
        # Calculate center of mass coordinates
        y_coords, x_coords = np.meshgrid(np.arange(mask.shape[0]), np.arange(mask.shape[1]), indexing='ij')
        
        center_y = np.sum(y_coords * mask) / total_mass
        center_x = np.sum(x_coords * mask) / total_mass
        
        # Get the bounding box of non-transparent pixels
        non_zero_y, non_zero_x = np.where(mask > 0)
        
        if len(non_zero_y) == 0:
            print(f"Warning: {input_path} has no non-transparent pixels!", file=sys.stderr)
            return False
        
        min_y, max_y = non_zero_y.min(), non_zero_y.max()
        min_x, max_x = non_zero_x.min(), non_zero_x.max()
        
        # Calculate the size of the content
        content_height = max_y - min_y + 1
        content_width = max_x - min_x + 1
        
        # Create new transparent image
        new_img = Image.new('RGBA', (output_size, output_size), (0, 0, 0, 0))
        
        # Calculate offset to center the image based on center of mass
        offset_x = int(output_size / 2 - center_x)
        offset_y = int(output_size / 2 - center_y)
        
        # Ensure the image fits within bounds
        # Calculate the actual bounds after offset
        new_min_x = min_x + offset_x
        new_max_x = max_x + offset_x
        new_min_y = min_y + offset_y
        new_max_y = max_y + offset_y
        
        # Adjust offset if image goes out of bounds
        if new_min_x < 0:
            offset_x -= new_min_x
        elif new_max_x >= output_size:
            offset_x -= (new_max_x - output_size + 1)
        
        if new_min_y < 0:
            offset_y -= new_min_y
        elif new_max_y >= output_size:
            offset_y -= (new_max_y - output_size + 1)
        
        # Paste the original image at the calculated position
        new_img.paste(img, (offset_x, offset_y), img)
        
        # Save the result
        new_img.save(output_path, 'PNG')
        
        if verbose:
            print(f"Processed: {input_path}")
            print(f"  Original size: {img.size}")
            print(f"  Center of mass: ({center_x:.1f}, {center_y:.1f})")
            print(f"  Content size: {content_width}x{content_height}")
            print(f"  Offset applied: ({offset_x}, {offset_y})")
            print(f"  Saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        return False

def process_directory(input_dir, output_dir, size, quiet):
    """
    Process all PNG files in a directory.
    
    Args:
        input_dir: Input directory path
        output_dir: Output directory path
        size: Output image size
        quiet: Suppress verbose output
    
    Returns:
        Tuple of (success_count, total_count)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all PNG files
    png_files = list(input_path.glob('*.png')) + list(input_path.glob('*.PNG'))
    
    if not png_files:
        print(f"No PNG files found in {input_dir}", file=sys.stderr)
        return 0, 0
    
    if not quiet:
        print(f"Processing {len(png_files)} PNG files from {input_dir} to {output_dir}")
        print()
    
    success_count = 0
    for png_file in png_files:
        output_file = output_path / png_file.name
        if center_transparent_png(png_file, output_file, size, not quiet):
            success_count += 1
        if not quiet:
            print()  # Add spacing between files
    
    return success_count, len(png_files)

def main():
    parser = argparse.ArgumentParser(
        description="Center transparent PNG images based on their center of mass.",
        epilog="Examples:\n"
               "  %(prog)s input.png                    # Creates input_out.png\n"
               "  %(prog)s input.png -o centered.png    # Specify output name\n"
               "  %(prog)s *.png                        # Process multiple files\n"
               "  %(prog)s ./pngs                       # Process directory, creates ./pngs_out/\n"
               "  %(prog)s input.png -s 1024           # Create 1024x1024 output\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Input PNG file(s) or directory to process'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path or directory (only valid with single input)'
    )
    
    parser.add_argument(
        '-s', '--size',
        type=int,
        default=500,
        help='Output image size in pixels (default: 500, creates 500x500 image)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.output and len(args.input) > 1:
        parser.error("Cannot specify --output with multiple inputs")
    
    if args.size <= 0:
        parser.error("Size must be positive")
    
    # Check if single input is a directory
    if len(args.input) == 1 and Path(args.input[0]).is_dir():
        input_dir = Path(args.input[0])
        
        # Determine output directory
        if args.output:
            output_dir = Path(args.output)
        else:
            # Default: add _out suffix to input directory name
            output_dir = input_dir.parent / f"{input_dir.name}_out"
        
        # Process directory
        success_count, total_count = process_directory(input_dir, output_dir, args.size, args.quiet)
        
        if not args.quiet and total_count > 0:
            print(f"Processed {success_count}/{total_count} files successfully")
        
        # Exit with error code if any files failed
        if success_count < total_count:
            sys.exit(1)
    
    else:
        # Process individual files
        success_count = 0
        total_count = 0
        
        for input_item in args.input:
            input_path = Path(input_item)
            
            if input_path.is_dir():
                print(f"Error: {input_item} is a directory. Use a single directory as input to process all PNGs within it.", file=sys.stderr)
                continue
                
            if not input_path.exists():
                print(f"Error: File not found: {input_item}", file=sys.stderr)
                continue
            
            if not input_path.suffix.lower() == '.png':
                print(f"Warning: Skipping non-PNG file: {input_item}", file=sys.stderr)
                continue
            
            total_count += 1
            
            # Determine output path
            if args.output and len(args.input) == 1:
                output_path = args.output
            else:
                output_path = None  # Will use default naming
            
            # Process the file
            if center_transparent_png(input_path, output_path, args.size, not args.quiet):
                success_count += 1
            
            if not args.quiet and len(args.input) > 1:
                print()  # Add spacing between files
        
        # Summary for multiple files
        if total_count > 1 and not args.quiet:
            print(f"Processed {success_count}/{total_count} files successfully")
        
        # Exit with error code if any files failed
        if success_count < total_count:
            sys.exit(1)

if __name__ == "__main__":
    main()