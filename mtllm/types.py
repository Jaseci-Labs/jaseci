"""Type classes for the mtllm package."""

import base64
import importlib
import importlib.util
from io import BytesIO
from typing import Any

from jaclang.compiler.semtable import SemInfo, SemRegistry, SemScope

from mtllm.utils import extract_non_primary_type, get_object_string, get_type_annotation

cv2 = importlib.import_module("cv2") if importlib.util.find_spec("cv2") else None
PILImage = (
    importlib.import_module("PIL.Image") if importlib.util.find_spec("PIL") else None
)


class Video:
    """Class to represent a video."""

    def __init__(self, file_path: str, seconds_per_frame: int = 2) -> None:
        """Initializes the Video class."""
        assert (
            cv2 is not None
        ), "Please install the required dependencies by running `pip install mtllm[video]`."
        self.file_path = file_path
        self.seconds_per_frame = seconds_per_frame

    def process(
        self,
    ) -> list:
        """Processes the video and returns a list of base64 encoded frames."""
        assert (
            cv2 is not None
        ), "Please install the required dependencies by running `pip install mtllm[video]`."

        assert self.seconds_per_frame > 0, "Seconds per frame must be greater than 0"

        base64_frames = []

        video = cv2.VideoCapture(self.file_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        video_total_seconds = total_frames / fps
        assert (
            video_total_seconds > self.seconds_per_frame
        ), "Video is too short for the specified seconds per frame"
        assert (
            video_total_seconds < 4
        ), "Video is too long. Please use a video less than 4 seconds long."

        frames_to_skip = int(fps * self.seconds_per_frame)
        curr_frame = 0
        while curr_frame < total_frames - 1:
            video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
            curr_frame += frames_to_skip
        video.release()
        return base64_frames


class Image:
    """Class to represent an image."""

    def __init__(self, file_path: str) -> None:
        """Initializes the Image class."""
        assert (
            PILImage is not None
        ), "Please install the required dependencies by running `pip install mtllm[image]`."
        self.file_path = file_path

    def process(self) -> tuple[str, str]:
        """Processes the image and returns a base64 encoded image and its format."""
        assert (
            PILImage is not None
        ), "Please install the required dependencies by running `pip install mtllm[image]`."
        image = PILImage.open(self.file_path)
        img_format = image.format
        with BytesIO() as buffer:
            image.save(buffer, format=img_format, quality=100)
            return (
                base64.b64encode(buffer.getvalue()).decode("utf-8"),
                img_format.lower(),
            )


class TypeExplanation:
    """Class to represent a type explanation."""

    def __init__(self, type_item: str, mod_registry: SemRegistry) -> None:
        """Initializes the TypeExplanation class."""
        self.type_item = type_item
        self.explanation, self._nested_types = self.get_type_explanation(mod_registry)

    def get_type_explanation(self, mod_registry: SemRegistry) -> tuple[str, set[str]]:
        """Get the type explanation of the input type string."""
        scope, sem_info = mod_registry.lookup(name=self.type_item)
        if isinstance(sem_info, SemInfo) and sem_info.type:
            sem_info_scope = SemScope(sem_info.name, sem_info.type, scope)
            _, type_info = mod_registry.lookup(scope=sem_info_scope)
            type_info_str = []
            type_info_types = []
            type_example = [f"{sem_info.name}("]
            if sem_info.type == "Enum" and isinstance(type_info, list):
                for enum_item in type_info:
                    type_info_str.append(
                        f"{enum_item.semstr} ({enum_item.name}) (EnumItem)".strip()
                    )
                type_example[0] = type_example[0].replace("(", f".{enum_item.name}")
            elif sem_info.type in ["obj", "class", "node", "edge"] and isinstance(
                type_info, list
            ):
                for arch_item in type_info:
                    if arch_item.type in ["obj", "class", "node", "edge"]:
                        continue
                    type_info_str.append(
                        f"{arch_item.semstr} ({arch_item.name}) ({arch_item.type})".strip()
                    )
                    type_example.append(f"{arch_item.name}={arch_item.type}, ")
                    if arch_item.type and extract_non_primary_type(arch_item.type):
                        type_info_types.extend(extract_non_primary_type(arch_item.type))
                if len(type_example) > 1:
                    type_example[-1] = type_example[-1].replace(", ", ")")
                else:
                    type_example.append(")")
            return (
                f"{sem_info.semstr} ({sem_info.name}) ({sem_info.type}) eg:- {''.join(type_example)} -> {', '.join(type_info_str)}".strip(),  # noqa: E501
                set(type_info_types),
            )
        return "", set()

    def __str__(self) -> str:
        """Returns the string representation of the TypeExplanation class."""
        return self.explanation

    @property
    def nested_types(self) -> set[str]:
        """Get the nested types of the type."""
        return self._nested_types


class InputInformation:
    """Class to represent the input information."""

    def __init__(self, semstr: str, name: str, value: Any) -> None:  # noqa: ANN401
        """Initializes the InputInformation class."""
        self.semstr = semstr
        self.name = name
        self.value = value

    def __str__(self) -> str:
        """Returns the string representation of the InputInformation class."""
        type_anno = get_type_annotation(self.value)
        return f"{self.semstr if self.semstr else ''} ({self.name}) ({type_anno}) = {get_object_string(self.value)}".strip()  # noqa: E501

    def to_list_dict(self) -> list[dict]:
        """Returns the list of dictionaries representation of the InputInformation class."""
        input_type = get_type_annotation(self.value)
        if input_type == "Image":
            img_base64, img_type = self.value.process()
            return [
                {
                    "type": "text",
                    "text": f"{self.semstr if self.semstr else ''} ({self.name}) (Image) = ".strip(),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{img_type};base64,{img_base64}"},
                },
            ]
        elif input_type == "Video":
            video_frames = self.value.process()
            return [
                {
                    "type": "text",
                    "text": f"{self.semstr if self.semstr else ''} ({self.name}) (Video) = ".strip(),
                },
                *(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{frame}",
                            "detail": "low",
                        },
                    }
                    for frame in video_frames
                ),
            ]
        return [
            {
                "type": "text",
                "text": str(self),
            }
        ]

    def get_types(self) -> list:
        """Get the types of the input."""
        return extract_non_primary_type(get_type_annotation(self.value))


