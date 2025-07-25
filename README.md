# Glyph Atlas

**Glyph Atlas** is a tool for generating a font sprite atlas that supports characters and emoji. It allows you to create a PNG and JSON file which can be used to generate a GL texture for rendering text using a sprite atlas of characters. This tool is particularly useful for creating pixelated fonts for WebGL applications.

## Features

- **Font Atlas Generator**: Create a sprite-based font atlas containing both ASCII characters and emoji.
- **Text Rendering**: Render text using the generated font atlas, with customization for scale, color, and spacing.
- **Export Options**: Download the generated atlas as both PNG and JSON files for easy integration into your projects.
- **Emoji Support**: Includes built-in support for common emoji like `:heart:`, `:sparkles:`, and `:skull:`.
- **Responsive and Customizable**: Adjustable atlas scale and rendering options to meet various design needs.

## Demo

You can interact with the tool directly in your browser at https://rjwalters.github.io/glyph-atlas/. Here's what you can do:

1. Generate a font sprite atlas.
2. Render custom text using the generated atlas with emojis.
3. Export the font atlas as a PNG image and JSON file.

## Installation

To use the Glyph Atlas tool locally, simply clone or download the repository and open the `index.html` file in your browser.

```bash
git clone https://github.com/rjwalters/glyph-atlas.git
cd glyph-atlas
open index.html
````

## Usage

1. **Generate the Font Atlas**:

   * Use the "Generate Atlas" button to create the sprite font atlas. The atlas will include all the characters and emojis defined in the `CHAR_MAP` and `EMOJI_CODES`.
   * You can adjust the scale of the atlas using the `Atlas Scale` input.
2. **Export the Atlas**:

   * Once the atlas is generated, you can save the `font.png` and `font.json` files using the respective buttons.
   * The JSON file contains the character positions and metadata to help you map the font atlas in your WebGL application.
3. **Render Text**:

   * In the `Text Renderer` section, type your desired text and use emoji codes like `:love:`, `:sparkles:`, and others.
   * Adjust the scale, color, and spacing to fit your needs.
   * The rendered text will appear on the canvas below the controls.

## Configuration

* **Atlas Scale**: Scale factor for the font atlas. A higher scale results in a higher resolution atlas.
* **Text Scale**: Scale factor for the rendered text. Allows resizing of individual characters.
* **Text Color**: Set the color for rendered text.
* **Spacing**: Adjust the space between characters in the rendered text.

## Example

To render the text "Hello! I ❤️ sprite fonts!" with custom settings:

1. **Type the text** into the `Text Renderer` textarea.
2. **Adjust the scale, color, and spacing** to your liking.
3. **Click "Render Text"** to display the output on the canvas.

The font atlas will be used to render the text, and you can adjust the appearance with the controls provided.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this project, open issues, or submit pull requests for improvements.

