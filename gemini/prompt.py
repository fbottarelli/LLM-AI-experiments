two_person_conversation = """
You will be given a audio from a Google Meet. Your task is to extract the dialogue and format it as a conversation between two speakers, labeled as "Person1" and "Person2".

Follow these guidelines to extract and format the dialogue:
1. Identify the two main speakers in the conversation.
2. Label the first speaker who talks as "Person1" and the second speaker as "Person2".
3. Format each line of dialogue as follows:
   <speaker>Person1/Person2</speaker>: [Their dialogue]
4. Start a new line for each change in speaker.
5. the language of the dialogue is Italian.
"""

audio_transcription = """
You are tasked with transcribing an audio file from a YouTube video that explains a topic. Your goal is to accurately convert the spoken content into written text. Follow these instructions carefully:
1. Listen to the audio file carefully, paying attention to every word and sound.
2. Transcribe the content of the audio file into text
3. Format your transcription as follows:
   - Use proper capitalization and punctuation.
   - Start a new paragraph for significant topic changes or natural breaks in speech.
   - Use timestamps to mark every 30 seconds of the audio, formatted as [00:30], [01:00], etc.
4. After completing the transcription, review it for accuracy and clarity.

Remember, the goal is to provide an accurate and readable representation of the audio content. Pay close attention to detail and strive for a high-quality transcription that captures both the words and the context of the explanation.
"""