class OutputHint:
    """Class to represent the output hint."""

    def __init__(self, semstr: str, type: str) -> None:  # noqa: ANN401
        """Initializes the OutputHint class."""
        self.semstr = semstr
        self.type = type

    def __str__(self) -> str:
        """Returns the string representation of the OutputHint class."""
        return f"{self.semstr if self.semstr else ''} ({self.type})".strip()

    def get_types(self) -> list:
        """Get the types of the output."""
        return extract_non_primary_type(self.type)


class Information:
    """Class to represent the information."""

    def __init__(
        self, filtered_registry: SemRegistry, name: str, value: Any  # noqa: ANN401
    ) -> None:
        """Initializes the Information class."""
        self.name = name
        self.value = value
        self.registry = filtered_registry

    @property
    def semstr(self) -> str:
        """Get the semantic string of the information."""
        _, sem_info = self.registry.lookup(name=self.name)
        return sem_info.semstr if sem_info and isinstance(sem_info, SemInfo) else ""

    @property
    def type(self) -> str:
        """Get the type of the information."""
        _, sem_info = self.registry.lookup(name=self.name)
        return (
            sem_info.type
            if sem_info and isinstance(sem_info, SemInfo)
            else get_type_annotation(self.value)
        )

    def __str__(self) -> str:
        """Returns the string representation of the Information class."""
        type_anno = get_type_annotation(self.value)
        return f"{self.semstr} ({self.name}) ({type_anno}) = {get_object_string(self.value)}".strip()

    def get_types(self) -> list:
        """Get the types of the information."""
        return extract_non_primary_type(self.type)
