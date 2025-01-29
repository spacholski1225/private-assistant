from smolagents import Tool

class HFModelDownloadsTool(Tool):
    name = "stretching_video_link "
    description = """
    To jest narzędzie które zwraca link do filmu z rozciąganiem."""
    inputs = {
        "task": {
            "type": "string",
            "description": "the task category (such as text-classification, depth-estimation, etc)",
        }
    }
    output_type = "string"

    def forward(self, task: str):
        return "https://www.youtube.com/watch?v=VpEqzDHWTB4&ab_channel=BorysMankowskiTazDrill"

model_downloads_tool = HFModelDownloadsTool()