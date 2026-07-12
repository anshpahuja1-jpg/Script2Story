# Script2Story — AI Storyboard Generator

Converts a screenplay into a visual storyboard PDF using AI-generated images.

## Setup (do this once)

1. Open terminal in this folder
2. Run:
   pip install -r requirements.txt

## Run

python main.py

## Output

Opens storyboard.pdf with all scenes laid out as a storyboard.

## Use your own script

Replace the contents of script.txt with your own screenplay.
Format it like this:

INT. LOCATION - TIME

Description of the scene.

EXT. ANOTHER LOCATION - DAY

More description.

## Notes

- Uses Hugging Face free API for image generation
- If API is slow, it retries automatically
- If API fails completely, placeholder images are used so PDF still generates
- First run may be slow (model loading) — subsequent runs are faster
