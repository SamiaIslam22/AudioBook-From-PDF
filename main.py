import pyttsx3
import PyPDF2
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

def convert_pdf_to_speech():
    try:
        # Open file dialog
        root = Tk()
        root.withdraw()  # Hide the main window
        book = askopenfilename(title="Select PDF File",
                             filetypes=[("PDF Files", "*.pdf")])
        
        if not book:  # If user cancels file selection
            print("No file selected. Exiting...")
            return

        # Initialize PDF reader
        pdfreader = PyPDF2.PdfReader(book)
        pages = len(pdfreader.pages)

        # Initialize text-to-speech engine
        player = pyttsx3.init()
        
        # Customize voice settings
        voices = player.getProperty('voices')
        player.setProperty('voice', voices[0].id)  # Index 0 for male, 1 for female
        player.setProperty('rate', 150)    # Speaking rate (default is 200)
        player.setProperty('volume', 0.8)  # Volume (max is 1.0)

        # Get page range from user
        start_page = max(0, int(input(f"Enter start page (1-{pages}): ")) - 1)
        end_page = min(pages, int(input(f"Enter end page (1-{pages}): ")))

        print(f"\nConverting PDF to speech...\nPages: {start_page + 1} to {end_page}")
        
        # Process each page
        for num in range(start_page, end_page):
            print(f"\nReading page {num + 1}/{pages}")
            try:
                page = pdfreader.pages[num]
                text = page.extract_text()
                
                if not text.strip():  # Check if page is empty
                    print(f"Page {num + 1} appears to be empty or contains no readable text")
                    continue
                
                player.say(text)
                player.runAndWait()
                
                # Allow user to pause/continue after each page
                if num < end_page - 1:
                    response = input("\nPress Enter to continue to next page, or 'q' to quit: ")
                    if response.lower() == 'q':
                        break
                        
            except Exception as e:
                print(f"Error processing page {num + 1}: {str(e)}")
                continue

        print("\nFinished converting PDF to speech!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
if __name__ == "__main__":
    convert_pdf_to_speech()