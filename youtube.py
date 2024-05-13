import googleapiclient.discovery
from config import get_secret_key
import pandas as pd
import re


class YoutubeCrawler:
    def __init__(self):
        self.api_service_name = "youtube"
        self.api_version = "v3"

    # Get Comment
    def crawl_comments(self, video_id, req_result):

        youtube = googleapiclient.discovery.build(
            self.api_service_name,
            self.api_version,
            developerKey=get_secret_key(),
        )

        max_result = int(req_result)

        results = []

        nextPageToken = None

        while len(results) < max_result:
            req = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken,
            )
            response = req.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comment_text = re.sub(
                    r"<.*?>", "", comment["textDisplay"]
                )  # Remove HTML tags
                author_without_at = re.sub(
                    r"@", "", comment["authorDisplayName"]
                )  # Remove '@' symbol

                if (
                    len(comment_text) >= 20
                ):  # Only add comments with at least 20 characters
                    results.append(
                        {
                            "author": author_without_at,
                            "like_count": comment["likeCount"],
                            "comment": comment_text,
                            "authorImage": comment["authorProfileImageUrl"],
                        }
                    )

                if (
                    len(results) >= max_result
                ):  # Break if we have collected enough comments
                    break

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:  # Break the loop if no more pages are available
                break

        result_processor = ResultProcessor(results)
        html_output = result_processor.normalize_alay()

        return html_output


class ResultProcessor:
    def __init__(self, result):
        self.result = result

    def normalize_alay(self):
        alay_dict = pd.read_csv(
            "https://raw.githubusercontent.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection/master/new_kamusalay.csv",
            names=["original", "replacement"],
            encoding="latin-1",
        )
        alay_dict_map = dict(zip(alay_dict["original"], alay_dict["replacement"]))

        for item in self.result:
            item["comment_normalized"] = " ".join(
                alay_dict_map.get(word, word) for word in item["comment"].split()
            )

        return self.process_to_html()

    def process_to_html(self):

        # Convert result to DataFrame
        new_df = pd.DataFrame(self.result)

        # Rename columns and format HTML for the UserImage
        if "authorImage" in new_df.columns:
            new_df["UserImage"] = new_df["authorImage"].apply(
                lambda x: f'<img src="{x}" width="50" height="50">'
            )
        else:
            new_df["UserImage"] = (
                f'<img src="default_image_url_here" width="50" height="50">'
            )

        df_process = new_df[["UserImage", "author", "comment_normalized", "like_count"]]
        print(len(df_process["author"]))

        # Rename columns for HTML presentation
        df_process.rename(
            columns={
                "UserImage": "User Images",
                "author": "Username",
                "comment_normalized": "Review",
                "like_count": "Like",
            },
            inplace=True,
        )

        # Use Pandas to_html to convert DataFrame to HTML table
        table_classes = "table table-responsive table-striped text-center"
        html_output = df_process.to_html(
            index=False, escape=False, header=True, classes=table_classes
        )

        return html_output
