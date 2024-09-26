from rich.console import Console
from rich.text import Text

console = Console()

class Text_Style:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def common_text(self, primary_text: str, error_text: str, text_color="black", text_style="normal") -> None:
        """
        Function to display two styled texts in the console.
        
        Parameters:
        - primary_text (str): The main text to display.
        - error_text (str): The error or secondary text to display.
        - text_color (str): The color of the text. Default is "black".
        - text_style (str): Additional styles (e.g., "bold", "italic"). Default is "normal".
        """
        # Combine the text color and style into one string
        style = f"{text_style} {text_color}"

        # Create rich text objects for both texts
        styled_primary = Text(primary_text, style=style)
        styled_error = Text(error_text, style=style)

        # Print both styled texts to the console in one line
        console.print(styled_primary, styled_error)

# Example usage
if __name__ == "__main__":
    text_style = Text_Style()
    text_style.common_text("This is the exception of the text", "This is an error message.", "red", "bold")
