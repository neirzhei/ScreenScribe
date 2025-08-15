An offline-first AI companion that provides real-time, spoken commentary on your screen activity to offer encouragement and witty observations.

## How It Works
This program is designed to run entirely offline on consumer hardware. It operates in a simple loop:

1. **Capture:** Periodically, it takes a screenshot of the user's primary monitor.

2. **Analyze:** A vision model analyzes the screenshot to generate a factual description of the on-screen activity.

3. **Comment:** A large language model (LLM) takes this description and generates a short, conversational, and encouraging or witty comment.

4. **Speak:** A text-to-speech (TTS) model synthesizes the comment into audio and plays it aloud.

To conserve system resources, each AI model is loaded into memory only when needed and unloaded immediately after its task is complete.

## Installation & Usage
This project is containerized using Docker for easy setup.

1. **Prerequisites:**

- A Linux-based operating system (tested on Debian/Ubuntu).

- Docker and Docker Compose installed.

- An active internet connection for the initial model download.

2. **Configuration:**

- Clone the repository.

- Key parameters like model repositories, GPU layer offloading (`LLM_GPU_LAYERS`), and commentary frequency (`MIN/MAX_INTERVAL_MINUTES`) can be adjusted in `src/config.py`.

3. **Running the Application:**

- Open a terminal in the project's root directory.

- Run the command: `docker-compose up --build`

- The companion will now be running in the background. To stop it, press Ctrl+C in the terminal.

## Potential Improvements

- **Two-way Communication:** User being able to reply to the companion's commentaries.
- **Conversational Memory:** A short-term memory system, allowing the companion to recall the last few interactions. This will make its comments more contextually relevant, natural, and engaging over time.
- **GPU Acceleration:** Significantly reduce the time from screenshot to spoken comment.
- **Cross-Platform Support:** Re-engineer the screen capture and audio playback modules to be compatible with Windows and macOS, making the companion OS-Independent.