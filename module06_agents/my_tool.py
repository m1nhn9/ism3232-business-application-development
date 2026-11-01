# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define a read-only FAQ tool so business answers stay outside conversation code.
class FAQBook:
    # Describe the tool's job for readers and help().
    """Find known FAQ topics and retrieve their stored answers."""

    # Receive the answer dictionary so the same tool can serve different shops.
    def __init__(self, answers):
        # Document which information belongs to the tool.
        """Store a dictionary mapping lowercase topics to answers."""
        # Keep the supplied answers as this object's lookup data.
        self.answers = answers

    # Identify a known topic from text without adding conversation behavior.
    def find_topic(self, text):
        # Explain the absence result so callers can handle failed lookups.
        """Return the first known topic in text, or None."""
        # Inspect known topic keys in their dictionary insertion order.
        for topic in self.answers:
            # Normalize user text so topic matching ignores capitalization.
            if topic in text.lower():
                # Return the recognized key so the caller can retrieve its answer.
                return topic
        # Indicate no known topic rather than guessing an answer.
        return None

    # Keep retrieving an answer separate from recognizing its topic.
    def answer_for(self, topic):
        # State the missing-data behavior instead of implying every topic exists.
        """Return the stored answer, or None if no answer is available."""
        # Check the key before indexing so unknown topics do not cause KeyError.
        if topic in self.answers:
            # Return only the stored information without making up shop policies.
            return self.answers[topic]
        # Let the assistant explain a failed lookup safely.
        return None
